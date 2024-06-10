import re

class BasicMarkdownRenderer:\

    def _make_title(self, title, author):
        return \
f"""
# {title}
## {author}
"""

    def _make_abstract(self, abstract):
        return \
f"""
## Abstract
{abstract}
"""
    def _make_references(self, source):
        references = "\n## References\n"
        matches = re.findall(r'\(\(citation.*?\)\)', source)
        for match in matches:
            references += f"-{match}  \n"
        
        return references
    
    def _make_results(self, source):
        results = "\n## Results\n"
        matches = re.findall(r'\(\(result.*?\)\)', source)
        for match in matches:
            results += f"-{match}  \n"
        
        return results

    def render(self, document_dict, author):
        markdown_source = ""
        markdown_source += self._make_title(document_dict["title"], author)
        markdown_source += self._make_abstract(document_dict["abstract"])

        sections = document_dict["sections"]
        for section in sections:
            markdown_source += f"\n## {section['name']}\n"

            section_paragraphs = section["body"]["paragraphs"]
            for paragraph in section_paragraphs:
                paragraph_name = paragraph["paragraph_name"]
                markdown_source += f"\n#### {paragraph_name}:\n"
                markdown_source += f"{paragraph['text']}\n"

            if "subsections" in section:
                for subsection in section["subsections"]:
                    markdown_source += f"\n### {subsection['name']}\n"

                    subsection_paragraphs = subsection["body"]["paragraphs"]
                    for paragraph in subsection_paragraphs:
                        paragraph_name = paragraph["paragraph_name"]
                        markdown_source += f"\n#### {paragraph_name}:\n"
                        markdown_source += f"{paragraph['text']}\n"

        markdown_source += self._make_references(markdown_source)
        markdown_source += self._make_results(markdown_source)

        return markdown_source


