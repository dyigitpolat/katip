class BasicPrompts:
    json_introducer = """using the following JSON protocol:\n"""
    prefix_introducer = """\n\nComplete the response as parsable JSON (use proper escape sequences, mind the JSON syntax etc.):\n```json\n"""
    draft_task = """Using the abstract, provide a draft for this scientific paper, complete with all crucial sections and subsections"""
    section_body_task_template = """Provide a fully detailed body (or intro) for the {section_name} section"""
    subsection_body_task_template = """Provide a fully detailed body for the {subsection_name} subsection of the {section_name} section"""