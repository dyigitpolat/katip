from katip.prompting.protocol_handler import ProtocolHandler

import json
import os

class AbstractGenerator:
    def generate_abstract(self, context):
        protocol_path = os.getcwd() + "/katip/protocols/abstract.json"
        abstract_protocol = json.load(open(protocol_path))

        return ProtocolHandler().get_structured_response(
            context,
            abstract_protocol, 
            "Write an abstract for the scientific paper explained above", 
            "title")["abstract"]
