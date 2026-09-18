import pandas as pd
import glob
import re
import time

print("Loading corpus...")

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

print("Total notices:", len(df))
print("Total portals:", df["portal_id"].nunique())


# ---------------------------------------------------------
# BEFORE
# ---------------------------------------------------------

counts = df["portal_id"].value_counts()

before = counts * (counts - 1) // 2

print("\nBEFORE MITIGATION")
print("=" * 60)
print("Total comparisons:", int(before.sum()))
print("Maximum workload:", int(before.max()))
print("Median workload:", float(before.median()))


# ---------------------------------------------------------
# REMOVE KNOWN NODAL BOILERPLATE
# ---------------------------------------------------------

def clean_text(text, portal):

    text = str(text)

    if portal in {"P001", "P002", "P005"}:
        marker = "NATIONAL PROCUREMENT AGGREGATION SERVICE"

        pos = text.upper().find(marker)

        if pos >= 0:
            text = text[pos + len(marker):]

            # Remove repeated disclaimer/footer if present
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

    # Normalize case and whitespace
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()

    return text


start = time.perf_counter()

df["clean_text"] = [
    clean_text(
        str(title) + " " + str(body),
        portal
    )
    for title, body, portal
    in zip(df["title"], df["body"], df["portal_id"])
]

clean_time = time.perf_counter() - start

print("\nBoilerplate removal time:",
      round(clean_time, 4), "seconds")


# ---------------------------------------------------------
# AFTER
#
# Bucket using first 20 meaningful characters.
# This is deliberately simple so the effect of
# boilerplate removal can be measured.
# ---------------------------------------------------------

df["bucket"] = (
    df["portal_id"].astype(str)
    + "_"
    + df["clean_text"].str[:20]
)

bucket_counts = df["bucket"].value_counts()

after = bucket_counts * (bucket_counts - 1) // 2

print("\nAFTER BOILERPLATE MITIGATION")
print("=" * 60)

print("Total candidate comparisons:",
      int(after.sum()))

print("Maximum bucket workload:",
      int(after.max()))

print("Median bucket workload:",
      float(after.median()))

print("Mean bucket workload:",
      round(float(after.mean()), 2))


print("\nLARGEST REMAINING BUCKETS")

for bucket, workload in after.head(15).items():

    print(
        f"{bucket}: "
        f"notices={bucket_counts[bucket]}, "
        f"comparisons={workload}"
    )


# ---------------------------------------------------------
# REDUCTION
# ---------------------------------------------------------

reduction = (
    1 - after.sum() / before.sum()
) * 100

print("\nWORKLOAD REDUCTION")
print("=" * 60)

print("Before:", int(before.sum()))
print("After:", int(after.sum()))
print("Reduction:", round(reduction, 2), "%")

print("\nDONE")