from crawlers.yuantaetfs import get_etf_trading_reference_rates

from typing import Union

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def connect():
    return {"msg": "connection successful"}

@app.get("/yuan_ta/etf_fee", tags=["元大投信"])
def get_yuan_ta_etf_fee():
    try:
        return get_etf_trading_reference_rates()
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))