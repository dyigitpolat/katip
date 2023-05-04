from katip.llm_adapters.openai_client import OpenAIClient
from katip.prompting.basic_prompts import BasicPrompts
import json

class ProtocolHandler:
    max_tries = 3

    def _get_prefix(self, json_str: str, prefix_key):
        prefix_index = json_str.find(f"\"{prefix_key}\"")
        prefix_offset = len(f"\"{prefix_key}\"")
        prefix = json_str[:prefix_index + prefix_offset] + ": \""
        return prefix

    def get_structured_response(self, context, json_protocol_dict, task, prefix_key):
        for trial in range(ProtocolHandler.max_tries):
            try:
                protocol_string = json.dumps(json_protocol_dict, indent=2)
                prefix = self._get_prefix(protocol_string, prefix_key)
                prompt = f"""{context}\n\n{task} {BasicPrompts.json_introducer} {protocol_string}"""
                prompt += f"{BasicPrompts.prefix_introducer}{prefix}"

                json_str = prefix + OpenAIClient().respond(prompt)
                json_str = json_str[:json_str.rfind("}") + 1]
                return json.loads(json_str)
            except:
                print(f"Trying again...{trial+1}/{ProtocolHandler.max_tries}")

        raise Exception("Failed to generate structured response")
