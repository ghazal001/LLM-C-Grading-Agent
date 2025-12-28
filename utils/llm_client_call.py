from utils.llm_client import LLMClient

def test():
    client = LLMClient()
    system = "You are a helpful assistant. Respond only in JSON."
    user = "Say hello and confirm you are ready to grade C++."
    
    print("Testing LLM Connection...")
    result = client.call(system, user)
    print("Response from AI:", result)

if __name__ == "__main__":
    test()