import argparse, sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))  # add project root

from myapp.search.preprocess import preprocess_jsonl
