import pandas as pd

df = pd.read_parquet("data/processed/products_clean.parquet")
print("Columns:", df.columns.tolist())
print("\nExample record:")
example = df.iloc[0].to_dict()
for k, v in example.items():
    print(f"{k:20}: {v}")
