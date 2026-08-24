import boto3
import pandas as pd
from io import StringIO
from urllib.parse import unquote_plus
import os


s3 = boto3.client("s3")

def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['date', 'amount'])
    df['category'] = df['category'].str.strip().str.lower()
    df['merchant'] = df['merchant'].str.strip()
    df = df.drop_duplicates()
    df['type'] = df['amount'].apply(lambda x: 'income' if x > 0 else 'expense')
    df = df.sort_values('date').reset_index(drop=True)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    return df

def lambda_handler(event, context):

    raw_bucket = event['Records'][0]['s3']['bucket']['name']
    raw_key = unquote_plus(event["Records"][0]["s3"]["object"]["key"])
    obj = s3.get_object(Bucket=raw_bucket, Key=raw_key)
    raw_df = pd.read_csv(obj['Body'])

    cleaned_df = clean_transactions(raw_df)


    PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET")
    if not PROCESSED_BUCKET:
        raise RuntimeError("Missing required environment variable: PROCESSED_BUCKET")

    
    processed_key = raw_key.replace(".csv", "_cleaned.csv")

    buffer = StringIO()
    cleaned_df.to_csv(buffer, index=False)
    s3.put_object(Bucket=PROCESSED_BUCKET, Key=processed_key, Body=buffer.getvalue())

    return {"statusCode": 200, "rows_processed": len(cleaned_df)}