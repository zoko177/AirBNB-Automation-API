from fastapi import FastAPI, Query
import airbnb_selenium
import time

app = FastAPI()


@app.get("/")
def home():
    return "Hello"


@app.get("/get-price/{check_in}/{check_out}/{apartment_id}")
def get_price(check_in: str, check_out: str, apartment_id: int):
    return {"Apartment ID": apartment_id, "API Price": airbnb_selenium.airBNB_price(apartment_id, check_in, check_out)}


@app.get("/get-multi-price/{check_in}/{check_out}/{apartment_str}")
def get_multi_price(check_in: str, check_out: str, apartment_str: str):
    start = time.time()
    ans = airbnb_selenium.airBNB_multi_price(apartment_str, check_in, check_out)
    print(time.time() - start)
    return ans

