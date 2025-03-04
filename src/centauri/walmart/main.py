from fastapi import FastAPI, Header
from centauri.walmart.models import Quantity, Inventory

app = FastAPI()


@app.get("/v3/inventory")
async def get_inventory(
    sku: str,
    shipnode: str,
    authorization: str = Header(None),
    wm_sec_access_token: str = Header(None),
    wm_consumer_channel_type: str = Header(None),
    wm_qos_correlation_id: str = Header(None),
    wm_svc_name: str = Header(None)

) -> Inventory:

    return Inventory(
        sku="97964_KFtest", quantity=Quantity(unit="EACH", amount=10)
    )
