# utils/benchmark_loader.py
import json
from pathlib import Path

def load_benchmark(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
