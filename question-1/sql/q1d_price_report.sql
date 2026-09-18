-- Q1(d): Revenue using the price revision
-- applicable during the reporting period.

SELECT
    DATE '2024-03-01' AS report_month,
    SUM(
        f.qty * r.selling_price
    ) AS revenue_using_applicable_price
FROM fact_sales f
JOIN price_revisions r
    ON f.product_sk = r.product_sk
    AND f.business_date >= r.effective_from
    AND f.business_date <= r.effective_to
WHERE f.line_type = 'SALE'
  AND f.business_date >= DATE '2024-03-01'
  AND f.business_date < DATE '2024-04-01';


-- Run the same query for another reporting month.
-- Only the reporting-period dates change.

SELECT
    DATE '2024-02-01' AS report_month,
    SUM(
        f.qty * r.selling_price
    ) AS revenue_using_applicable_price
FROM fact_sales f
JOIN price_revisions r
    ON f.product_sk = r.product_sk
    AND f.business_date >= r.effective_from
    AND f.business_date <= r.effective_to
WHERE f.line_type = 'SALE'
  AND f.business_date >= DATE '2024-02-01'
  AND f.business_date < DATE '2024-03-01';