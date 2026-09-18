from pathlib import Path
import re
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError


SALES_DIR = Path("data/sales")

MINIO_ENDPOINT = "http://localhost:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin123"
BUCKET = "annapurna"


s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)


pattern = re.compile(
    r"SALES_(S\d+)_(\d{4})(\d{2})(\d{2})(?:__R\d+)?\.(csv|parquet)$",
    re.IGNORECASE,
)


uploaded = 0
already_present = 0
skipped = 0


for file_path in sorted(SALES_DIR.iterdir()):

    if not file_path.is_file():
        continue

    match = pattern.match(file_path.name)

    if not match:
        print(f"SKIP: {file_path.name}")
        skipped += 1
        continue

    store, year, month, day, extension = match.groups()

    object_key = (
        f"sales/"
        f"store={store}/"
        f"year={year}/"
        f"month={month}/"
        f"{file_path.name}"
    )

    # Check whether this exact object already exists
    try:
        s3.head_object(
            Bucket=BUCKET,
            Key=object_key
        )

        print(f"EXISTS: {file_path.name}")
        already_present += 1

    except ClientError as e:

        error_code = e.response.get("Error", {}).get("Code")

        if error_code in ("404", "NoSuchKey", "NotFound"):

            print(f"UPLOAD: {file_path.name}")
            print(f"     -> {object_key}")

            s3.upload_file(
                str(file_path),
                BUCKET,
                object_key,
            )

            uploaded += 1

        else:
            raise


print()
print("========== LANDING COMPLETE ==========")
print(f"Uploaded        : {uploaded}")
print(f"Already present : {already_present}")
print(f"Skipped         : {skipped}")
print("=======================================")