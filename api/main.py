from crawlers.yuantaetfs import get_etf_trading_reference_rates

from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def connect():
    return {"msg": "connection successful"}

@app.get("/yuan_ta/etf_fee", tags=["元大投信"])
def get_yuan_ta_etf_fee():
    return get_etf_trading_reference_rates()
