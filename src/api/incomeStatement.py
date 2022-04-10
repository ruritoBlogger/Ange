import json
from typing import List, Optional
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import IncomeStatement
from api.type import AddIncomeStatementRequestType

HOST = os.getenv("TOKO_HOST")
PORT = os.getenv("TOKO_PORT")

def addIncomeStatement(companyID: int, props: AddIncomeStatementRequestType, isPrintLog: bool = False) -> Optional[IncomeStatement]:
    url = "{}:{}/company/{}/finantial/{}/income".format(HOST, PORT, companyID, props["finantialID"])
    try:
        result = requests.post(url, json=({"props": props}))
    except requests.exceptions.InvalidJSONError:
        # NOTE: いずれかの情報がyfinance APIから取得出来ていない場合
        return None
        
    incomeStatement: IncomeStatement = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[addIncomeStatement] result: {}".format(incomeStatement))
    return incomeStatement

def getIncomeStatementList(companyID: int, finantialID: int, isPrintLog: bool = False) -> List[IncomeStatement]:
    url = "{}:{}/company/{}/finantial/{}/income".format(HOST, PORT, companyID, finantialID)
    result = requests.get(url)
    incomeStatementList: List[IncomeStatement] = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getIncomeStatementList] result: {}".format(incomeStatementList))
    return incomeStatementList


def getIncomeStatement(companyID: int, finantialID: int, incomeID: int, isPrintLog: bool = False) -> IncomeStatement:
    url = "{}:{}/company/{}/finantial/{}/income/{}".format(HOST, PORT, companyID, finantialID, incomeID)
    result = requests.get(url)
    incomeStatement: IncomeStatement = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getIncomeStatement] result: {}".format(incomeStatement))
    return incomeStatement


if __name__ == "__main__":
    # addIncomeStatement("test", 1, 3)
    # getIncomeStatement(1)
    getIncomeStatementList(1, 1)
