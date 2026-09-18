import duckdb

con = duckdb.connect("annapurna.duckdb")

query = """
WITH void_bills AS (
    SELECT DISTINCT bill_no
    FROM sales_clean
    WHERE line_type = 'VOID'
),

valid_lines AS (
    SELECT
        s.*
    FROM sales_clean s
    LEFT JOIN void_bills v
        ON s.bill_no = v.bill_no
    WHERE v.bill_no IS NULL
),

monthly_revenue AS (
    SELECT
        strftime(business_date, '%Y-%m') AS month,

        ROUND(
            SUM(
                CASE
                    WHEN line_type = 'SALE'
                        THEN qty * unit_price

                    WHEN line_type = 'RETURN'
                        THEN qty * unit_price

                    WHEN line_type = 'DISCOUNT'
                        THEN qty * unit_price

                    ELSE 0
                END
            ),
            2
        ) AS calculated_revenue

    FROM valid_lines

    GROUP BY 1
),

finance AS (
    SELECT
        month,
        revenue_inr AS finance_revenue
    FROM read_csv_auto(
        'data/finance_monthly.csv'
    )
)

SELECT
    m.month,
    m.calculated_revenue,
    f.finance_revenue,

    ROUND(
        m.calculated_revenue - f.finance_revenue,
        2
    ) AS difference,

    ROUND(
        100.0 *
        (m.calculated_revenue - f.finance_revenue)
        / f.finance_revenue,
        2
    ) AS difference_percent

FROM monthly_revenue m

JOIN finance f
    ON m.month = f.month

ORDER BY m.month;
"""

print("========== FINAL RECONCILIATION ==========")

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()