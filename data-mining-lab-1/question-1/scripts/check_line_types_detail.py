import duckdb

con = duckdb.connect("annapurna.duckdb")

result = con.execute("""
    SELECT
        line_type,
        COUNT(*) AS total_rows,
        COUNT(product_code) AS rows_with_product,
        COUNT(*) - COUNT(product_code) AS rows_without_product
    FROM sales_clean
    GROUP BY line_type
    ORDER BY line_type
""").fetchdf()

print(result.to_string(index=False))

con.close()