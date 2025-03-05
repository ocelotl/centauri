from pathlib import Path
from os import listdir
from json import load, dumps
from ipdb import set_trace
from collections import OrderedDict


dumps
schemas_path = Path(__file__).parent.joinpath("schemas")


_type_type = {
    "integer": int,
    "boolean": bool,
    "string": str,
    "array": list,
    "object": object,
    "number": float,
}


def parse_schema(schema_path: Path, parsed_schema: dict):

    def traverse_schema(schema: dict, path: list, parsed_schema: dict):

        schema_type = schema.get("type")

        if schema_type == "array":
            traverse_schema(schema["items"], path, parsed_schema)

        if schema_type == "object":

            schema_properties = schema.get("properties", {})

            all_properties = set(schema_properties.keys())

            required_properties = set(schema.get("required", []))

            optional_properties = all_properties.difference(
                required_properties
            )

            required_properties = sorted(list(required_properties))
            optional_properties = sorted(list(optional_properties))

            result_required_properties = OrderedDict()
            result_optional_properties = OrderedDict()

            for required_property in required_properties:

                required_property_type = _type_type[
                    schema_properties[required_property]["type"]
                ].__name__

                if (
                    required_property_type == "list" or
                    required_property_type == "object"
                ):
                    path.append(required_property)
                    traverse_schema(
                        schema["properties"][required_property],
                        path,
                        parsed_schema
                    )
                    path.pop()

                result_required_properties[required_property] = (
                    required_property_type
                )

            for optional_property in optional_properties:

                optional_property_type = _type_type[
                    schema_properties[optional_property]["type"]
                ].__name__

                if (
                    optional_property_type == "list" or
                    optional_property_type == "object"
                ):
                    path.append(required_property)
                    traverse_schema(
                        schema["properties"][optional_property],
                        path,
                        parsed_schema
                    )
                    path.pop()

                result_optional_properties[optional_property] = (
                    optional_property_type
                )

            result = OrderedDict()
            result["class_name"] = schema["xml"]["name"]

            result.update(result_required_properties)
            result.update(result_optional_properties)

            print(dumps(result, indent=4))
            set_trace()

    with open(schema_path) as schema_file:
        schema = load(schema_file)

    paths = {}

    for path_key, path_value in schema["paths"].items():

        paths[path_key] = {}

        for operation_key, operation_value in path_value.items():

            paths[path_key][operation_key] = {}

            for status_code_key, status_code_value in (
                operation_value["responses"].items()
            ):

                if "application/json" in status_code_value["content"].keys():
                    paths[path_key][operation_key][status_code_key] = (
                        status_code_value["content"]
                        ["application/json"]["schema"]
                    )

    for path_key, path_value in paths.items():
        for operation_key, operation_value in path_value.items():
            for status_code_key, status_code_value in (
                operation_value.items()
            ):
                traverse_schema(
                    status_code_value,
                    ["/".join([path_key, operation_key, status_code_key])]
                )


for schema in listdir(schemas_path):

    parsed_schema = {}

    parse_schema(schemas_path.joinpath(schema), parsed_schema)
