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
\\title{{{title}}}
\\author{{{author}}}
\\maketitle
"""

    def render(self, document_dict, author):
        latex_source = BasicLatexRenderer.latex_prefix
        latex_source += self._make_title(document_dict["title"], author)

        sections = document_dict["sections"]
        for i, section in enumerate(sections):
            latex_source += f"\\section{{{section['name']}}}\n"
            
            subsections = sections[i]["subsections"]
            for j, subsection in enumerate(subsections):
                latex_source += f"\\subsection{{{subsection['name']}}}\n"

                subsection_paragraphs = subsections[j]["body"]["paragraphs"]
                for k, paragraph in enumerate(subsection_paragraphs):
                    latex_source += f"\\paragraph{{{paragraph['paragraph_name']}}}\n"
                    latex_source += f"{paragraph['text']}\n"
            
            section_paragraphs = sections[i]["intro_or_body"]["paragraphs"]
            for j, paragraph in enumerate(section_paragraphs):
                latex_source += f"\\paragraph{{{paragraph['paragraph_name']}}}\n"
                latex_source += f"{paragraph['text']}\n"

        latex_source += BasicLatexRenderer.latex_suffix

        return latex_source


