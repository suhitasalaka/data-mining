import duckdb

con = duckdb.connect("annapurna.duckdb")

result = con.execute("""
    SELECT
        line_type,
        COUNT(*) AS rows,
        COUNT(*) FILTER (
            WHERE product_code IS NULL
        ) AS no_product_code
    FROM sales_clean
    GROUP BY line_type
    ORDER BY rows DESC
""").fetchdf()

print(result.to_string(index=False))

con.close()