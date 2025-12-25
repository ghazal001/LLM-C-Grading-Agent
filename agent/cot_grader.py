from agent.base import BaseGrader
from utils.llm_client import LLMClient
from prompts.cot_templates import COT_SYSTEM_PROMPT
import json

class CoTGrader(BaseGrader):
    def __init__(self):
        self.client = LLMClient()

    def grade(self, problem_data, student_code):
        # 1. Prepare the prompt using the helper from base.py
        user_prompt = self.format_user_prompt(problem_data, student_code)
        
        # 2. Call the LLM with the CoT System Prompt
        response_json = self.client.call(COT_SYSTEM_PROMPT, user_prompt)
        
        # 3. Parse and return the result
        try:
            return json.loads(response_json)
        except:
            return {"error": "Failed to parse LLM response"}