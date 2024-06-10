import api_keys
from katip.content_generation.document_generator import DocumentGenerator
from katip.renderers.basic_markdown_renderer import BasicMarkdownRenderer
from katip.citations.reference_fetcher import find_references_in_document_dict

import flask
import json
import markdown

from flask import Flask, render_template, request, render_template_string

app = Flask(__name__)



@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    katip_token = request.form['katip_token']
    research_context = request.form['research_context']

    if katip_token != api_keys.katip_token:
        return render_template('error.html')

    print("generating document...")
    document_dict = DocumentGenerator().generate(research_context)

    print("fetching references...")
    document_dict = find_references_in_document_dict(document_dict)

    print("rendering markdown...")
    markdown_source = BasicMarkdownRenderer().render(document_dict, "Anonymous")

    print("rendering html...")
    html = markdown.markdown(markdown_source)

    return render_template('result.html', html=html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)


        