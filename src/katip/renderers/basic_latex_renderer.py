import re

class BasicLatexRenderer:
    latex_prefix = \
"""
\\documentclass{article}

\\begin{document}
"""

    latex_suffix = \
"""
\\end{document}
"""

    def _make_title(self, title, author):
        return \
f"""
\\title{{{self._L(title)}}}
\\author{{{self._L(author)}}}
\\maketitle
"""

    def _make_abstract(self, abstract):
        return \
f"""
\\begin{{abstract}}
{self._L(abstract)}
\\end{{abstract}}
"""

    def _L(self, text):
        latex_source = text

        # replace latex special characters with escaped versions
        latex_characters = ['\\', '{', '}', '&', '%', '$', '#', '_', '^', '~']
        for character in latex_characters:
            latex_source = latex_source.replace(character, '\\' + character)

        return latex_source
    
    def _make_references(self, latex_source):
        references = "\n\\section{{References}}\n"
        matches = re.findall(r'\(citation\\_needed:.*?\)', latex_source)
        for match in matches:
            references += f"{match} \\\\ \n"
        
        return references
    
    def _make_results(self, latex_source):
        results = "\n\\section{{Results}}\n"
        matches = re.findall(r'\(result\\_needed:.*?\)', latex_source)
        for match in matches:
            results += f"{match} \\\\ \n"
        
        return results


    def render(self, document_dict, author):
        latex_source = BasicLatexRenderer.latex_prefix
        latex_source += self._make_title(document_dict["title"], author)
        
        abstract = document_dict["abstract"]
        latex_source += self._make_abstract(abstract)

        sections = document_dict["sections"]
        for i, section in enumerate(sections):
            latex_source += f"\\section{{{self._L(section['name'])}}}\n"
            
            subsections = sections[i]["subsections"]
            for j, subsection in enumerate(subsections):
                latex_source += f"\\subsection{{{self._L(subsection['name'])}}}\n"

                subsection_paragraphs = subsections[j]["body"]["paragraphs"]
                for k, paragraph in enumerate(subsection_paragraphs):
                    latex_source += f"\\paragraph{{{self._L(paragraph['paragraph_name'])}}}\n"
                    latex_source += f"{self._L(paragraph['text'])}\n"
            
            section_paragraphs = sections[i]["body"]["paragraphs"]
            for j, paragraph in enumerate(section_paragraphs):
                latex_source += f"\\paragraph{{{self._L(paragraph['paragraph_name'])}}}\n"
                latex_source += f"{self._L(paragraph['text'])}\n"

        latex_source += self._make_references(latex_source)
        latex_source += self._make_results(latex_source)
        latex_source += BasicLatexRenderer.latex_suffix

        return latex_source


