import duckdb

# --------------------------------------------------
# CONNECT TO DUCKDB
# --------------------------------------------------

con = duckdb.connect()

# --------------------------------------------------
# LOAD EXTENSIONS
# --------------------------------------------------

con.execute("INSTALL httpfs")
con.execute("LOAD httpfs")

con.execute("INSTALL postgres")
con.execute("LOAD postgres")

# --------------------------------------------------
# CONNECT TO MINIO
# --------------------------------------------------

con.execute("""
    SET s3_endpoint='localhost:9000';
    SET s3_access_key_id='minioadmin';
    SET s3_secret_access_key='minioadmin123';
    SET s3_use_ssl=false;
    SET s3_url_style='path';
""")

# --------------------------------------------------
# CONNECT TO POSTGRESQL
# --------------------------------------------------

con.execute("""
    ATTACH
    'dbname=annapurna host=localhost port=5432 user=postgres password=postgres'
    AS postgres_db
    (TYPE POSTGRES, READ_ONLY)
""")

# --------------------------------------------------
# CROSS-SYSTEM QUERY
#
# Sales -> MinIO
# Stores -> PostgreSQL
# Products -> PostgreSQL
# Categories -> PostgreSQL
#
# DuckDB performs the JOIN
# --------------------------------------------------

query = """
WITH raw_sales AS (

    SELECT
        bill_no,
        line_no,
        product_code,
        qty,
        unit_price,
        line_type,
        filename

    FROM read_csv_auto(
        's3://annapurna/sales/store=S01/year=2024/month=10/*.csv',
        filename=true,
        union_by_name=true
    )
),

sales_normalized AS (

    SELECT
        bill_no,
        line_no,
        product_code,
        qty,
        unit_price,
        line_type,

        'S01' AS store_id,

        CAST(
            regexp_extract(
                filename,
                'SALES_[^_]+_([0-9]{4})([0-9]{2})([0-9]{2})',
                1
            )
            || '-' ||
            regexp_extract(
                filename,
                'SALES_[^_]+_([0-9]{4})([0-9]{2})([0-9]{2})',
                2
            )
            || '-' ||
            regexp_extract(
                filename,
                'SALES_[^_]+_([0-9]{4})([0-9]{2})([0-9]{2})',
                3
            )
            AS DATE
        ) AS business_date

    FROM raw_sales
)

SELECT
    st.store_id,
    st.store_name,
    pc.category_name,
    COUNT(*) AS sale_lines,
    SUM(s.qty * s.unit_price) AS revenue

FROM sales_normalized s

JOIN postgres_db.public.stores st
    ON s.store_id = st.store_id

JOIN postgres_db.public.products p
    ON s.product_code = p.product_code
    AND s.business_date >= p.valid_from
    AND s.business_date <= p.valid_to

JOIN postgres_db.public.product_categories pc
    ON p.category_id = pc.category_id

WHERE s.line_type = 'SALE'

GROUP BY
    st.store_id,
    st.store_name,
    pc.category_name

ORDER BY revenue DESC

LIMIT 10
"""

# --------------------------------------------------
# RUN CROSS-SYSTEM QUERY
# --------------------------------------------------

print("========== CROSS-SYSTEM QUERY ==========")

try:

    result = con.execute(query).fetchdf()

    print(result.to_string(index=False))

except Exception as e:

    print("Cross-system query failed:")
    print(e)

    con.close()
    raise


# --------------------------------------------------
# QUERY PLAN
# --------------------------------------------------

print()
print("========== QUERY PLAN ==========")

try:

    plan = con.execute(
        "EXPLAIN " + query
    ).fetchall()

    for row in plan:
        print(row[1])

except Exception as e:

    print("EXPLAIN could not be completed.")
    print("The cross-system query itself was successful.")
    print("EXPLAIN reason:")
    print(e)


# --------------------------------------------------
# FINISH
# --------------------------------------------------

con.close()

print()
print("========== Q1(e) COMPLETE ==========")
print("Sales source: MinIO")
print("Stores source: PostgreSQL")
print("Products source: PostgreSQL")
print("Categories source: PostgreSQL")
print("Join engine: DuckDB")