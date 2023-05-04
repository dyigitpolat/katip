from katip.prompting.protocol_handler import ProtocolHandler
import os
import json

class Elaborator:
    def elaborate(self, context, paragraph):
        protocol_path = os.getcwd() + "/katip/protocols/paragraph.json"
        paragraph_protocol = json.load(open(protocol_path))

        context += "\n\n" + json.dumps(paragraph, indent=2)
        return ProtocolHandler().get_structured_response(
            context,
            paragraph_protocol,
            "Add more content and elaborate the given paragraph (but retain the main ideas)",
            "paragraph_name")
    
    def elaborate_abstract(self, abstract):
        protocol_path = os.getcwd() + "/katip/protocols/abstract.json"
        abstract_protocol = json.load(open(protocol_path))

        return ProtocolHandler().get_structured_response(
            abstract,
            abstract_protocol, 
            "Add more content and elaborate the abstract",
            "title")["abstract"]
