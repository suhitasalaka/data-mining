import psycopg2
import time
import hashlib
import numpy as np

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="annapurna",
    user="postgres", password="postgres"
)

cur = conn.cursor()

# ---------------------------------------------------------
# Create deterministic sample LSH records
# ---------------------------------------------------------

print("Preparing LSH records...")

cur.execute("TRUNCATE TABLE notice_lsh;")

# 12,000 notices × 16 bands
# We use deterministic hashes so the same notice always
# produces the same LSH bucket.
records = []

for i in range(1, 12001):

    notice_id = f"N{i:06d}"

    for band in range(16):

        key = f"{notice_id}_{band}"
        digest = hashlib.sha256(key.encode()).digest()

        # Keep value inside PostgreSQL BIGINT range
        value = int.from_bytes(digest[:8], "big", signed=False)
        band_hash = value % 9223372036854775807

        records.append((notice_id, band, band_hash))

    if i % 1000 == 0:
        print("Prepared:", i, "/ 12000")

# Insert
print("Inserting records...")

cur.executemany(
    """
    INSERT INTO notice_lsh
    (notice_id, band_no, band_hash)
    VALUES (%s, %s, %s)
    """,
    records
)

conn.commit()

print("Rows inserted:", len(records))

# Update statistics
cur.execute("ANALYZE notice_lsh;")
conn.commit()

# ---------------------------------------------------------
# Indexed retrieval
# ---------------------------------------------------------

print("\nINDEXED RETRIEVAL")
print("=" * 60)

test_notice = "N010018"
test_band = 5

cur.execute(
    """
    SELECT band_hash
    FROM notice_lsh
    WHERE notice_id = %s AND band_no = %s
    """,
    (test_notice, test_band)
)

band_hash = cur.fetchone()[0]

query = """
SELECT notice_id
FROM notice_lsh
WHERE band_no = %s
AND band_hash = %s
"""

# EXPLAIN ANALYZE
cur.execute(
    "EXPLAIN (ANALYZE, BUFFERS) " + query,
    (test_band, band_hash)
)

plan = cur.fetchall()

for row in plan:
    print(row[0])

# Wall clock
start = time.perf_counter()

cur.execute(query, (test_band, band_hash))
rows = cur.fetchall()

elapsed = time.perf_counter() - start

print("\nIndexed query results:", len(rows))
print("Indexed wall-clock time:", round(elapsed * 1000, 4), "ms")

# ---------------------------------------------------------
# Forced sequential scan
# ---------------------------------------------------------

print("\nFORCED SEQUENTIAL SCAN")
print("=" * 60)

cur.execute("SET enable_indexscan = off;")
cur.execute("SET enable_bitmapscan = off;")

cur.execute(
    "EXPLAIN (ANALYZE, BUFFERS) " + query,
    (test_band, band_hash)
)

plan_seq = cur.fetchall()

for row in plan_seq:
    print(row[0])

start = time.perf_counter()

cur.execute(query, (test_band, band_hash))
rows_seq = cur.fetchall()

elapsed_seq = time.perf_counter() - start

print("\nSequential query results:", len(rows_seq))
print("Sequential wall-clock time:", round(elapsed_seq * 1000, 4), "ms")

# ---------------------------------------------------------
# Restore planner settings
# ---------------------------------------------------------

cur.execute("RESET enable_indexscan;")
cur.execute("RESET enable_bitmapscan;")

conn.commit()

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

print("\nSUMMARY")
print("=" * 60)
print("Total notices:", 12000)
print("Bands per notice:", 16)
print("Total LSH rows:", len(records))
print("Indexed time (ms):", round(elapsed * 1000, 4))
print("Sequential time (ms):", round(elapsed_seq * 1000, 4))

if elapsed > 0:
    print(
        "Speedup:",
        round(elapsed_seq / elapsed, 2),
        "x"
    )

cur.close()
conn.close()

print("\nDONE")
