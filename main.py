import os
import sys

# This adds the current folder to the Python Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from agent.cot_grader import CoTGrader
from agent.evaluator_opt import EvaluatorOptimizer

def run_benchmark():
    # 1. Load your dataset
    try:
        with open('benchmark/benchmark.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: benchmark.json not found in benchmark/ folder!")
        return

    #grader = CoTGrader()
    grader = EvaluatorOptimizer()
    
    # 2. Loop through each level
    for level in data['levels']:
        print(f"\n" + "="*50)
        print(f"GRADING LEVEL: {level['title']}")
        print("="*50)
        
        # 3. Grade each sample answer in that level
        for sample in level['sample_answers']:
            print(f"\n[Testing Sample: {sample['label']}]")
            
            result = grader.grade(level, sample['code'])
            
            # Print the Comparison
            print(f"  > Human Score:  {sample['score']}")
            print(f"  > AI Score:     {result.get('final_score')}")
            print(f"  > Logic Score:  {result.get('score_breakdown', {}).get('logic', 'N/A')}")
            print(f"  > Syntax Score: {result.get('score_breakdown', {}).get('syntax', 'N/A')}")
            print(f"  > AI Feedback:  {result.get('feedback')}")
            print("-" * 30)

if __name__ == "__main__":
    run_benchmark()