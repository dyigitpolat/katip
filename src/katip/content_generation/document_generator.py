from katip.content_generation.draft_generator import DraftGenerator
from katip.content_generation.body_generator import BodyGenerator 

class DocumentGenerator:
    def generate_from_abstract(self, abstract):
        document_dict = DraftGenerator().generate_from_abstract(abstract)

        sections = document_dict["sections"]
        for i, section in enumerate(sections):
            sections[i] = BodyGenerator().generate_section_body(abstract, section)
            
            subsections = sections[i]["subsections"]
            for j, subsection in enumerate(subsections):
                subsections[j] = BodyGenerator().generate_subsection_body(abstract, section, subsection)

        return document_dict