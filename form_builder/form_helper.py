# Helper functions to convert MongoDB documents to dict
def form_helper(form) -> dict:
    return {
        "id": str(form["id"]),
        "org_id": form["org_id"],
        "name": form["name"],
        "version": form["version"],
    }


def form_field_helper(form_field) -> dict:
    return {
        "id": str(form_field["id"]),
        "form_id": form_field["form_id"],
        "name": form_field["name"],
        "field_type": form_field["field_type"],
        "validation_rules": form_field["validation_rules"]
    }
