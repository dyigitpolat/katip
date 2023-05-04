from katip.prompting.protocol_handler import ProtocolHandler
import os
import json

class Elaborator:
    def elaborate(self, context, paragraph):
        protocol_path = os.getcwd() + "/katip/protocols/paragraph.json"
        paragraph_protocol = json.load(open(protocol_path))

        context += f"\n\nGiven paragraph:\n{paragraph['paragraph_name']}: {paragraph['text']}"

        return ProtocolHandler().get_structured_completion(
            context,
            paragraph_protocol,
            "Add more content and elaborate the given paragraph (but retain the main ideas)",
            "text", paragraph)
    
    def elaborate_abstract(self, abstract):
        protocol_path = os.getcwd() + "/katip/protocols/abstract.json"
        abstract_protocol = json.load(open(protocol_path))

        return ProtocolHandler().get_structured_response(
            abstract,
            abstract_protocol, 
            "Add more content and elaborate the abstract",
            "title")["abstract"]
