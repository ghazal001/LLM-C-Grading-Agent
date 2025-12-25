import sys
from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agent.cot_grader import CoTGrader
from agent.evaluator_opt import EvaluatorOptimizer
from utils.benchmark_loader import load_benchmark

BENCHMARK_PATH = "benchmark/benchmark.json"


def run(level_id, sample_id):
    benchmark = load_benchmark(BENCHMARK_PATH)

    level = next(l for l in benchmark["levels"] if l["id"] == level_id)
    sample = next(s for s in level["sample_answers"] if s["id"] == sample_id)

    student_code = sample["code"]

    print("\n" + "=" * 60)
    print(f"LEVEL: {level_id}")
    print(f"SAMPLE: {sample_id} — {sample['label']}")
    print("=" * 60)

    cot = CoTGrader()
    cot_result = cot.grade(level, student_code)

    print("\n🧑‍🏫 CoT GRADER (Junior TA):")
    print(json.dumps(cot_result, indent=2))

    evaluator = EvaluatorOptimizer()
    eval_result = evaluator.grade(level, student_code)

    print("\n👨‍🏫 EVALUATOR (Senior TA):")
    print(json.dumps(eval_result, indent=2))

    print("\n📌 HUMAN RATIONALE:")
    print(sample["human_rationale"])


if __name__ == "__main__":
    run("L1_VERY_EASY", "L1_S1")
    run("L2_EASY", "L2_S2")
    run("L4_HARD", "L4_S3")
