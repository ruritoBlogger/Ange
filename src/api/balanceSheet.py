import json
from typing import List, Optional
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import BalanceSheet
from api.type import AddBalanceSheetRequestType

HOST = os.getenv("TOKO_URL")
PORT = os.getenv("TOKO_PORT")

def addBalanceSheet(companyID: int, props: AddBalanceSheetRequestType, isPrintLog: bool = False) -> Optional[BalanceSheet]:
    url = "{}:{}/company/{}/finantial/{}/sheet".format(HOST, PORT, companyID, props["finantialID"])
    try:
        result = requests.post(url, json=({"props": props}))
    except requests.exceptions.InvalidJSONError:
        # NOTE: いずれかの情報がyfinance APIから取得出来ていない場合
        return None

    balanceSheet: BalanceSheet = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[addBalanceSheet] result: {}".format(balanceSheet))
    return balanceSheet

def getBalanceSheetList(companyID: int, finantialID: int, isPrintLog: bool = False) -> List[BalanceSheet]:
    url = "{}:{}/company/{}/finantial/{}/sheet".format(HOST, PORT, companyID, finantialID)
    result = requests.get(url)
    balanceSheetList: List[BalanceSheet] = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getBalanceSheetList] result: {}".format(balanceSheetList))
    return balanceSheetList


def getBalanceSheet(companyID: int, finantialID: int, sheetID: int, isPrintLog: bool = False) -> BalanceSheet:
    url = "{}:{}/company/{}/finantial/{}/sheet/{}".format(HOST, PORT, companyID, finantialID, sheetID)
    result = requests.get(url)
    balanceSheet: BalanceSheet = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getBalanceSheet] result: {}".format(balanceSheet))
    return balanceSheet


if __name__ == "__main__":
    # addBalanceSheet("test", 1, 3)
    # getBalanceSheet(1)
    getBalanceSheetList(1, 1)
