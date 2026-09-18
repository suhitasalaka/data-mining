import pandas as pd
import glob
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# LOAD ALL NOTICES
# --------------------------------------------------

files = glob.glob("notices/*.csv")

df = pd.concat(
    [pd.read_csv(f) for f in files],
    ignore_index=True
)

print("Total notices:", len(df))


# --------------------------------------------------
# GET THE FOUR LABELLED EXAMPLES
# --------------------------------------------------

ids = [
    "N010018",
    "N010020",
    "N007876",
    "N008565"
]

notices = df[df["notice_id"].isin(ids)].copy()

notice_text = {}

for _, row in notices.iterrows():
    notice_text[row["notice_id"]] = (
        str(row["title"]) + " " + str(row["body"])
    )


# --------------------------------------------------
# PREPROCESSING
# --------------------------------------------------

def normalize_text(text):
    text = text.lower()

    # Remove reference-number-like patterns
    text = re.sub(
        r'\b(?:npas|spc|pwd|ref|mc|tn)[-/a-z0-9]*\b',
        ' ',
        text
    )

    # Remove long numeric/reference tokens
    text = re.sub(r'\b\d{5,}\b', ' ', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# --------------------------------------------------
# FOUR TEXT VERSIONS
# --------------------------------------------------

texts_raw = [
    notice_text["N010018"],
    notice_text["N010020"],
    notice_text["N007876"],
    notice_text["N008565"]
]

texts_normalized = [
    normalize_text(x)
    for x in texts_raw
]


# --------------------------------------------------
# FUNCTION TO PRINT PAIR SCORES
# --------------------------------------------------

def run_experiment(name, texts, analyzer, ngram_range):

    vectorizer = TfidfVectorizer(
        analyzer=analyzer,
        ngram_range=ngram_range,
        min_df=1
    )

    matrix = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(matrix)

    same_score = similarity[0, 1]
    different_score = similarity[2, 3]

    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    print("Features:", matrix.shape[1])

    print(
        "Same pair N010018-N010020:",
        round(same_score, 4)
    )

    print(
        "Different pair N007876-N008565:",
        round(different_score, 4)
    )

    print(
        "Separation:",
        round(same_score - different_score, 4)
    )


# --------------------------------------------------
# EXPERIMENT 1
# WORD TF-IDF — RAW
# --------------------------------------------------

run_experiment(
    "WORD TF-IDF — RAW",
    texts_raw,
    analyzer="word",
    ngram_range=(1, 1)
)


# --------------------------------------------------
# EXPERIMENT 2
# WORD TF-IDF — NORMALIZED
# --------------------------------------------------

run_experiment(
    "WORD TF-IDF — NORMALIZED",
    texts_normalized,
    analyzer="word",
    ngram_range=(1, 1)
)


# --------------------------------------------------
# EXPERIMENT 3
# CHARACTER TF-IDF — RAW
# --------------------------------------------------

run_experiment(
    "CHARACTER TF-IDF — RAW",
    texts_raw,
    analyzer="char",
    ngram_range=(3, 5)
)


# --------------------------------------------------
# EXPERIMENT 4
# CHARACTER TF-IDF — NORMALIZED
# --------------------------------------------------

run_experiment(
    "CHARACTER TF-IDF — NORMALIZED",
    texts_normalized,
    analyzer="char",
    ngram_range=(3, 5)
)