import boto3
import csv
import io
import os
from datetime import datetime
from urllib.parse import unquote_plus

s3 = boto3.client("s3")


def clean_transactions(rows):
    cleaned_rows = []
    seen_rows = set()

    for row in rows:
        try:
            date = datetime.strptime(row["date"].strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
            amount = float(row["amount"])
            category = row["category"].strip().lower()
            merchant = row["merchant"].strip()
        except (KeyError, ValueError, AttributeError):
            continue

        cleaned_row = (
            date,
            amount,
            category,
            merchant,
            "income" if amount > 0 else "expense",
        )

        if cleaned_row not in seen_rows:
            seen_rows.add(cleaned_row)
            cleaned_rows.append(cleaned_row)

    return sorted(cleaned_rows, key=lambda row: row[0])


def lambda_handler(event, context):
    processed_bucket = os.environ["PROCESSED_BUCKET"]

    for record in event["Records"]:
        raw_bucket = record["s3"]["bucket"]["name"]
        raw_key = unquote_plus(record["s3"]["object"]["key"])

        response = s3.get_object(Bucket=raw_bucket, Key=raw_key)
        text = response["Body"].read().decode("utf-8")
        rows = csv.DictReader(io.StringIO(text))

        cleaned_rows = clean_transactions(rows)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["date", "amount", "category", "merchant", "type"])
        writer.writerows(cleaned_rows)

        processed_key = raw_key.removesuffix(".csv") + "_cleaned.csv"

        s3.put_object(
            Bucket=processed_bucket,
            Key=processed_key,
            Body=output.getvalue().encode("utf-8"),
            ContentType="text/csv",
        )

    return {"statusCode": 200, "rows_processed": len(cleaned_rows)}