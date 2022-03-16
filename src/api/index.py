import json
from typing import List, Optional
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import Index
from api.type import AddIndexRequestType


def addIndex(companyID: int, props: AddIndexRequestType, isPrintLog: bool = False) -> Optional[Index]:
    url = "http://localhost:3000/company/{}/finantial/{}/index".format(companyID, props["finantialID"])
    result = requests.post(url, json=({"props": props}))
    index: Index = json.loads(result.content.decode('utf-8'))

    # 正常に情報を取得出来なかった場合の処理
    # FIXME: 本当は情報を取得する部分で実装すべき
    if "capitalAdequacyRatio" not in index:
        return None

    if isPrintLog:
        print("[addIndex] result: {}".format(index))
    return index

def getIndexList(companyID: int, finantialID: int, isPrintLog: bool = False) -> List[Index]:
    url = "http://localhost:3000/company/{}/finantial/{}/index".format(companyID, finantialID)
    result = requests.get(url)
    indexList: List[Index] = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getIndexList] result: {}".format(indexList))
    return indexList


def getIndex(companyID: int, finantialID: int, indexID: int, isPrintLog: bool = False) -> Index:
    url = "http://localhost:3000/company/{}/finantial/{}/index/{}".format(companyID, finantialID, indexID)
    result = requests.get(url)
    index: Index = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getIndex] result: {}".format(index))
    return index


if __name__ == "__main__":
    # addIndex("test", 1, 3)
    # getIndex(1)
    getIndexList(1, 1)
