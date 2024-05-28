from common.exceptions import BadRequestException

from database import forms_collection, form_fields_collection
from db_interface.db_interface_impl import DBInterface

from form_builder.form_helper import form_helper, form_field_helper
from form_builder import form_schema as schemas


class FormFieldsInterface:
    @staticmethod
    async def create_form_fields(request_data, form_id):
        data, message, errors = None, "", {}
        try:
            db_interface = DBInterface(form_fields_collection)
            form_db_interface = DBInterface(forms_collection)
            form_results, result = [], None

            form_obj = await form_db_interface.get_single_item_by_filters({"id": form_id})
            if not form_obj:
                errors["id"] = ["Form not found"]
                raise BadRequestException("Form not found")

            for form_field in request_data["fields"]:
                fields = {"form_id": form_id, "name": form_field["name"], "field_type": form_field["field_type"],
                          "validation_rules": form_field["validation_rules"]}
                form_filed_data = await db_interface.create_with_uuid(data=fields)
                result = form_field_helper(form_filed_data)
                form_results.append(result)

            resultant_data = {"id": form_id, "name": form_obj['name'], "organization_id": form_obj['org_id'],
                              "version": form_obj['version'], "form_fields": form_results}
            data = schemas.FormResponseListData.model_validate(resultant_data)
        except BadRequestException as err:
            message = err.msg
        except Exception as err:
            message = err
        return {"data": data, "errors": errors, "message": message}

    @staticmethod
    async def create_form(request_data, organization_id):
        data, message, errors = None, "", {}
        try:
            form_db_interface = DBInterface(forms_collection)
            # Create form data
            form_obj = await form_db_interface.create_with_uuid(
                data={"name": request_data["name"], "org_id": organization_id, "version": 1.0})
            form_data = form_helper(form_obj)
            result = {"id": form_data["id"], "name": form_data["name"], "version": form_data["version"],
                      "organization_id": organization_id}
            data = schemas.FormResponseData.model_validate(result)
        except BadRequestException as err:
            message = err.msg
        except Exception as err:
            message = err
        return {"data": data, "errors": errors, "message": message}

    @staticmethod
    async def update_form(request_data, form_id):
        data, message, errors = None, "", {}
        try:
            form_db_interface = DBInterface(forms_collection)
            form_field_db_interface = DBInterface(form_fields_collection)
            # Get form data
            form_data = await form_db_interface.get_single_item_by_filters({"id": form_id})
            if not form_data:
                errors["id"] = ["Form not found"]
                raise BadRequestException("Form not found")

            # Create form data
            data = {"name": request_data.pop("name"), "org_id": form_data["org_id"],
                    "version": float(form_data["version"]) + 1}
            new_form_data = await form_db_interface.create_with_uuid(data=data)

            # Create form field data
            form_results = await FormFieldsInterface.create_form_fields(request_data, new_form_data["id"])
            if form_results["errors"]:
                errors["id"] = ["Form not updated"]
                raise BadRequestException(form_results["message"])

            data = form_results["data"]
        except BadRequestException as err:
            message = err.msg
        except Exception as err:
            message = err
        return {"data": data, "errors": errors, "message": message}

    @staticmethod
    async def list_forms(organization_id):
        data, message, errors = None, "", {}
        try:
            form_db_interface = DBInterface(forms_collection)
            form_field_db_interface = DBInterface(form_fields_collection)
            # Get form data
            form_obj = await form_db_interface.get_multiple_items_by_filters({"org_id": organization_id})
            if not form_obj:
                errors["id"] = ["Form not found"]
                raise BadRequestException("Form not found")
            data = []
            for form in form_obj:
                form_field_data = await form_field_db_interface.get_multiple_items_by_filters({"form_id": form["id"]})
                result = {"id": form["id"], "name": form["name"], "organization_id": organization_id,
                          "version": form["version"], "form_fields": form_field_data}
                validated_data = schemas.FormResponseListData.model_validate(result)
                data.append(validated_data)
        except BadRequestException as err:
            message = err.msg
        except Exception as err:
            message = err
        return {"data": data, "errors": errors, "message": message}

    @staticmethod
    async def get_form(form_id):
        data, message, errors = None, "", {}
        try:
            form_db_interface = DBInterface(forms_collection)
            form_field_db_interface = DBInterface(form_fields_collection)
            # Get form data
            form_obj = await form_db_interface.get_single_item_by_filters({"id": form_id})
            if not form_obj:
                errors["id"] = ["Form not found"]
                raise BadRequestException("Form not found")
            form_data = form_helper(form_obj)
            form_field_data = await form_field_db_interface.get_multiple_items_by_filters({"form_id": form_data["id"]})
            result = schemas.FormFieldsResponseList.model_validate(form_field_data)

            data = {"id": form_data["id"], "name": form_data["name"], "organization_id": form_data["org_id"],
                    "form_fields": result}
        except BadRequestException as err:
            message = err.msg
        except Exception as err:
            message = err
        return {"data": data, "errors": errors, "message": message}
