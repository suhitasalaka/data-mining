import os
import re
import glob
import numpy as np
import pandas as pd

DATA_DIR = r".\notices"
LABEL_FILE = r".\labelled_pairs.csv"

def normalize(text):
    text = str(text).lower()
    text = re.sub(r'\b(?:npas|spc|pwd|ref|mc|tn)[-/a-z0-9]*\b', ' ', text)
    text = re.sub(r'\b\d{5,}\b', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def shingles(text, k=5):
    return {text[i:i+k] for i in range(len(text)-k+1)}

print("Loading labelled pairs...")
pairs = pd.read_csv(LABEL_FILE)

ids = set(pairs["notice_id_a"]) | set(pairs["notice_id_b"])

frames = []
for f in glob.glob(os.path.join(DATA_DIR, "*.csv")):
    if os.path.basename(f) == "labelled_pairs.csv":
        continue
    df = pd.read_csv(f, low_memory=False)
    frames.append(df)

notices = pd.concat(frames, ignore_index=True)
notices = notices[notices["notice_id"].isin(ids)].copy()

print("Notices used:", len(notices))
print("Labelled pairs:", len(pairs))

# Create 5-character shingle sets
sets = {}
for _, r in notices.iterrows():
    text = normalize(str(r["title"]) + " " + str(r["body"]))
    sets[r["notice_id"]] = shingles(text)

# Exact Jaccard for every labelled pair
exact = []

for _, r in pairs.iterrows():
    a = sets[r["notice_id_a"]]
    b = sets[r["notice_id_b"]]

    union = len(a | b)
    inter = len(a & b)

    exact.append(inter / union if union else 0.0)

exact = np.array(exact)

print("\nEXACT JACCARD")
print("Mean:", round(exact.mean(), 6))
print("Median:", round(np.median(exact), 6))
print("Min:", round(exact.min(), 6))
print("Max:", round(exact.max(), 6))

# Fast MinHash-style estimator using random hash projections
# One 64-bit hash per shingle
all_shingles = set()
for s in sets.values():
    all_shingles.update(s)

print("\nUnique shingles:", len(all_shingles))

shingle_list = list(all_shingles)
shingle_to_int = {
    s: i + 1 for i, s in enumerate(shingle_list)
}

rng = np.random.default_rng(42)

# Large prime
P = 4294967311

A = rng.integers(1, P, size=256, dtype=np.uint64)
B = rng.integers(0, P, size=256, dtype=np.uint64)

signatures = {}

for idx, (notice_id, s) in enumerate(sets.items()):
    x = np.array([shingle_to_int[v] for v in s], dtype=np.uint64)

    # Process in chunks to stay fast and memory-safe
    sig = np.full(256, np.uint64(P))

    for start in range(0, len(x), 5000):
        xx = x[start:start+5000]
        h = (A[:, None] * xx[None, :] + B[:, None]) % P
        sig = np.minimum(sig, h.min(axis=1))

    signatures[notice_id] = sig

    if (idx + 1) % 300 == 0:
        print("Signatures:", idx + 1, "/", len(sets))

# Evaluate signature sizes
for size in [32, 64, 128, 256]:

    estimates = []

    for _, r in pairs.iterrows():
        sa = signatures[r["notice_id_a"]][:size]
        sb = signatures[r["notice_id_b"]][:size]

        estimates.append(np.mean(sa == sb))

    estimates = np.array(estimates)
    errors = estimates - exact
    abs_errors = np.abs(errors)

    print("\n" + "="*60)
    print("SIGNATURE SIZE:", size)
    print("="*60)

    print("Mean signed error:", round(errors.mean(), 6))
    print("Mean absolute error:", round(abs_errors.mean(), 6))
    print("Median absolute error:", round(np.median(abs_errors), 6))
    print("90th percentile absolute error:", round(np.quantile(abs_errors, .90), 6))
    print("95th percentile absolute error:", round(np.quantile(abs_errors, .95), 6))
    print("Maximum absolute error:", round(abs_errors.max(), 6))

    print("Within +/-0.05:",
          round(np.mean(abs_errors <= .05) * 100, 2), "%")

    print("Within +/-0.10:",
          round(np.mean(abs_errors <= .10) * 100, 2), "%")

print("\nDONE")
