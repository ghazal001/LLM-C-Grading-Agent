import json
from agent.base import BaseGrader
from utils.llm_client import LLMClient
from prompts.few_shot_cot_templates import FEW_SHOT_COT_SYSTEM_PROMPT


class FewShotCoTGrader(BaseGrader):
    """
    Few-Shot Chain-of-Thought Grader.
    This grader uses human-aligned examples to improve grading calibration
    and partial credit assignment.
    """

    def __init__(self):
        self.client = LLMClient()

    def grade(self, problem_data, student_code):
        """
        Grades a student submission using few-shot Chain-of-Thought prompting.
        """
        # 1. Prepare the user prompt using the shared formatter
        user_prompt = self.format_user_prompt(problem_data, student_code)

        # 2. Call the LLM with the Few-Shot CoT system prompt
        response = self.client.call(
            FEW_SHOT_COT_SYSTEM_PROMPT,
            user_prompt
        )

        # 3. Parse and return the JSON result
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse LLM response",
                "raw_response": response
            }
