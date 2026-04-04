import json
from langchain_core.tools import tool

@tool
def log_interaction(hcp_name: str = "", date: str = "", product: str = "", sentiment: str = "", follow_up: str = "", notes: str = ""):
    """Extract structured medical CRM interaction details from this input."""
    return json.dumps({"type": "log_interaction", "data": {"hcp_name": hcp_name, "date": date, "product": product, "sentiment": sentiment, "follow_up": follow_up, "notes": notes}})

@tool
def edit_interaction(field_name: str, new_value: str):
    """Modify specific fields based on user correction."""
    return json.dumps({"type": "edit_interaction", "field": field_name, "value": new_value})

@tool
def validate_missing_fields(hcp_name: str = "", date: str = "", product: str = "", sentiment: str = "", follow_up: str = "", notes: str = ""):
    """Check missing required fields. Required fields: hcp_name, date, product, sentiment."""
    missing = []
    if not hcp_name: missing.append("hcp_name")
    if not date: missing.append("date")
    if not product: missing.append("product")
    if not sentiment: missing.append("sentiment")
    if missing:
        return f"Missing required fields: {', '.join(missing)}"
    return "All required fields are present."

@tool
def submit_form():
    """Trigger the submission of the form to save the data in the database."""
    return json.dumps({"type": "submit_form"})

@tool
def clear_form():
    """Reset all fields in the form."""
    return json.dumps({"type": "clear_form"})

tools_list = [log_interaction, edit_interaction, validate_missing_fields, submit_form, clear_form]
