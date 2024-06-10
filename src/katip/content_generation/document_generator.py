from katip.content_generation.abstract_generator import AbstractGenerator
from katip.content_generation.draft_generator import DraftGenerator
from katip.content_generation.body_generator import BodyGenerator 
from katip.content_generation.elaborator import Elaborator 

import threading

class DocumentGenerator:
    def _elaborate_paragraph(self, paragraphs, idx, abstract, paragraph):
        print("elaborating paragraph:", paragraph["paragraph_name"])
        paragraphs[idx] = Elaborator().elaborate(abstract, paragraph)
        print("elaborated paragraph:", paragraph["paragraph_name"])

    def _generate_subsection(self, abstract, subsections, section, subsection, j):
        print("generating subsection", subsection["name"], "of", section["name"])
        subsections[j] = BodyGenerator().generate_subsection_body(abstract, section, subsection)

        threads = []
        paragraph_dict = {}
        subsection_paragraphs = subsections[j]["body"]["paragraphs"]
        for k, paragraph in enumerate(subsection_paragraphs):
            thread = threading.Thread(target=self._elaborate_paragraph, args=(paragraph_dict, int(k), abstract, paragraph))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

        for k, paragraph in enumerate(subsection_paragraphs):
            subsection_paragraphs[j] = paragraph_dict[j]
        
        print("generated subsection", subsection["name"], "of", section["name"])


    def _generate_section(self, abstract, sections, section, i):
        print("generating section", section["name"])
        sections[i] = BodyGenerator().generate_section_body(abstract, section)
            
        subsections = sections[i]["subsections"]
        subsections_dict = {}
        threads = []
        for j, subsection in enumerate(subsections):
            thread = threading.Thread(target=self._generate_subsection, args=(abstract, subsections_dict, section, subsection, int(j)))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

        for j, subsection in enumerate(subsections):
            subsections[j] = subsections_dict[j]
        
        threads = []
        paragraph_dict = {}
        section_paragraphs = sections[i]["body"]["paragraphs"]
        for j, paragraph in enumerate(section_paragraphs):
            thread = threading.Thread(target=self._elaborate_paragraph, args=(paragraph_dict, int(j), abstract, paragraph))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

        for j, paragraph in enumerate(section_paragraphs):
            section_paragraphs[j] = paragraph_dict[j]

        print("generated section", section["name"])
    

    def generate(self, user_context):
        print("generating abstract...")
        abstract = AbstractGenerator().generate_abstract(user_context)

        print("elaborating abstract...")
        abstract = Elaborator().elaborate_abstract(abstract)

        print("generating draft...")
        document_dict = DraftGenerator().generate_from_abstract(abstract)

        document_structure_context = "The paper is structured as follows: \n"
        for section in document_dict["sections"]:
            document_structure_context += section["name"] + "("
            if "subsections" in section:
                for subsection in section["subsections"]:
                    document_structure_context += subsection["name"] + ", "
            document_structure_context = document_structure_context[:-2] + ") \n"

        section_context = user_context + "\n\nAbstract: " + abstract + "\n\n" + document_structure_context

        sections = document_dict["sections"]
        sections_dict = {}
        threads = []
        for i, section in enumerate(sections):
            thread = threading.Thread(target=self._generate_section, args=(section_context, sections_dict, section, int(i)))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

        for i, section in enumerate(sections):
            sections[i] = sections_dict[i]

        document_dict["abstract"] = abstract
        return document_dict
        

