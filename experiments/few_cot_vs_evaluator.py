import sys
from pathlib import Path
import json

# --------------------------------------------------
# Ensure project root is in PYTHONPATH
# --------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# --------------------------------------------------
# Imports
# --------------------------------------------------
from agent.cot_grader import CoTGrader
from agent.few_cot_grader import FewShotCoTGrader
from agent.evaluator_opt import EvaluatorOptimizer
from utils.benchmark_loader import load_benchmark

# --------------------------------------------------
# Config
# --------------------------------------------------
BENCHMARK_PATH = "benchmark/benchmark.json"


def run_experiment(level_id, sample_id):
    benchmark = load_benchmark(BENCHMARK_PATH)

    # Retrieve level and sample
    level = next(l for l in benchmark["levels"] if l["id"] == level_id)
    sample = next(s for s in level["sample_answers"] if s["id"] == sample_id)

    student_code = sample["code"]

    print("\n" + "=" * 80)
    print(f"LEVEL: {level_id}")
    print(f"SAMPLE: {sample_id} — {sample['label']}")
    print("=" * 80)

    # --------------------------------------------------
    # Initialize graders
    # --------------------------------------------------
    cot_grader = CoTGrader()
    fewshot_grader = FewShotCoTGrader()
    evaluator = EvaluatorOptimizer()

    # --------------------------------------------------
    # Run graders
    # --------------------------------------------------
    cot_result = cot_grader.grade(level, student_code)
    fewshot_result = fewshot_grader.grade(level, student_code)
    evaluator_result = evaluator.grade(level, student_code)

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------
    print("\n🧑‍🏫 CoT GRADER (Zero-Shot):")
    print(json.dumps(cot_result, indent=2))

    print("\n🧠 FEW-SHOT CoT GRADER:")
    print(json.dumps(fewshot_result, indent=2))

    print("\n👨‍🏫 EVALUATOR (Teacher / Critic):")
    print(json.dumps(evaluator_result, indent=2))

    print("\n📌 HUMAN RATIONALE:")
    print(sample["human_rationale"])


# --------------------------------------------------
# Run experiments
# --------------------------------------------------
if __name__ == "__main__":
    # Strong diagnostic cases
    run_experiment("L1_VERY_EASY", "L1_S1")   # Integer division trap
    run_experiment("L2_EASY", "L2_S2")        # Factorial starts at 0
    run_experiment("L4_HARD", "L4_S3")        # Iterative Fibonacci violation
