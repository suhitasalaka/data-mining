import os
import re
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

print("Loading data...")

pairs = pd.read_csv(LABEL_FILE)

frames = []
for f in glob.glob(os.path.join(DATA_DIR, "*.csv")):
    if os.path.basename(f) == "labelled_pairs.csv":
        continue
    frames.append(pd.read_csv(f, low_memory=False))

notices = pd.concat(frames, ignore_index=True)

# Only notices appearing in labelled pairs
ids = set(pairs["notice_id_a"]) | set(pairs["notice_id_b"])
notices = notices[notices["notice_id"].isin(ids)].copy()

sets = {}

for _, r in notices.iterrows():
    txt = normalize(str(r["title"]) + " " + str(r["body"]))
    sets[r["notice_id"]] = shingles(txt)

# Create 128 MinHash signatures
all_shingles = set()
for s in sets.values():
    all_shingles.update(s)

mapping = {s: i + 1 for i, s in enumerate(all_shingles)}

rng = np.random.default_rng(42)
P = 4294967311

A = rng.integers(1, P, size=128, dtype=np.uint64)
B = rng.integers(0, P, size=128, dtype=np.uint64)

signatures = {}

for notice_id, s in sets.items():

    x = np.array([mapping[v] for v in s], dtype=np.uint64)

    sig = np.full(128, np.uint64(P))

    for start in range(0, len(x), 5000):
        xx = x[start:start+5000]
        h = (A[:, None] * xx[None, :] + B[:, None]) % P
        sig = np.minimum(sig, h.min(axis=1))

    signatures[notice_id] = sig

print("Signatures created:", len(signatures))

# Exact Jaccard for labelled pairs
true_sim = []

for _, r in pairs.iterrows():

    a = sets[r["notice_id_a"]]
    b = sets[r["notice_id_b"]]

    true_sim.append(len(a & b) / len(a | b))

true_sim = np.array(true_sim)

# Test LSH configurations
configs = [
    (32, 4),
    (16, 8),
    (8, 16),
    (4, 32)
]

results = []

for bands, rows in configs:

    survivors = []

    for _, r in pairs.iterrows():

        sa = signatures[r["notice_id_a"]]
        sb = signatures[r["notice_id_b"]]

        found = False

        for band in range(bands):

            start = band * rows
            end = start + rows

            if np.array_equal(sa[start:end], sb[start:end]):
                found = True
                break

        survivors.append(found)

    survivors = np.array(survivors)

    results.append({
        "bands": bands,
        "rows_per_band": rows,
        "candidate_recall_all": survivors.mean(),
        "candidate_recall_same": survivors[pairs["label"].values == 1].mean(),
        "candidate_rate": survivors.mean()
    })

print("\nLSH RESULTS")
print("=" * 60)

for r in results:

    print(
        f"Bands={r['bands']:2d}, "
        f"Rows/band={r['rows_per_band']:2d}, "
        f"All-pair survival={r['candidate_recall_all']:.4f}, "
        f"Same-pair recall={r['candidate_recall_same']:.4f}"
    )

# Survival probability by true Jaccard bins
bins = np.arange(0.0, 1.01, 0.1)

chosen_bands = 16
chosen_rows = 8

survive = []

for _, r in pairs.iterrows():

    sa = signatures[r["notice_id_a"]]
    sb = signatures[r["notice_id_b"]]

    found = False

    for band in range(chosen_bands):

        start = band * chosen_rows
        end = start + chosen_rows

        if np.array_equal(sa[start:end], sb[start:end]):
            found = True
            break

    survive.append(found)

survive = np.array(survive)

print("\nSURVIVAL BY TRUE JACCARD")
print("=" * 60)

centers = []

for low in bins[:-1]:

    high = low + 0.1

    mask = (true_sim >= low) & (true_sim < high)

    if mask.sum() > 0:

        rate = survive[mask].mean()

        centers.append((low + 0.05, rate, mask.sum()))

        print(
            f"{low:.1f}-{high:.1f}: "
            f"survival={rate:.4f}, "
            f"pairs={mask.sum()}"
        )

plt.figure(figsize=(8, 5))

plt.plot(
    [x[0] for x in centers],
    [x[1] for x in centers],
    marker="o"
)

plt.xlabel("True Jaccard similarity")
plt.ylabel("Probability pair survives candidate stage")
plt.title("LSH Candidate Survival vs True Similarity")
plt.grid(True)

plt.savefig("lsh_survival_curve.png", dpi=150)

print("\nSaved plot: lsh_survival_curve.png")