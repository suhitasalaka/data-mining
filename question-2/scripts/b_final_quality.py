import pandas as pd
import glob
import re
import numpy as np

print("Loading labelled pairs...")

pairs = pd.read_csv(".\\labelled_pairs.csv")

files = glob.glob(".\\notices\\*.csv")

dfs = [
    pd.read_csv(f, usecols=["notice_id", "portal_id", "title", "body"],
                low_memory=False)
    for f in files
]

df = pd.concat(dfs, ignore_index=True)
df = df.set_index("notice_id")


def clean(text, portal):

    text = str(text)

    if portal in {"P001", "P002", "P005"}:
        marker = "NATIONAL PROCUREMENT AGGREGATION SERVICE"
        pos = text.upper().find(marker)
        if pos >= 0:
            text = text[pos + len(marker):]
            text = re.sub(
                r"DISCLAIMER.*$",
                " ",
                text,
                flags=re.IGNORECASE | re.DOTALL
            )

    elif portal in {"P003", "P004", "P006"}:
        marker = "STATE PROCUREMENT CELL"
        pos = text.upper().find(marker)
        if pos >= 0:
            text = text[pos + len(marker):]

    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()

    return text


def shingles(text, k=5):
    return set(text[i:i+k] for i in range(len(text)-k+1))


raw_sets = {}
clean_sets = {}

for notice_id, row in df.iterrows():

    raw = str(row["title"]) + " " + str(row["body"])

    raw_norm = re.sub(r"\s+", " ", raw.lower()).strip()

    cleaned = clean(raw, row["portal_id"])

    raw_sets[notice_id] = shingles(raw_norm)
    clean_sets[notice_id] = shingles(cleaned)


raw_scores = []
clean_scores = []
labels = []

for _, p in pairs.iterrows():

    a = p["notice_id_a"]
    b = p["notice_id_b"]

    raw_a = raw_sets[a]
    raw_b = raw_sets[b]

    clean_a = clean_sets[a]
    clean_b = clean_sets[b]

    raw_scores.append(len(raw_a & raw_b) / len(raw_a | raw_b))
    clean_scores.append(len(clean_a & clean_b) / len(clean_a | clean_b))

    labels.append(str(p["label"]).lower())


raw_scores = np.array(raw_scores)
clean_scores = np.array(clean_scores)
labels = np.array(labels)

same = np.isin(labels, ["1", "same", "true"])
different = np.isin(labels, ["0", "different", "false"])

print("\nBOILERPLATE MITIGATION QUALITY")
print("=" * 60)

print("Same pairs:", same.sum())
print("Different pairs:", different.sum())

print("\nRAW JACCARD")
print("Same mean:", round(raw_scores[same].mean(), 4))
print("Different mean:", round(raw_scores[different].mean(), 4))

print("\nCLEANED JACCARD")
print("Same mean:", round(clean_scores[same].mean(), 4))
print("Different mean:", round(clean_scores[different].mean(), 4))

print("\nCHANGE")
print(
    "Same-pair mean change:",
    round(
        (clean_scores[same].mean() - raw_scores[same].mean()),
        4
    )
)

print(
    "Different-pair mean change:",
    round(
        (clean_scores[different].mean() - raw_scores[different].mean()),
        4
    )
)

# High-confidence retrieval threshold
threshold = 0.60

raw_recall = (raw_scores[same] >= threshold).mean()
clean_recall = (clean_scores[same] >= threshold).mean()

raw_fp = (raw_scores[different] >= threshold).mean()
clean_fp = (clean_scores[different] >= threshold).mean()

print("\nAT JACCARD THRESHOLD =", threshold)

print("Raw same-pair recall:",
      round(raw_recall * 100, 2), "%")

print("Cleaned same-pair recall:",
      round(clean_recall * 100, 2), "%")

print("Raw different-pair rate:",
      round(raw_fp * 100, 2), "%")

print("Cleaned different-pair rate:",
      round(clean_fp * 100, 2), "%")

print("\nDONE")