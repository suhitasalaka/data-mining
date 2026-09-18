import duckdb

con = duckdb.connect()

con.execute("INSTALL postgres")
con.execute("LOAD postgres")

con.execute("""
    ATTACH 'dbname=annapurna host=localhost port=5432 user=postgres password=postgres'
    AS postgres_db (TYPE POSTGRES, READ_ONLY)
""")

count = con.execute("""
    SELECT COUNT(*)
    FROM postgres_db.public.products
""").fetchone()[0]

print("Products visible from DuckDB:", count)

con.close()