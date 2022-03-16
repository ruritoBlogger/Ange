import json
from typing import List
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import Company
from api.type import AddCompanyRequestType


def addCompany(props: AddCompanyRequestType, isPrintLog: bool = False) -> Company:
    url = "http://localhost:3000/company"
    result = requests.post(url, json=({"props": props}))
    company: Company = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[addCompany] result: {}".format(company))
    return company

def getCompanyList(isPrintLog: bool = False) -> List[Company]:
    url = "http://localhost:3000/company"
    result = requests.get(url)
    companyList: List[Company] = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getCompanyList] result: {}".format(companyList))
    return companyList


def getCompany(id: int, isPrintLog: bool = False) -> Company:
    url = "http://localhost:3000/company/{}".format(id)
    result = requests.get(url)
    company: Company = json.loads(result.content.decode('utf-8'))
    if isPrintLog:
        print("[getCompany] result: {}".format(company))
    return company


if __name__ == "__main__":
    # addCompany("test", 1, 3)
    getCompany(1)
    # getCompanyList()
