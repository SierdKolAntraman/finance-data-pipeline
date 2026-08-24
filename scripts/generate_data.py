import pandas as pd
import numpy as np
import os

np.random.seed(42)

N = 500
start_date = pd.Timestamp("2026-01-01")
end_date = pd.Timestamp("2026-08-24")

dates = np.random.choice(pd.date_range(start_date, end_date), N)

expense_categories = ["groceries", "rent", "transport", "entertainment", "utilities", "dining", "subscription", "shopping"]
expense_merchants = {
    "groceries": ["Tesco", "Lidl", "Aldi"],
    "rent": ["Landlord Ltd"],
    "transport": ["Dublin Bus", "Luas", "Irish Rail"],
    "entertainment": ["Cinema World", "Spotify"],
    "utilities": ["Electric Ireland", "Eir"],
    "dining": ["Starbucks", "Local Cafe"],
    "subscription": ["Netflix", "Spotify"],
    "shopping": ["Amazon", "Penneys"],
}

income_categories = ["salary", "freelance", "refund"]
income_merchants = {
    "salary": ["Employer Ltd"],
    "freelance": ["Client Payment"],
    "refund": ["Amazon", "Tesco"],
}

rows = []
for d in dates:
    is_income = np.random.rand() < 0.4
    if is_income:
        category = np.random.choice(income_categories)
        merchant = np.random.choice(income_merchants[category])
        amount = round(np.random.uniform(50, 2500), 2)
    else:
        category = np.random.choice(expense_categories)
        merchant = np.random.choice(expense_merchants[category])
        amount = -round(np.random.uniform(3, 300), 2)
    rows.append([pd.Timestamp(d).strftime("%Y-%m-%d"), amount, category, merchant])

df = pd.DataFrame(rows, columns=["date", "amount", "category", "merchant"])
df = df.sort_values("date").reset_index(drop=True)

#df.to_csv("transactions_sample.csv", index=False)

output_path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "transactions_sample.csv")
df.to_csv(output_path, index=False)

print(df.head())
print(df.shape)