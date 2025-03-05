from requests import get
from ipdb import set_trace
from centauri.walmart.models import Inventory
from snowflake.snowpark.session import Session
from json import load
from os import getenv

api_url = "http://localhost:8000/"

response = get(
    f"{api_url}/v3/inventory/",
    params={"sku": "the_sku", "shipnode": "the_shipnode"},
    headers={
        "Authorization": "the_Authorization",
        "WM_SEC.ACCESS_TOKEN": "the_WM_SEC.ACCESS_TOKEN"
    }
)

print(response.json())

inventory = Inventory(**response.json())

with open(getenv("SNOWFLAKE_CREDENTIALS_PATH")) as credentials_file:
    session = Session.builder.configs(load(credentials_file)).create()

table = session.table("INVENTORY")

dataframe = session.create_dataframe(
    [(inventory.sku, inventory.unit, inventory.amount)],
    schema=["sku", "unit", "amount"]
)
dataframe.write.save_as_table("inventory", mode="append")
table.show()
print(table.count())
set_trace()
