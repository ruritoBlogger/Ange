import json
from typing import List
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import BalanceSheet
from api.type import AddBalanceSheetRequestType


def addBalanceSheet(companyID: int, props: AddBalanceSheetRequestType) -> BalanceSheet:
    url = "http://localhost:3000/company/{}/finantial/{}/sheet".format(companyID, props["finantialID"])
    result = requests.post(url, json=({"props": props}))
    balanceSheet: BalanceSheet = json.loads(result.content.decode('utf-8'))
    print("[addBalanceSheet] result: {}".format(balanceSheet))
    return balanceSheet

def getBalanceSheetList(companyID: int, finantialID: int) -> List[BalanceSheet]:
    url = "http://localhost:3000/company/{}/finantial/{}/sheet".format(companyID, finantialID)
    result = requests.get(url)
    balanceSheetList: List[BalanceSheet] = json.loads(result.content.decode('utf-8'))
    print("[getBalanceSheetList] result: {}".format(balanceSheetList))
    return balanceSheetList


def getBalanceSheet(companyID: int, finantialID: int, sheetID: int) -> BalanceSheet:
    url = "http://localhost:3000/company/{}/finantial/{}/sheet/{}".format(companyID, finantialID, sheetID)
    result = requests.get(url)
    balanceSheet: BalanceSheet = json.loads(result.content.decode('utf-8'))
    print("[getBalanceSheet] result: {}".format(balanceSheet))
    return balanceSheet


if __name__ == "__main__":
    # addBalanceSheet("test", 1, 3)
    # getBalanceSheet(1)
    getBalanceSheetList(1, 1)
