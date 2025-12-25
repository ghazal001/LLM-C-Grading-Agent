import statistics
from agent.base import BaseGrader
from agent.cot_grader import CoTGrader
from agent.few_cot_grader import FewShotCoTGrader


class VotingGrader:
    def __init__(self, strategy="median"):
        self.strategy = strategy

    def aggregate(self, results):
        valid = [r for r in results if isinstance(r, dict) and "final_score" in r]

        if not valid:
            return {
                "analysis": f"Voting failed. No valid grader outputs.",
                "final_score": None,
                "feedback": "All graders failed."
            }

        scores = [r["final_score"] for r in valid]

        if self.strategy == "mean":
            final = round(sum(scores) / len(scores))
        elif self.strategy == "median":
            final = int(statistics.median(scores))
        elif self.strategy == "majority":
            final = max(set(scores), key=scores.count)
        else:
            raise ValueError("Unknown strategy")

        return {
            "analysis": f"Voting using {self.strategy} over {len(valid)} graders",
            "individual_scores": scores,
            "final_score": final,
            "feedback": "Final score from voting aggregation."
        }
