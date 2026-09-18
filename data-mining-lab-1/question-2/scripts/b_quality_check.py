import pandas as pd
import glob
import re

print("Loading labelled pairs...")

pairs = pd.read_csv(".\\labelled_pairs.csv")

files = glob.glob(".\\notices\\*.csv")

dfs = [
    pd.read_csv(
        f,
        usecols=["notice_id", "portal_id", "title", "body"],
        low_memory=False
    )
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


survived_before = []
survived_after = []

for _, p in pairs.iterrows():

    a = df.loc[p["notice_id_a"]]
    b = df.loc[p["notice_id_b"]]

    # Before mitigation:
    # same portal = candidate
    before = a["portal_id"] == b["portal_id"]

    # After mitigation:
    # same portal + first 20 cleaned characters
    ta = clean(
        str(a["title"]) + " " + str(a["body"]),
        a["portal_id"]
    )

    tb = clean(
        str(b["title"]) + " " + str(b["body"]),
        b["portal_id"]
    )

    after = (
        a["portal_id"] == b["portal_id"]
        and ta[:20] == tb[:20]
    )

    survived_before.append(before)
    survived_after.append(after)


survived_before = pd.Series(survived_before)
survived_after = pd.Series(survived_after)

labels = pairs["label"].astype(str).str.lower()

same = labels.isin(["1", "same", "true"])
different = labels.isin(["0", "different", "false"])

print("\nQUALITY CHECK")
print("=" * 60)

print("Total labelled pairs:", len(pairs))
print("Same pairs:", int(same.sum()))
print("Different pairs:", int(different.sum()))

print("\nBEFORE MITIGATION")
print("Same-pair survival:",
      round(survived_before[same].mean() * 100, 2), "%")

print("Different-pair survival:",
      round(survived_before[different].mean() * 100, 2), "%")

print("\nAFTER MITIGATION")
print("Same-pair survival:",
      round(survived_after[same].mean() * 100, 2), "%")

print("Different-pair survival:",
      round(survived_after[different].mean() * 100, 2), "%")

print("\nCHANGE IN SAME-PAIR RECALL:",
      round(
          (survived_after[same].mean()
           - survived_before[same].mean()) * 100,
          2
      ),
      "percentage points")

print("\nDONE")