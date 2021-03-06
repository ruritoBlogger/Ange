import json
from typing import List
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import FinantialStatements
from api.type import AddFinantialStatementsRequstType

HOST = os.getenv("TOKO_HOST")
PORT = os.getenv("TOKO_PORT")

def addFinantialStatements(props: AddFinantialStatementsRequstType, isPrintLog: bool = False) -> FinantialStatements:
    url = "{}:{}/company/{}/finantial".format(HOST, PORT, props["companyID"])
    result = requests.post(url, json=({"props": props}))
    finantialStatements: FinantialStatements = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[addFinantialStatements] result: {}".format(finantialStatements))

    return finantialStatements

def getFinantialStatementsList(companyID: int, isPrintLog: bool = False) -> List[FinantialStatements]:
    url = "{}:{}/company/{}/finantial".format(HOST, PORT, companyID)
    result = requests.get(url)
    finantialStatementsList: List[FinantialStatements] = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getFinantialStatementsList] result: {}".format(finantialStatementsList))
    return finantialStatementsList


def getFinantialStatements(companyID: int, finantialID: int, isPrintLog: bool = False) -> FinantialStatements:
    url = "{}:{}/company/{}/finantial/{}".format(HOST, PORT, companyID, finantialID)
    result = requests.get(url)
    finantialStatements: FinantialStatements = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getFinantialStatements] result: {}".format(finantialStatements))
    return finantialStatements


if __name__ == "__main__":
    # addFinantialStatements("test", 1, 3)
    # getFinantialStatements(1)
    getFinantialStatementsList(1)
