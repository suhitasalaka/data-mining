from pathlib import Path
import pandas as pd


sales_dir = Path("data/sales")

files = sorted(sales_dir.iterdir())

print("Total files:", len(files))
print()

# Inspect one file from each store
seen_stores = set()

for file_path in files:

    if not file_path.is_file():
        continue

    name = file_path.name

    if not name.startswith("SALES_"):
        continue

    parts = name.split("_")
    store = parts[1]

    if store in seen_stores:
        continue

    seen_stores.add(store)

    print("=" * 70)
    print("FILE:", file_path.name)
    print("STORE:", store)

    try:
        if file_path.suffix.lower() == ".parquet":
            df = pd.read_parquet(file_path)

        else:
            # Try comma first
            try:
                df = pd.read_csv(file_path)

                # If it looks like a single-column file, try semicolon
                if len(df.columns) == 1:
                    df = pd.read_csv(file_path, sep=";")

            except Exception:
                df = pd.read_csv(file_path, sep=";")

        print("Columns:")
        for column in df.columns:
            print("  ", column)

        print("Rows:", len(df))

        print("\nFirst 2 rows:")
        print(df.head(2).to_string(index=False))

    except Exception as e:
        print("ERROR:", e)

    print()

print("=" * 70)
print("Stores inspected:", sorted(seen_stores))