from ipdb import set_trace
from json import load

SCHEMA = "inventory.json"

with open(SCHEMA, "r") as schema_file:
    schema = load(schema_file)

# (
#     schema["paths"]["/v3/inventory"]["get"]["responses"]["200"]["content"]
#     ["application/json"]["schema"]["properties"]["quantity"]
# )
set_trace()
