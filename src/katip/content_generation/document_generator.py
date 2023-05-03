from katip.content_generation.draft_generator import DraftGenerator
from katip.content_generation.body_generator import BodyGenerator 
from katip.content_generation.elaborator import Elaborator 

class DocumentGenerator:
    def generate_from_abstract(self, abstract):
        document_dict = DraftGenerator().generate_from_abstract(abstract)

        sections = document_dict["sections"]
        for i, section in enumerate(sections):
            sections[i] = BodyGenerator().generate_section_body(abstract, section)
            
            subsections = sections[i]["subsections"]
            for j, subsection in enumerate(subsections):
                subsections[j] = BodyGenerator().generate_subsection_body(abstract, section, subsection)

                subsection_paragraphs = subsections[j]["body"]["paragraphs"]
                for k, paragraph in enumerate(subsection_paragraphs):
                    subsection_paragraphs[k] = Elaborator().elaborate(abstract, paragraph)
            
            section_paragraphs = sections[i]["intro_or_body"]["paragraphs"]
            for j, paragraph in enumerate(section_paragraphs):
                section_paragraphs[j] = Elaborator().elaborate(abstract, paragraph)

        return document_dict