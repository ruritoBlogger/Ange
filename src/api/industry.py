import json
from typing import List
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import Industry
from api.type import AddIndustryRequestType


def addIndustry(props: AddIndustryRequestType, isPrintLog: bool = False) -> Industry:
    url = "http://localhost:3000/industry"
    result = requests.post(url, json=({"props": props}))
    industry: Industry = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[addIndustry] result: {}".format(industry))
    return industry


def getIndustryList(isPrintLog: bool = False) -> List[Industry]:
    url = "http://localhost:3000/industry"
    result = requests.get(url)
    industryList: List[Industry] = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getIndustryList] result: {}".format(industryList))
    return industryList


if __name__ == "__main__":
    getIndustryList()
