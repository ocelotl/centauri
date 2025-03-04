from ipdb import set_trace
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col, udf
from json import load

with open("credentials.json") as credentials_file:
    credentials = load(credentials_file)

session = Session.builder.configs(credentials).create()

@udf(name="capitalize", is_permanent=True, )

print(session)

table = session.table("FLOWER_DETAILS")

table.show()
print(table.count())
set_trace()
