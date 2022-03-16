import json
from typing import List, Optional
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import IncomeStatement
from api.type import AddIncomeStatementRequestType


def addIncomeStatement(companyID: int, props: AddIncomeStatementRequestType, isPrintLog: bool = False) -> Optional[IncomeStatement]:
    url = "http://localhost:3000/company/{}/finantial/{}/income".format(companyID, props["finantialID"])

    try:
        result = requests.post(url, json=({"props": props}))
    except requests.exceptions.InvalidJSONError:
        return None

    incomeStatement: IncomeStatement = json.loads(result.content.decode('utf-8'))
    # 正常に情報を取得出来なかった場合の処理
    # FIXME: 本当は情報を取得する部分で実装すべき
    if "finantialID" not in incomeStatement:
        return None

    if isPrintLog:
        print("[addIncomeStatement] result: {}".format(incomeStatement))
    return incomeStatement

def getIncomeStatementList(companyID: int, finantialID: int, isPrintLog: bool = False) -> List[IncomeStatement]:
    url = "http://localhost:3000/company/{}/finantial/{}/income".format(companyID, finantialID)
    result = requests.get(url)
    incomeStatementList: List[IncomeStatement] = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getIncomeStatementList] result: {}".format(incomeStatementList))
    return incomeStatementList


def getIncomeStatement(companyID: int, finantialID: int, incomeID: int, isPrintLog: bool = False) -> IncomeStatement:
    url = "http://localhost:3000/company/{}/finantial/{}/income/{}".format(companyID, finantialID, incomeID)
    result = requests.get(url)
    incomeStatement: IncomeStatement = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getIncomeStatement] result: {}".format(incomeStatement))
    return incomeStatement


if __name__ == "__main__":
    # addIncomeStatement("test", 1, 3)
    # getIncomeStatement(1)
    getIncomeStatementList(1, 1)
