from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

rates = {
    "INR":1,
    "USD":0.010,
    "EUR":0.009,
    "YEN":1.695,
    "GBP":0.008,
    "AUD":0.015
    }
class updaterates(BaseModel):
     USD:Optional[int]=None
     EUR:Optional[int]=None
     YEN:Optional[int]=None
     GBP:Optional[int]=None
     AUD:Optional[int]=None
   
@app.get("/convert")
def convert(amount:float, from_currency:str, to_currency:str):
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in rates or to_currency not in rates:
        raise HTTPException(status_code = 400, detail="this currency is not in the list")
    amount_in_USD = amount  / rates[from_currency]
    converted_amount = amount_in_USD * rates[to_currency]

    return {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
        "converted_amount": round(converted_amount, 2)
    }

@app.put("/rates")
def update_rates(new_rates: updaterates):
    updated = False

    for currency, value in new_rates.dict().items():
        if value is not None:
            rates[currency] = value
            updated = True

    if not updated:
        raise HTTPException(status_code=400, detail="No valid rates provided to update")

    return {"updated_rates": rates}
