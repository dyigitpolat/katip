import os

openai_api_key = os.environ.get("OPENAI_API_KEY")
semanticscholar_api_key = os.environ.get("SEMANTICSCHOLAR_API_KEY")
katip_token = os.environ.get("KATIP_TOKEN")

key_str = f"openai_api_key = \"{openai_api_key}\"\nkatip_token = \"{katip_token}\"\nss_api_key = \"{semanticscholar_api_key}\""

open("src/api_keys.py", "w").write(key_str)