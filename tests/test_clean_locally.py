from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "lambda"))

from handler import clean_transactions

raw_path = PROJECT_ROOT / "sample_data" / "transactions_sample.csv"
processed_path = PROJECT_ROOT / "sample_data" / "processed_sample.csv"

raw = pd.read_csv(raw_path)
cleaned = clean_transactions(raw)
cleaned.to_csv(processed_path, index=False)

print("Raw rows:", len(raw))
print("Cleaned rows:", len(cleaned))
print(cleaned.head())