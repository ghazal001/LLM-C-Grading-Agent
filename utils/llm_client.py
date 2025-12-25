import os
from openai import OpenAI  # We still use the OpenAI library!
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

    def call(self, system_prompt, user_prompt):
        """Sends a request to the LLM and returns the JSON response."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0,
                response_format={"type": "json_object"} 
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"