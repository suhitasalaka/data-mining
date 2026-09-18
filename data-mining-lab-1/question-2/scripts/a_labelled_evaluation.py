import pandas as pd
import glob
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# LOAD NOTICES
# --------------------------------------------------

files = glob.glob("notices/*.csv")

notices = pd.concat(
    [pd.read_csv(f) for f in files],
    ignore_index=True
)

print("Total notices:", len(notices))


# --------------------------------------------------
# CREATE NOTICE TEXT
# --------------------------------------------------

notices["text"] = (
    notices["title"].fillna("").astype(str)
    + " "
    + notices["body"].fillna("").astype(str)
)


# --------------------------------------------------
# NORMALIZATION
# --------------------------------------------------

def normalize_text(text):

    text = text.lower()

    # Remove common portal reference-number patterns
    text = re.sub(
        r'\b(?:npas|spc|pwd|ref|mc|tn)[-/a-z0-9]*\b',
        ' ',
        text
    )

    # Remove long numeric identifiers
    text = re.sub(r'\b\d{5,}\b', ' ', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


notices["normalized_text"] = notices["text"].apply(normalize_text)


# --------------------------------------------------
# LOAD LABELLED PAIRS
# --------------------------------------------------

pairs = pd.read_csv("labelled_pairs.csv")

print("Labelled pairs:", len(pairs))
print("Same:", (pairs["label"] == "same").sum())
print("Different:", (pairs["label"] == "different").sum())


# --------------------------------------------------
# INDEX NOTICES
# --------------------------------------------------

text_map = dict(
    zip(notices["notice_id"], notices["normalized_text"])
)


# --------------------------------------------------
# BUILD CORPUS FOR TF-IDF
# --------------------------------------------------

all_ids = list(notices["notice_id"])

corpus = [
    text_map[x]
    for x in all_ids
]


# --------------------------------------------------
# CHARACTER TF-IDF
# --------------------------------------------------

vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    min_df=2
)

matrix = vectorizer.fit_transform(corpus)

print("TF-IDF matrix shape:", matrix.shape)


# --------------------------------------------------
# MAP NOTICE ID TO MATRIX ROW
# --------------------------------------------------

id_to_index = {
    notice_id: i
    for i, notice_id in enumerate(all_ids)
}


# --------------------------------------------------
# CALCULATE PAIR SIMILARITIES
# --------------------------------------------------

scores = []

for _, row in pairs.iterrows():

    a = id_to_index[row["notice_id_a"]]
    b = id_to_index[row["notice_id_b"]]

    score = cosine_similarity(
        matrix[a],
        matrix[b]
    )[0, 0]

    scores.append(score)


pairs["similarity"] = scores


# --------------------------------------------------
# SUMMARY BY LABEL
# --------------------------------------------------

print()
print("=" * 60)
print("SIMILARITY BY LABEL")
print("=" * 60)

print(
    pairs.groupby("label")["similarity"]
    .agg(["count", "mean", "std", "min", "median", "max"])
)


# --------------------------------------------------
# QUANTILES
# --------------------------------------------------

print()
print("=" * 60)
print("QUANTILES")
print("=" * 60)

for label in ["same", "different"]:

    values = pairs.loc[
        pairs["label"] == label,
        "similarity"
    ]

    print()
    print(label)

    print(
        values.quantile(
            [0.01, 0.05, 0.10, 0.25,
             0.50, 0.75, 0.90, 0.95, 0.99]
        )
    )


# --------------------------------------------------
# THRESHOLD TABLE
# --------------------------------------------------

print()
print("=" * 60)
print("THRESHOLD PERFORMANCE")
print("=" * 60)

for threshold in [0.30, 0.35, 0.40, 0.45, 0.50,
                  0.55, 0.60, 0.65, 0.70, 0.75]:

    predicted_same = pairs["similarity"] >= threshold

    actual_same = pairs["label"] == "same"

    tp = ((predicted_same) & (actual_same)).sum()
    fp = ((predicted_same) & (~actual_same)).sum()
    fn = ((~predicted_same) & (actual_same)).sum()
    tn = ((~predicted_same) & (~actual_same)).sum()

    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0

    fpr = fp / (fp + tn) if fp + tn else 0

    print(
        f"threshold={threshold:.2f} "
        f"TP={tp} FP={fp} FN={fn} TN={tn} "
        f"precision={precision:.3f} "
        f"recall={recall:.3f} "
        f"FPR={fpr:.3f}"
    )