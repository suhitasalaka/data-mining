from pathlib import Path
import re
import pandas as pd
import duckdb


# ==========================================
# CONFIGURATION
# ==========================================

SALES_DIR = Path("data/sales")
DB_PATH = "annapurna.duckdb"


# ==========================================
# READ AND NORMALIZE ONE SALES FILE
# ==========================================

def read_sales_file(path):

    name = path.name

    # --------------------------------------
    # Read CSV
    # --------------------------------------

    if path.suffix.lower() == ".csv":

        df = pd.read_csv(path)

        # S06-S09 use semicolon delimiter.
        # If comma parsing produced only one column,
        # read the file again using semicolon.
        if len(df.columns) == 1:
            df = pd.read_csv(path, sep=";")

    # --------------------------------------
    # Read Parquet if present
    # --------------------------------------

    elif path.suffix.lower() == ".parquet":

        df = pd.read_parquet(path)

    else:

        raise ValueError(
            f"Unsupported file: {name}"
        )


    # ======================================
    # NORMALIZE COLUMN NAMES
    # ======================================

    rename_map = {

        "item_code": "product_code",

        "quantity": "qty",

        "rate": "unit_price",

        "type": "line_type",

        "txn_time": "timestamp",

        "ts": "timestamp",
    }

    df = df.rename(
        columns=rename_map
    )


    # ======================================
    # NORMALIZE TIMESTAMP
    # ======================================

    # S10-S12 contain Unix epoch timestamps.

    if name.startswith(
        ("SALES_S10_", "SALES_S11_", "SALES_S12_")
    ):

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            unit="s"
        )

    else:

        # S01-S05 use ISO timestamps.
        # S06-S09 use DD-MM-YYYY HH:MM:SS.
        # format="mixed" lets pandas handle both.

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            format="mixed",
            dayfirst=True
        )


    # ======================================
    # EXTRACT STORE + BUSINESS DATE
    # ======================================

    match = re.search(
        r"SALES_(S\d+)_(\d{4})(\d{2})(\d{2})",
        name
    )

    if not match:

        raise ValueError(
            f"Cannot extract store/date from: {name}"
        )

    store, year, month, day = match.groups()


    # Store comes from the filename.

    df["store"] = store


    # IMPORTANT:
    # Business date comes from the filename,
    # NOT from the transaction timestamp.

    df["business_date"] = pd.Timestamp(
        f"{year}-{month}-{day}"
    ).date()


    # Keep the original source filename
    # for audit/debugging.

    df["source_file"] = name


    # ======================================
    # RETURN COMMON SCHEMA
    # ======================================

    return df[
        [
            "bill_no",
            "line_no",
            "product_code",
            "qty",
            "unit_price",
            "line_type",
            "timestamp",
            "store",
            "business_date",
            "source_file",
        ]
    ]


# ==========================================
# READ ALL SALES FILES
# ==========================================

frames = []

files = sorted(
    p
    for p in SALES_DIR.iterdir()
    if p.is_file()
)


print(
    "Source files:",
    len(files)
)


for i, path in enumerate(
    files,
    start=1
):

    print(
        f"Reading {i}/{len(files)}: {path.name}"
    )

    df = read_sales_file(path)

    frames.append(df)


# Combine every file into one dataframe.

all_sales = pd.concat(
    frames,
    ignore_index=True
)


print()

print(
    "Rows before deduplication:",
    len(all_sales)
)


# ==========================================
# DEDUPLICATION
# ==========================================

# Sort deterministically.

all_sales = all_sales.sort_values(
    [
        "bill_no",
        "line_no",
        "source_file"
    ]
)


# A billing line is identified by:
#
#       bill_no + line_no
#
# This prevents resend files from creating
# duplicate billing lines.

deduped = all_sales.drop_duplicates(
    subset=[
        "bill_no",
        "line_no"
    ],
    keep="last"
)


print(
    "Rows after deduplication:",
    len(deduped)
)


# ==========================================
# CREATE DUCKDB DATABASE
# ==========================================

con = duckdb.connect(
    DB_PATH
)


# ==========================================
# CREATE FINAL SALES TABLE
# ==========================================

con.execute(
    """
    CREATE TABLE IF NOT EXISTS sales_clean (

        bill_no VARCHAR,

        line_no INTEGER,

        product_code VARCHAR,

        qty DOUBLE,

        unit_price DOUBLE,

        line_type VARCHAR,

        timestamp TIMESTAMP,

        store VARCHAR,

        business_date DATE,

        source_file VARCHAR
    )
    """
)


# ==========================================
# IDEMPOTENT LOAD
# ==========================================

# Delete the previous result first.
#
# This means running the entire pipeline again
# produces the same table rather than appending
# another copy of the data.

con.execute(
    "DELETE FROM sales_clean"
)


# Give DuckDB access to the pandas dataframe.

con.register(
    "deduped_df",
    deduped
)


# Insert the clean data.

con.execute(
    """
    INSERT INTO sales_clean

    SELECT
        bill_no,
        line_no,
        product_code,
        qty,
        unit_price,
        line_type,
        timestamp,
        store,
        business_date,
        source_file

    FROM deduped_df
    """
)


# ==========================================
# ROW COUNT
# ==========================================

row_count = con.execute(
    """
    SELECT COUNT(*)
    FROM sales_clean
    """
).fetchone()[0]


# ==========================================
# DETERMINISTIC CHECKSUM
# ==========================================

checksum = con.execute(
    """
    SELECT
        md5(
            string_agg(
                concat_ws(
                    '|',

                    bill_no,

                    CAST(line_no AS VARCHAR),

                    product_code,

                    CAST(qty AS VARCHAR),

                    CAST(unit_price AS VARCHAR),

                    line_type,

                    CAST(timestamp AS VARCHAR),

                    store,

                    CAST(business_date AS VARCHAR)
                ),

                '||'

                ORDER BY
                    bill_no,
                    line_no
            )
        )

    FROM sales_clean
    """
).fetchone()[0]


# ==========================================
# FINAL RESULT
# ==========================================

print()

print(
    "========== LOAD COMPLETE =========="
)

print(
    "Final row count:",
    row_count
)

print(
    "Checksum:",
    checksum
)

print(
    "===================================="
)


con.close()