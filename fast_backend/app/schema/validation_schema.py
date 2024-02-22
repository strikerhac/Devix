
import sys
import traceback
import re
from app.schema.base_schema import BaseSchema
class Validator:
    @staticmethod
    def get_field_data_types(schema_class):
        data_types = {}

        for field, value in schema_class.__annotations__.items():
            # Extract the data type without considering the '| None' part
            data_type = re.sub(r'\s*\|\s*None', '', str(value))
            data_types[field] = data_type.strip()

        return data_types

    @staticmethod
    def convert_to_type(type_str):
        # Convert string representation to Python types
        if type_str == 'str':
            return str
        elif type_str == 'int':
            return int
        # Add other type conversions as needed (e.g., float, bool, etc.)
        else:
            return None  # Handle unsupported types

    @staticmethod
    def validate_data(schema_class, data):
        try:
            errors = []

            # Get schema field names and types
            schema_fields = schema_class.__annotations__
            updated_schema_fields = Validator.get_field_data_types(schema_class)
            print("updates schema fields are:::::::::::::::::::::::::::::::",updated_schema_fields,file=sys.stderr)

            # Check if data contains all the fields defined in the schema_class
            for field, expected_type in schema_fields.items():
                # Get the parsed expected type from the updated_schema_fields
                expected_type_parsed = Validator.convert_to_type(updated_schema_fields[field])

                if expected_type_parsed is not None and not isinstance(data[field], expected_type_parsed):
                    errors.append({
                        "id": field,
                        "errors": [f"Value is not of type {expected_type_parsed.__name__}"]
                    })
                
            print("error in validate date is:::::::::::::::::::::::::::::::",errors,file=sys.stderr)
            return errors
        except Exception as e:
            print("Error occurred in validating:", e)
            return [{"id": "validation_error", "errors": ["Error occurred during validation"]}]
        


class Response200(BaseSchema):
    data: dict
    message: str