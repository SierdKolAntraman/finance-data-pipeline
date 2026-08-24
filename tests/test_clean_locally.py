import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lambda"))
import pandas as pd
from handler import clean_transactions

raw = pd.read_csv("sample_data/transactions_sample.csv")
cleaned = clean_transactions(raw)
cleaned.to_csv("sample_data/processed_sample.csv", index=False)
print("Raw rows:", len(raw))
print("Cleaned rows:", len(cleaned))
print(cleaned.head())