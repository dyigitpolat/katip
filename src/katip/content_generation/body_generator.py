from katip.prompting.protocol_handler import ProtocolHandler
from katip.prompting.basic_prompts import BasicPrompts

import json
import os

class BodyGenerator:
    def generate_section_body(self, context, section):
        protocol_path = os.getcwd() + "/katip/protocols/section_details.json"
        protocol_dict = json.load(open(protocol_path))

        completion_dict = dict(protocol_dict)
        completion_dict["name"] = section["name"]
        completion_dict["summary"] = section["summary"]

        if "subsections" in section:
            completion_dict["subsections"] = section["subsections"]
        else:
            completion_dict["subsections"] = []

        return ProtocolHandler().get_structured_completion(
            context, protocol_dict, 
            BasicPrompts.section_body_task_template.format(
                section_name=section["name"]), 
            BasicPrompts.additional_text_instructions,
            "paragraph_name", completion_dict
        )
    
    def generate_subsection_body(self, context, section, subsection):
        protocol_path = os.getcwd() + "/katip/protocols/subsection_details.json"
        protocol_dict = json.load(open(protocol_path))

        context += f"\n\nSection: {section['name']}"
        context += f"\nSection Summary: {section['summary']}\n"
        
        completion_dict = dict(protocol_dict)
        completion_dict["name"] = subsection["name"]
        completion_dict["summary"] = subsection["summary"]

        return ProtocolHandler().get_structured_completion(
            context, protocol_dict, 
            BasicPrompts.subsection_body_task_template.format(
                section_name=section["name"], subsection_name=subsection["name"]), 
            BasicPrompts.additional_text_instructions,
            "paragraph_name", completion_dict
        )
        


