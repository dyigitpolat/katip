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
    

    def get_structured_response(self, context, json_protocol_dict, task, additional_instructions, prefix_key):
        return self.get_structured_completion(context, json_protocol_dict, task, additional_instructions, prefix_key, json_protocol_dict)
    
    def get_structured_completion(self, context, json_protocol_dict, task, additional_instructions, prefix_key, completion_dict):
        for trial in range(ProtocolHandler.max_tries):
            try:
                protocol_string = json.dumps(json_protocol_dict, indent=2)
                prompt = f"""{context}\n\n{task} {BasicPrompts.json_introducer}{protocol_string}"""
                prompt += f"\n\nAdditional Instructions: {additional_instructions}"

                completion_string = json.dumps(completion_dict, indent=2)
                prefix = self._get_prefix(completion_string, prefix_key)
                prompt += f"{BasicPrompts.prefix_introducer}{prefix}"

                json_str :str = prefix + OpenAIClient().respond(prompt)
                json_str = json_str.replace("\n", "")
                json_str = json_str.replace("\t", "")
                json_str = json_str.replace("\r", "")
            
                try:
                    json_str_final = json_str[:json_str.rfind("}") + 1]
                    print("JSON STR FINAL 1", json_str_final)
                    return json.loads(json_str_final)
                except:
                    json_str_final = json_str + "\"}"
                    print("JSON STR FINAL 2", json_str_final)
                    return json.loads(json_str_final)
                
            except:
                print(f"Trying again...{trial+1}/{ProtocolHandler.max_tries}")

        raise Exception("Failed to generate structured response")