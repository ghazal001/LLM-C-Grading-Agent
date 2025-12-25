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
from agent.voting_grader import VotingGrader
from utils.benchmark_loader import load_benchmark

# --------------------------------------------------
# Config
# --------------------------------------------------
BENCHMARK_PATH = "benchmark/benchmark.json"
VOTING_STRATEGIES = ["mean", "median", "majority"]


# --------------------------------------------------
# Pretty printer
# --------------------------------------------------
def pretty(title, obj):
    print(f"\n{title}")
    print(json.dumps(obj, indent=2, ensure_ascii=False))


# --------------------------------------------------
# Voting using cached results (NO LLM CALLS HERE)
# --------------------------------------------------
def run_voting_from_cached(results):
    voting_outputs = {}

    for strategy in VOTING_STRATEGIES:
        voter = VotingGrader(strategy=strategy)
        voting_outputs[strategy] = voter.aggregate(results)

    return voting_outputs


# --------------------------------------------------
# Run one benchmark case
# --------------------------------------------------
def run_case(level_id, sample_id):
    benchmark = load_benchmark(BENCHMARK_PATH)
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
    cot = CoTGrader()
    fewshot = FewShotCoTGrader()
    evaluator = EvaluatorOptimizer()

    # --------------------------------------------------
    # Run graders ONCE
    # --------------------------------------------------
    cot_result = cot.grade(level, student_code)
    fewshot_result = fewshot.grade(level, student_code)
    evaluator_result = evaluator.grade(level, student_code)

    # Collect only valid grading outputs for voting
    voting_inputs = [
        r for r in [cot_result, fewshot_result]
        if isinstance(r, dict) and "final_score" in r
    ]

    voting_results = run_voting_from_cached(voting_inputs)

    # --------------------------------------------------
    # Print results
    # --------------------------------------------------
    pretty("🧑‍🏫 CoT Grader (Zero-Shot)", cot_result)
    pretty("🧠 Few-Shot CoT Grader", fewshot_result)
    pretty("👨‍🏫 Evaluator (Sequential)", evaluator_result)

    for strategy, result in voting_results.items():
        pretty(f"🗳️ Voting Grader ({strategy.upper()})", result)

    print("\n📌 HUMAN RATIONALE:")
    print(sample["human_rationale"])


# --------------------------------------------------
# Run experiments
# --------------------------------------------------
if __name__ == "__main__":
    run_case("L1_VERY_EASY", "L1_S1")   # Integer division trap
    run_case("L2_EASY", "L2_S2")        # Factorial starts at 0
    run_case("L4_HARD", "L4_S3")        # Iterative Fibonacci violation
