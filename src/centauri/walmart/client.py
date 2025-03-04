from requests import get
from ipdb import set_trace

set_trace

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
