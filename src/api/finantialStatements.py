import json
from typing import List, Optional
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import FinantialStatements
from api.type import AddFinantialStatementsRequstType


def addFinantialStatements(props: AddFinantialStatementsRequstType, isPrintLog: bool = False) -> Optional[FinantialStatements]:
    url = "http://localhost:3000/company/{}/finantial".format(props["companyID"])
    result = requests.post(url, json=({"props": props}))
    finantialStatements: FinantialStatements = json.loads(result.content.decode('utf-8'))

    # 正常に情報を取得出来なかった場合の処理
    # FIXME: 本当は情報を取得する部分で実装すべき
    if "announcementDate" not in finantialStatements:
        return None

    if isPrintLog:
        print("[addFinantialStatements] result: {}".format(finantialStatements))
    return finantialStatements

def getFinantialStatementsList(companyID: int, isPrintLog: bool = False) -> List[FinantialStatements]:
    url = "http://localhost:3000/company/{}/finantial".format(companyID)
    result = requests.get(url)
    finantialStatementsList: List[FinantialStatements] = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getFinantialStatementsList] result: {}".format(finantialStatementsList))
    return finantialStatementsList


def getFinantialStatements(companyID: int, finantialID: int, isPrintLog: bool = False) -> FinantialStatements:
    url = "http://localhost:3000/company/{}/finantial/{}".format(companyID, finantialID)
    result = requests.get(url)
    finantialStatements: FinantialStatements = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getFinantialStatements] result: {}".format(finantialStatements))
    return finantialStatements


if __name__ == "__main__":
    # addFinantialStatements("test", 1, 3)
    # getFinantialStatements(1)
    getFinantialStatementsList(1)
