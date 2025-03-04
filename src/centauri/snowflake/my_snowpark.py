from ipdb import set_trace
from snowflake.snowpark.session import Session
from json import load

with open("credentials.json") as credentials_file:
    credentials = load(credentials_file)

session = Session.builder.configs(credentials).create()

print(session)

table = session.table("INVENTORY")

table.show()
print(table.count())
set_trace()
