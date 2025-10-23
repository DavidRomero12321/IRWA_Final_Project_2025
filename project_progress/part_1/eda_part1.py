import json, os
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

INP = "data/processed/products_clean.parquet"
OUTDIR = "project_progress/part_1"
os.makedirs(OUTDIR, exist_ok=True)

df = pd.read_parquet(INP)

summary = {
    "docs": int(len(df)),
    "brands": int(df["brand"].nunique()),
    "categories": int(df["category"].nunique()),
    "avg_price": float(df["selling_price"].dropna().mean()) if "selling_price" in df else None,
    "avg_discount_frac": float(df["discount_frac"].dropna().mean()) if "discount_frac" in df else None,
    "avg_rating": float(df["average_rating"].dropna().mean()) if "average_rating" in df else None,
    "out_of_stock_pct": float(100 * df["out_of_stock"].mean()),
}
print(summary)
with open(os.path.join(OUTDIR, "summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

# Top brands
top_brands = df["brand"].value_counts().head(20).rename_axis("brand").reset_index(name="count")
top_brands.to_csv(os.path.join(OUTDIR, "top_brands.csv"), index=False)
print(top_brands.head(10))

# Token frequencies
v_title = Counter(t for ts in df["title_tokens"] for t in ts)
v_desc  = Counter(t for ts in df["desc_tokens"]  for t in ts)
pd.DataFrame(v_title.most_common(50), columns=["term","freq"]).to_csv(os.path.join(OUTDIR,"top_terms_title.csv"), index=False)
pd.DataFrame(v_desc.most_common(50),  columns=["term","freq"]).to_csv(os.path.join(OUTDIR,"top_terms_desc.csv"),  index=False)

# Plots (saved as PNGs)
ax = df["selling_price"].dropna().plot(kind="hist", bins=40, title="Selling Price Distribution")
ax.set_xlabel("price")
plt.tight_layout(); plt.savefig(os.path.join(OUTDIR, "fig_price_hist.png")); plt.clf()

if "discount_frac" in df:
    ax = df["discount_frac"].dropna().plot(kind="hist", bins=40, title="Discount Fraction Distribution")
    ax.set_xlabel("discount (0-1)")
    plt.tight_layout(); plt.savefig(os.path.join(OUTDIR, "fig_discount_hist.png")); plt.clf()

if "average_rating" in df:
    ax = df["average_rating"].dropna().plot(kind="hist", bins=20, title="Average Rating Distribution")
    ax.set_xlabel("rating")
    plt.tight_layout(); plt.savefig(os.path.join(OUTDIR, "fig_rating_hist.png")); plt.clf()
