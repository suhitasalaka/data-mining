import duckdb
import psycopg2
from psycopg2.extras import execute_values

DUCKDB_PATH = "annapurna.duckdb"

# --------------------------------------------------
# 1. Connect to DuckDB
# --------------------------------------------------

duck = duckdb.connect(DUCKDB_PATH)

duck.execute("INSTALL postgres")
duck.execute("LOAD postgres")

duck.execute("""
    ATTACH 'dbname=annapurna host=localhost port=5432 user=postgres password=postgres'
    AS postgres_db (TYPE POSTGRES, READ_ONLY)
""")

print("Reading and matching sales in DuckDB...")

matched_sales = duck.execute("""
    SELECT
        s.bill_no,
        s.line_no,
        s.store AS store_id,
        p.product_sk,
        s.business_date,
        s.qty,
        s.unit_price,
        s.line_type,
        s.timestamp,
        s.source_file
    FROM sales_clean s
    LEFT JOIN postgres_db.public.products p
        ON s.product_code = p.product_code
        AND s.business_date >= p.valid_from
        AND s.business_date <= p.valid_to
""").fetchall()

print("Rows prepared:", len(matched_sales))

duck.close()

# --------------------------------------------------
# 2. Connect to PostgreSQL
# --------------------------------------------------

pg = psycopg2.connect(
    host="localhost",
    port=5432,
    database="annapurna",
    user="postgres",
    password="postgres"
)

cur = pg.cursor()

# Clear previous attempt
cur.execute("DELETE FROM fact_sales")

# --------------------------------------------------
# 3. Insert in batches
# --------------------------------------------------

insert_sql = """
INSERT INTO fact_sales (
    bill_no,
    line_no,
    store_id,
    product_sk,
    business_date,
    qty,
    unit_price,
    line_type,
    timestamp,
    source_file
)
VALUES %s
"""

batch_size = 10000
inserted = 0
unmatched = 0

for start in range(0, len(matched_sales), batch_size):

    batch = matched_sales[start:start + batch_size]

    valid_rows = []

    for row in batch:
        if row[3] is None:
            unmatched += 1
        else:
            valid_rows.append(row)

    if valid_rows:
        execute_values(
            cur,
            insert_sql,
            valid_rows,
            page_size=1000
        )

        inserted += len(valid_rows)

    print(
        f"Processed: "
        f"{min(start + batch_size, len(matched_sales))}"
        f"/{len(matched_sales)}"
    )

pg.commit()

# --------------------------------------------------
# 4. Verify
# --------------------------------------------------

cur.execute("SELECT COUNT(*) FROM fact_sales")
final_count = cur.fetchone()[0]

print()
print("========== FACT LOAD COMPLETE ==========")
print("Inserted:", inserted)
print("Unmatched:", unmatched)
print("PostgreSQL fact_sales rows:", final_count)
print("=========================================")

cur.close()
pg.close()