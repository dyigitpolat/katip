class BasicPrompts:
    json_introducer = """using the following JSON protocol:\n"""
    prefix_introducer = """\n\nComplete the JSON response (json.loads() must be able to parse it):\n```json\n"""
    draft_task = """Using the abstract, provide a draft for this scientific paper, complete with all crucial sections and subsections"""
    section_body_task_template = """Provide a fully detailed body (or intro) for the {section_name} section"""
    subsection_body_task_template = """Provide a fully detailed body for the {subsection_name} subsection of the {section_name} section"""
    additional_text_instructions = \
"""Refer to other work and experiments as much as possible. To cite, always use the syntax ((citation_needed: <put meaningful keywords about relevant studies here (WITHOUT any author names)>)). to refer to experiments and results, always use the syntax ((result_needed: <put a short description of the required experiment here>)). Refer to other work and experiments as much as possible using our special ((citation_needed: ...)) or ((result_needed: ...)) syntax."""