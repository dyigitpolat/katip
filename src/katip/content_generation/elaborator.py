from katip.prompting.protocol_handler import ProtocolHandler
import os
import json

class Elaborator:
    def elaborate(self, context, paragraph):
        protocol_path = os.getcwd() + "/katip/protocols/paragraph.json"
        paragraph_protocol = json.load(open(protocol_path))

        context += "\n\n" + json.dumps(paragraph)
        return ProtocolHandler().get_structured_response(
            context,
            paragraph_protocol,
            "Add more content and elaborate the paragraph",
            "paragraph_name")
