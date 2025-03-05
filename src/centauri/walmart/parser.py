from pathlib import Path
from os import listdir
from json import load, dumps
from ipdb import set_trace

set_trace
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


def parse_schema(schema: dict, path: list):

    parsed_schema = {}

    schema_type = schema.get("type")

    if schema_type == "object":

        schema_properties = schema.get("properties", {})

        all_properties = set(schema_properties.keys())

        required_properties = set(schema.get("required", []))

        optional_properties = all_properties.difference(
            required_properties
        )

        required_properties = sorted(list(required_properties))
        optional_properties = sorted(list(optional_properties))

        parsed_schema["required_properties"] = []
        parsed_schema["optional_properties"] = []

        def process_properties(
            schema: dict,
            properties: list,
            schema_propeties: dict,
            parsed_schema_properties: list,
            path: list
        ):

            for property_ in properties:

                property_type = _type_type[
                    schema_properties[property_]["type"]
                ].__name__

                if (
                    property_type == "str" and
                    "enum" in schema_properties[property_].keys()
                ):
                    parsed_schema_properties.append(
                        {
                            property_: "enum",
                            "values": schema_properties[property_]["enum"]
                        }
                    )

                if property_type == "object":
                    path.append(property_)
                    parsed_schema_properties.append(
                        {
                            "is_array": False,
                            property_: parse_schema(
                                schema["properties"][property_],
                                path
                            )
                        }
                    )
                    path.pop()

                elif property_type == "list":
                    path.append(property_)
                    parsed_schema_properties.append(
                        {
                            "is_array": True,
                            property_: parse_schema(
                                schema["properties"][property_]["items"],
                                path
                            )
                        }
                    )
                    path.pop()

                else:
                    parsed_schema_properties.append(
                        {
                            property_: property_type
                        }
                    )

        process_properties(
            schema,
            required_properties,
            schema_properties,
            parsed_schema["required_properties"],
            path
        )
        process_properties(
            schema,
            optional_properties,
            schema_properties,
            parsed_schema["optional_properties"],
            path
        )

        if "xml" in schema.keys():
            parsed_schema["name"] = schema["xml"]["name"]

        else:
            parsed_schema["name"] = None

        parsed_schema["path"] = "/".join(path)

    return parsed_schema


def process_schema(schema_path: Path) -> dict:

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

    processed_schema = {}

    for path_key, path_value in paths.items():
        for operation_key, operation_value in path_value.items():
            for status_code_key, status_code_value in (
                operation_value.items()
            ):

                processed_path = "/".join(
                    [
                        schema_path.name,
                        "paths",
                        path_key[1:],
                        operation_key,
                        status_code_key
                    ]
                )

                processed_schema[processed_path] = parse_schema(
                    status_code_value,
                    [processed_path]
                )

    return processed_schema


for schema in listdir(schemas_path):

    processed_schema = process_schema(schemas_path.joinpath(schema))

    with open(schemas_path.joinpath(f"processed_{schema}"), "w") as (
        processed_schema_file
    ):
        processed_schema_file.write(dumps(processed_schema, indent=4))
