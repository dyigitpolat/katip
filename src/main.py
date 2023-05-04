from katip.content_generation.abstract_generator import AbstractGenerator
from katip.content_generation.elaborator import Elaborator
from katip.content_generation.document_generator import DocumentGenerator
from katip.renderers.basic_latex_renderer import BasicLatexRenderer

import json
import os

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs("../generated", exist_ok=True)

    context = input("provide context: _")
    abstract = AbstractGenerator().generate_abstract(context)
    abstract = Elaborator().elaborate_abstract(abstract)

    document_dict = DocumentGenerator().generate_from_abstract(abstract)
    json.dump(document_dict, open("../generated/document.json", "w"))

    document_dict = json.load(open("../generated/document.json"))
    latex_source = BasicLatexRenderer().render(document_dict, "Yigit Polat")

    with open("../generated/document.tex", "w") as f:
        f.write(latex_source)