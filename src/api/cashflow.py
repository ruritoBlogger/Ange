import json
from typing import List
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import Cashflow
from api.type import AddCashFlowRequestType


def addCashFlow(companyID: int, props: AddCashFlowRequestType, isPrintLog: bool = False) -> Cashflow:
    url = "http://localhost:3000/company/{}/finantial/{}/cashflow".format(companyID, props["finantialID"])
    result = requests.post(url, json=({"props": props}))
    cashflow: Cashflow = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[addCashFlow] result: {}".format(cashflow))
    return cashflow

def getCashFlowList(companyID: int, finantialID: int, isPrintLog: bool = False) -> List[Cashflow]:
    url = "http://localhost:3000/company/{}/finantial/{}/cashflow".format(companyID, finantialID)
    result = requests.get(url)
    cashflowList: List[Cashflow] = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getCashFlowList] result: {}".format(cashflowList))
    return cashflowList


def getCashFlow(companyID: int, finantialID: int, cashID: int, isPrintLog: bool = False) -> Cashflow:
    url = "http://localhost:3000/company/{}/finantial/{}/cashflow/{}".format(companyID, finantialID, cashID)
    result = requests.get(url)
    cashflow: Cashflow = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getCashFlow] result: {}".format(cashflow))
    return cashflow


if __name__ == "__main__":
    # addCashFlow("test", 1, 3)
    # getCashFlow(1)
    getCashFlowList(1, 1)
