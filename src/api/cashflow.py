import json
from typing import List, Optional
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import Cashflow
from api.type import AddCashFlowRequestType

HOST = os.getenv("TOKO_URL")
PORT = os.getenv("TOKO_PORT")

def addCashFlow(companyID: int, props: AddCashFlowRequestType, isPrintLog: bool = False) -> Optional[Cashflow]:
    url = "{}:{}/company/{}/finantial/{}/cashflow".format(HOST, PORT, companyID, props["finantialID"])
    try:
        result = requests.post(url, json=({"props": props}))
    except requests.exceptions.InvalidJSONError:
        # NOTE: いずれかの情報がyfinance APIから取得出来ていない場合
        return None

    cashflow: Cashflow = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[addCashFlow] result: {}".format(cashflow))
    return cashflow

def getCashFlowList(companyID: int, finantialID: int, isPrintLog: bool = False) -> List[Cashflow]:
    url = "{}:{}/company/{}/finantial/{}/cashflow".format(HOST, PORT, companyID, finantialID)
    result = requests.get(url)
    cashflowList: List[Cashflow] = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getCashFlowList] result: {}".format(cashflowList))
    return cashflowList


def getCashFlow(companyID: int, finantialID: int, cashID: int, isPrintLog: bool = False) -> Cashflow:
    url = "{}:{}/company/{}/finantial/{}/cashflow/{}".format(HOST, PORT, companyID, finantialID, cashID)
    result = requests.get(url)
    cashflow: Cashflow = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getCashFlow] result: {}".format(cashflow))
    return cashflow


if __name__ == "__main__":
    # addCashFlow("test", 1, 3)
    # getCashFlow(1)
    getCashFlowList(1, 1)
