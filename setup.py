openai_api_key = input("Enter your OpenAI API key: _")
semanticscholar_api_key = input("Enter your Semantic Scholar API key: _")
katip_token = input("Enter your Katip token: _")

key_str = f"openai_api_key = \"{openai_api_key}\"\nkatip_token = \"{katip_token}\"\nss_api_key = \"{semanticscholar_api_key}\""

open("src/api_keys.py", "w").write(key_str)