## Part 1 – Preprocessing + EDA

### Data
Place raw files locally (not pushed to git):
- data/raw/fashion_products_dataset.json
- data/raw/validation_labels.csv

### Run preprocessing
python scripts/prepare_part1.py --in data/raw/fashion_products_dataset.json --out data/processed/products_clean.parquet

### (Optional) Validate
python scripts/checking_correctness.py
# Expected: 28,080 rows, 0 missing PIDs vs validation_labels.csv

### Run EDA
python scripts/eda_part1.py

### Outputs
- data/processed/products_clean.parquet
- project_progress/part_1/fig_price_hist.png
- project_progress/part_1/fig_discount_hist.png
- project_progress/part_1/fig_rating_hist.png
- project_progress/part_1/top_brands.csv
- project_progress/part_1/top_terms_title.csv
- project_progress/part_1/summary.json
