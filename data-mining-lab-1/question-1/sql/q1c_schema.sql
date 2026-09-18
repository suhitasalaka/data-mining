DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_category;
DROP TABLE IF EXISTS dim_store;


CREATE TABLE dim_store AS
SELECT
    store_id,
    store_name,
    address_line,
    city,
    state,
    region,
    floor_area_sqft,
    opened_on
FROM stores;

ALTER TABLE dim_store
ADD PRIMARY KEY (store_id);


CREATE TABLE dim_category AS
SELECT
    category_id,
    category_name,
    department,
    gst_rate
FROM product_categories;

ALTER TABLE dim_category
ADD PRIMARY KEY (category_id);


CREATE TABLE dim_product AS
SELECT
    product_sk,
    product_code,
    product_name,
    category_id,
    brand,
    pack_size,
    uom,
    valid_from,
    valid_to,
    is_current
FROM products;

ALTER TABLE dim_product
ADD PRIMARY KEY (product_sk);

ALTER TABLE dim_product
ADD CONSTRAINT fk_dim_product_category
FOREIGN KEY (category_id)
REFERENCES dim_category(category_id);


CREATE TABLE dim_date (
    date_key DATE PRIMARY KEY,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    day INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name TEXT NOT NULL
);


CREATE TABLE fact_sales (
    bill_no TEXT NOT NULL,
    line_no INTEGER NOT NULL,
    store_id TEXT NOT NULL,
    product_sk BIGINT NOT NULL,
    business_date DATE NOT NULL,
    qty DOUBLE PRECISION,
    unit_price NUMERIC(12,2),
    line_type TEXT NOT NULL,
    timestamp TIMESTAMP,
    source_file TEXT,

    PRIMARY KEY (bill_no, line_no),

    FOREIGN KEY (store_id)
        REFERENCES dim_store(store_id),

    FOREIGN KEY (product_sk)
        REFERENCES dim_product(product_sk),

    FOREIGN KEY (business_date)
        REFERENCES dim_date(date_key)
);


CREATE INDEX ix_fact_sales_store_date
    ON fact_sales(store_id, business_date);

CREATE INDEX ix_fact_sales_product_date
    ON fact_sales(product_sk, business_date);

CREATE INDEX ix_fact_sales_date
    ON fact_sales(business_date);