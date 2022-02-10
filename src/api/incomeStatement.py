import json
from typing import List
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import IncomeStatement
from api.type import AddIncomeStatementRequestType


def addIncomeStatement(companyID: int, props: AddIncomeStatementRequestType) -> IncomeStatement:
    print(props)
    url = "http://localhost:3000/company/{}/finantial/{}/income".format(companyID, props["finantialID"])
    result = requests.post(url, json=({"props": props}))
    incomeStatement: IncomeStatement = json.loads(result.content.decode('utf-8'))
    print("[addIncomeStatement] result: {}".format(incomeStatement))
    return incomeStatement

def getIncomeStatementList(companyID: int, finantialID: int) -> List[IncomeStatement]:
    url = "http://localhost:3000/company/{}/finantial/{}/income".format(companyID, finantialID)
    result = requests.get(url)
    incomeStatementList: List[IncomeStatement] = json.loads(result.content.decode('utf-8'))
    print("[getIncomeStatementList] result: {}".format(incomeStatementList))
    return incomeStatementList


def getIncomeStatement(companyID: int, finantialID: int, incomeID: int) -> IncomeStatement:
    url = "http://localhost:3000/company/{}/finantial/{}/income/{}".format(companyID, finantialID, incomeID)
    result = requests.get(url)
    incomeStatement: IncomeStatement = json.loads(result.content.decode('utf-8'))
    print("[getIncomeStatement] result: {}".format(incomeStatement))
    return incomeStatement


if __name__ == "__main__":
    # addIncomeStatement("test", 1, 3)
    # getIncomeStatement(1)
    getIncomeStatementList(1, 1)
