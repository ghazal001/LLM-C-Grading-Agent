import json
import re
from agent.base import BaseGrader
from utils.llm_client import LLMClient
from prompts.cot_templates import COT_SYSTEM_PROMPT, CRITIC_SYSTEM_PROMPT

class EvaluatorOptimizer(BaseGrader):
    def __init__(self):
        self.client = LLMClient()

    def _parse_json(self, text):
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            return json.loads(match.group(0)) if match else None
        except:
            return None

    def grade(self, problem_data, student_code):
        # STEP 1: Initial Grade (Junior TA)
        user_prompt = self.format_user_prompt(problem_data, student_code)
        initial_response_raw = self.client.call(COT_SYSTEM_PROMPT, user_prompt)
        initial_grade = self._parse_json(initial_response_raw)

        # STEP 2: Critique (Senior TA)
        critic_user_prompt = f"""
        --- ORIGINAL PROBLEM ---
        {user_prompt}
        
        --- JUNIOR TA GRADE ---
        {json.dumps(initial_grade)}
        
        Please review this grade for accuracy and fairness.
        """
        
        final_response_raw = self.client.call(CRITIC_SYSTEM_PROMPT, critic_user_prompt)
        final_grade = self._parse_json(final_response_raw)
        
        return final_grade or initial_grade # Fallback to initial if critic fails