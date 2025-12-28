import sys
from pathlib import Path
import json
import statistics
import time

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))


from agent.cot_grader import CoTGrader
from agent.few_cot_grader import FewShotCoTGrader
from agent.evaluator_opt import EvaluatorOptimizer
from agent.voting_grader import VotingGrader
from utils.benchmark_loader import load_benchmark


BENCHMARK_PATH = "benchmark/benchmark.json"
VOTING_STRATEGIES = ["mean", "median"]


# We will store the "Error" (Difference from Human) for every method
performance_tracker = {
    "CoT_ZeroShot": [],
    "FewShot_CoT": [],
    "Evaluator_Optimizer": [],
    "Voting_Mean": [],
    "Voting_Median": []
}

def calculate_error(ai_result, human_score):
    """Safely extracts score and calculates absolute difference."""
    try:
        if isinstance(ai_result, dict) and "final_score" in ai_result:
            ai_score = float(ai_result["final_score"])
            return abs(ai_score - human_score)
    except:
        pass
    return None

# --------------------------------------------------
# Main Experiment Runner
# --------------------------------------------------
def run_full_evaluation():
    print("🚀 Starting Full Benchmark Evaluation...")
    benchmark = load_benchmark(BENCHMARK_PATH)
    
    # Initialize Graders
    cot = CoTGrader()
    fewshot = FewShotCoTGrader()
    evaluator = EvaluatorOptimizer()

    total_samples = 0

    # Loop through every Difficulty Level
    for level in benchmark["levels"]:
        print(f"\n--- Testing Level: {level['id']} ---")
        
        # Loop through every Student Sample in that level
        for sample in level["sample_answers"]:
            total_samples += 1
            student_code = sample["code"]
            human_score = float(sample["human_score"])
            
            print(f"  > Processing Sample: {sample['id']}...", end="\r")

            # 1. Get AI Scores
            res_cot = cot.grade(level, student_code)
            time.sleep(1)
            res_fewshot = fewshot.grade(level, student_code)
            time.sleep(1)
            res_eval = evaluator.grade(level, student_code)
            

            # 2. Collect for Voting (include all 3 brain types)
            voting_inputs = [
                r for r in [res_cot, res_fewshot, res_eval]
                if isinstance(r, dict) and "final_score" in r
            ]

            # 3. Calculate Voting
            mean_voter = VotingGrader(strategy="mean")
            median_voter = VotingGrader(strategy="median")
            
            res_vote_mean = mean_voter.aggregate(voting_inputs)
            res_vote_median = median_voter.aggregate(voting_inputs)

            # 4. Calculate and Store Errors (Absolute Difference)
            performance_tracker["CoT_ZeroShot"].append(calculate_error(res_cot, human_score))
            performance_tracker["FewShot_CoT"].append(calculate_error(res_fewshot, human_score))
            performance_tracker["Evaluator_Optimizer"].append(calculate_error(res_eval, human_score))
            performance_tracker["Voting_Mean"].append(calculate_error(res_vote_mean, human_score))
            performance_tracker["Voting_Median"].append(calculate_error(res_vote_median, human_score))

    print(f"\n\n✅ Evaluation Complete. Processed {total_samples} samples.")
    print_report()

# --------------------------------------------------
# Final Report Generation
# --------------------------------------------------
def print_report():
    print("\n" + "="*50)
    print("📊 FINAL PERFORMANCE REPORT (Mean Absolute Error)")
    print("Lower is Better (0 = Perfect Match with Human)")
    print("="*50)

    best_method = ""
    lowest_error = 999

    for method, errors in performance_tracker.items():
        # Clean out None values
        clean_errors = [e for e in errors if e is not None]
        
        if clean_errors:
            avg_error = statistics.mean(clean_errors)
            print(f"{method:<25} : {avg_error:>6.2f} points avg. error")
            
            if avg_error < lowest_error:
                lowest_error = avg_error
                best_method = method
        else:
            print(f"{method:<25} : DATA ERROR (Failed to get scores)")

    print("="*50)
    print(f"🏆 WINNER: {best_method}")
    print(f"This is the method we should use for the final Web App.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_full_evaluation()