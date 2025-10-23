import argparse, sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))  # add project root

from project_progress.part_1.preprocess import preprocess_jsonl
