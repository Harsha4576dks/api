from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import random
import string

app = FastAPI()

Urls = {
    "azch": "https://www.harsha.python.com"
}


class Url(BaseModel):
    Link: str


@app.post("/urls", status_code=status.HTTP_201_CREATED)
def create_url(url: Url):
    characters = string.ascii_letters + string.digits

    while True:
        random_code = "".join(random.choices(characters, k=6))
        if random_code not in Urls:
            break

    Urls[random_code] = url.Link

    return {
        "message": "Short URL created successfully",
        "short_code": random_code,
        "short_url": f"http://localhost:8000/{random_code}"
    }

@app.get("/{short_code}")
def open_url(short_code: str):
    if short_code not in Urls:
        raise HTTPException(status_code=404,detail="Short URL not found")

    return RedirectResponse(url=Urls[short_code])

@app.get("/urls")
def get_all_urls():
    return Urls

@app.delete("/urls/{short_code}", status_code=status.HTTP_200_OK)
def delete_url(short_code: str):
    if short_code not in Urls:
        raise HTTPException(status_code=404,detail="Short URL not found")

    del Urls[short_code]
    return {"message": "Short URL deleted successfully"}