from __future__ import annotations
import json, re, unicodedata, pathlib
import pandas as pd
from myapp.search.tokenize import build_terms
from myapp.search.load_corpus import load_corpus

def _norm(s: str) -> str:
    if not isinstance(s, str): return ""
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"[^\w\s]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def _num(x):
    s = str(x).replace(",", "")
    m = re.findall(r"\d+(?:\.\d+)?", s)
    return float(m[0]) if m else None

def _disc(x):
    m = re.search(r"(\d+(?:\.\d+)?)", str(x))
    return float(m.group(1))/100.0 if m else None

def _rating(x):
    try: return float(x)
    except: return None

def _details_tokens(lst):
    out=[]
    if isinstance(lst, list):
        for d in lst:
            if isinstance(d, dict):
                for k,v in d.items():
                    out += build_terms(str(k)) + build_terms(str(v))
    return out

def preprocess_row(doc: dict) -> dict:
    title = doc.get("title","")
    desc  = doc.get("description","")
    return {
        "pid": doc.get("pid"),
        "title_tokens": build_terms(title),
        "desc_tokens": build_terms(desc),
        "details_tokens": _details_tokens(doc.get("product_details", [])),
        "brand": _norm(doc.get("brand","")),
        "category": _norm(doc.get("category","")),
        "sub_category": _norm(doc.get("sub_category","")),
        "seller": _norm(doc.get("seller","")),
        "out_of_stock": bool(doc.get("out_of_stock", False)),
        "selling_price": _num(doc.get("selling_price")),
        "actual_price": _num(doc.get("actual_price")),
        "discount_frac": _disc(doc.get("discount")),
        "average_rating": _rating(doc.get("average_rating")),
        "title_raw": title,
        "description_raw": desc,
        "url": doc.get("url",""),
    }

def _iter_docs(path):
    with open(path, "r", encoding="utf-8") as f:
        # peek first non-space
        import itertools, json
        first = f.read(1024)
        while first and first[0].isspace():
            first = first[1:]
        f.seek(0)
        if first.startswith("["):            # JSON array
            data = json.load(f)
            for doc in data:
                yield doc
        else:                                # JSONL
            for line in f:
                line = line.strip()
                if line:
                    yield json.loads(line)

def preprocess_jsonl(input_path, output_parquet):
    rows = [preprocess_row(doc) for doc in _iter_docs(input_path)]
    df = pd.DataFrame(rows)
    pathlib.Path(output_parquet).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_parquet, index=False)
    return df

