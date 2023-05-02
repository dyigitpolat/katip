openai_api_key = input("Enter your OpenAI API key: _")
open("src/api_keys.py", "w").write(f"openai_api_key = \"{openai_api_key}\"")