import duckdb

con = duckdb.connect("annapurna.duckdb")

con.execute("INSTALL postgres")
con.execute("LOAD postgres")

con.execute("""
    ATTACH 'dbname=annapurna host=localhost port=5432 user=postgres password=postgres'
    AS postgres_db (TYPE POSTGRES, READ_ONLY)
""")

result = con.execute("""
    SELECT
        s.product_code,
        s.business_date,
        COUNT(*) AS rows
    FROM sales_clean s
    LEFT JOIN postgres_db.public.products p
        ON s.product_code = p.product_code
        AND s.business_date >= p.valid_from
        AND s.business_date < p.valid_to
    WHERE p.product_sk IS NULL
      AND s.line_type = 'SALE'
    GROUP BY s.product_code, s.business_date
    ORDER BY rows DESC
""").fetchdf()

print(result.to_string(index=False))

con.close()