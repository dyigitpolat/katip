from katip.content_generation.draft_generator import DraftGenerator
from katip.content_generation.body_generator import BodyGenerator 
from katip.content_generation.elaborator import Elaborator 

import threading

class DocumentGenerator:
    def _elaborate_paragraph(self, paragraphs, idx, abstract, paragraph):
        paragraphs[idx] = Elaborator().elaborate(abstract, paragraph)

    def _generate_subsection(self, abstract, subsections, section, subsection, j):
        subsections[j] = BodyGenerator().generate_subsection_body(abstract, section, subsection)

        threads = []
        subsection_paragraphs = subsections[j]["body"]["paragraphs"]
        for k, paragraph in enumerate(subsection_paragraphs):
            thread = threading.Thread(target=self._elaborate_paragraph, args=(subsection_paragraphs, k, abstract, paragraph))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()


    def _generate_section(self, abstract, sections, section, i):
        sections[i] = BodyGenerator().generate_section_body(abstract, section)
            
        subsections = sections[i]["subsections"]
        threads = []
        for j, subsection in enumerate(subsections):
            thread = threading.Thread(target=self._generate_subsection, args=(abstract, subsections, section, subsection, j))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        threads = []
        section_paragraphs = sections[i]["intro_or_body"]["paragraphs"]
        for j, paragraph in enumerate(section_paragraphs):
            thread = threading.Thread(target=self._elaborate_paragraph, args=(section_paragraphs, j, abstract, paragraph))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()


    def generate_from_abstract(self, abstract):
        document_dict = DraftGenerator().generate_from_abstract(abstract)

        sections = document_dict["sections"]
        threads = []
        for i, section in enumerate(sections):
            thread = threading.Thread(target=self._generate_section, args=(abstract, sections, section, i))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

        return document_dict