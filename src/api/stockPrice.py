import json
from typing import List
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import StockPrice
from api.type import AddStockPriceRequestType


def addPrice(props: AddStockPriceRequestType) -> StockPrice:
    url = "http://localhost:3000/company/{}/stock".format(props["companyID"])
    result = requests.post(url, json=({"props": props}))
    price: StockPrice = json.loads(result.content.decode('utf-8'))
    print("[addPrice] result: {}".format(price))
    return price

def getPriceList(companyID: int) -> List[StockPrice]:
    url = "http://localhost:3000/company/{}/stock".format(companyID)
    result = requests.get(url)
    priceList: List[StockPrice] = json.loads(result.content.decode('utf-8'))
    print("[getPriceList] result: {}".format(priceList))
    return priceList


def getPrice(companyID: int, id: int) -> StockPrice:
    url = "http://localhost:3000/company/{}/stock/{}".format(companyID, id)
    result = requests.get(url)
    price: StockPrice = json.loads(result.content.decode('utf-8'))
    print("[getPrice] result: {}".format(price))
    return price


if __name__ == "__main__":
    # addPrice("test", 1, 3)
    getPriceList(1)
    # getPriceList()