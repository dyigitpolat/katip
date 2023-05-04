from katip.prompting.protocol_handler import ProtocolHandler
from katip.prompting.basic_prompts import BasicPrompts

import json
import os

class DraftGenerator:
    def generate_from_abstract(self, abstract):
        protocol_path = os.getcwd() + "/katip/protocols/document_structure.json"
        draft_protocol = json.load(open(protocol_path))

        return ProtocolHandler().get_structured_response(
            abstract,
            draft_protocol, 
            BasicPrompts.draft_task, 
            BasicPrompts.additional_text_instructions,
            "title")