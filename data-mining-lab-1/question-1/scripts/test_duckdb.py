import duckdb

con = duckdb.connect()

# Load the extensions needed for S3/MinIO
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

# Configure MinIO
con.execute("""
    SET s3_endpoint='localhost:9000';
    SET s3_access_key_id='minioadmin';
    SET s3_secret_access_key='minioadmin123';
    SET s3_use_ssl=false;
    SET s3_url_style='path';
""")

print("DuckDB connected to MinIO successfully!")

# Check the S01 October partition
result = con.execute("""
    SELECT COUNT(*) AS row_count
    FROM read_csv_auto(
        's3://annapurna/sales/store=S01/year=2024/month=10/*.csv'
    );
""").fetchone()

print("Rows in S01 October:", result[0])