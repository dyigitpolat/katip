from katip.content_generation.document_generator import DocumentGenerator
from katip.renderers.basic_latex_renderer import BasicLatexRenderer

import json
import os
import sys

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs("../generated", exist_ok=True)

    if len(sys.argv) < 2:
        user_context = input("provide context: _")
    else:
        user_context = open(sys.argv[1]).read()
        
    print("generating document...")
    document_dict = DocumentGenerator().generate(user_context)
    json.dump(document_dict, open("../generated/document.json", "w"))

    print("rendering latex...")
    document_dict = json.load(open("../generated/document.json"))
    latex_source = BasicLatexRenderer().render(document_dict, "Yigit Polat")

    with open("../generated/document.tex", "w") as f:
        f.write(latex_source)