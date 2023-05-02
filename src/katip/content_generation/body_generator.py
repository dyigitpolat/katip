from katip.prompting.protocol_handler import ProtocolHandler
from katip.prompting.basic_prompts import BasicPrompts

import json
import os

class BodyGenerator:
    def generate_section_body(self, context, section):
        protocol_path = os.getcwd() + "/katip/protocols/section_details.json"

        protocol_dict = json.load(open(protocol_path))
        protocol_dict["name"] = section["name"]
        protocol_dict["summary"] = section["summary"]

        if "subsections" in section:
            protocol_dict["subsections"] = section["subsections"]
        else:
            protocol_dict["subsections"] = []

        return ProtocolHandler().get_structured_response(
            context, protocol_dict, 
            BasicPrompts.section_body_task_template.format(
                section_name=section["name"]), 
            "paragraph_name"
        )
    
    def generate_subsection_body(self, context, section, subsection):
        protocol_path = os.getcwd() + "/katip/protocols/subsection_details.json"

        protocol_dict = json.load(open(protocol_path))
        protocol_dict["name"] = subsection["name"]
        protocol_dict["summary"] = subsection["summary"]

        return ProtocolHandler().get_structured_response(
            context, protocol_dict, 
            BasicPrompts.subsection_body_task_template.format(
                section_name=section["name"], subsection_name=subsection["name"]), 
            "paragraph_name"
        )
        


