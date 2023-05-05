class BasicPrompts:
    json_introducer = """using the following JSON protocol:\n"""
    prefix_introducer = """\n\nComplete the JSON response (json.loads() must be able to parse it):\n```json\n"""
    draft_task = """Using the abstract, provide a draft for this scientific paper, complete with all crucial sections and subsections"""
    section_body_task_template = """Provide a fully detailed body for the "{section_name}" section (stay strictly within the section scope of "{section_name}")"""
    subsection_body_task_template = """Provide a fully detailed body for the "{subsection_name}" subsection of the "{section_name}" section (stay strictly within the subsection scope of "{subsection_name}")"""
    additional_text_instructions = \
"""Refer to other work and experiments as much as possible. Always use the syntax ((result_needed: <short description of experiment>)) for referring to experiments and results. Always use the syntax ((citation_needed: <keywords and topics about relevant work, without author names>)) for referring to other work. """