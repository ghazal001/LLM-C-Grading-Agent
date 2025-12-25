import sys
from pathlib import Path
import json

# --------------------------------------------------
# Ensure project root is in PYTHONPATH
# --------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agent.cot_grader import CoTGrader
from agent.few_cot_grader import FewShotCoTGrader
from agent.evaluator_opt import EvaluatorOptimizer
from utils.benchmark_loader import load_benchmark

BENCHMARK_PATH = "benchmark/benchmark.json"


def pretty_print(title, data):
    print(f"\n{title}")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def run_experiment(level_id, sample_id):
    benchmark = load_benchmark(BENCHMARK_PATH)
    level = next(l for l in benchmark["levels"] if l["id"] == level_id)
    sample = next(s for s in level["sample_answers"] if s["id"] == sample_id)

    student_code = sample["code"]

    print("\n" + "=" * 80)
    print(f"LEVEL: {level_id}")
    print(f"SAMPLE: {sample_id} — {sample['label']}")
    print("=" * 80)

    cot = CoTGrader()
    fewshot = FewShotCoTGrader()
    evaluator = EvaluatorOptimizer()

    # -----------------------------
    # Run graders (ONLY ONCE)
    # -----------------------------
    cot_result = cot.grade(level, student_code)
    fewshot_result = fewshot.grade(level, student_code)
    evaluator_result = evaluator.grade(level, student_code)

    # -----------------------------
    # Clean printing
    # -----------------------------
    pretty_print("🧑‍🏫 CoT GRADER (Zero-Shot):", cot_result)
    pretty_print("🧠 FEW-SHOT CoT GRADER:", fewshot_result)
    pretty_print("👨‍🏫 EVALUATOR (Teacher / Critic):", evaluator_result)

    print("\n📌 HUMAN RATIONALE:")
    print(sample["human_rationale"])


if __name__ == "__main__":
    run_experiment("L1_VERY_EASY", "L1_S1")
    run_experiment("L2_EASY", "L2_S2")
    run_experiment("L4_HARD", "L4_S3")
