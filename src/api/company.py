import json
from typing import List
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import Company, CompanyType


def addCompany(name: str, code: int, industryID: int) -> CompanyType:
    url = "http://localhost:3000/company"
    result = requests.post(url, json=({"props": {"name": name, "identificationCode": code, "industryID": industryID }}))
    company: Company = json.loads(result.content.decode('utf-8'))
    print("[addCompany] result: {}".format(company))
    return company

def getCompanyList() -> List[CompanyType]:
    url = "http://localhost:3000/company"
    result = requests.get(url)
    companyList: List[Company] = json.loads(result.content.decode('utf-8'))
    print("[getCompanyList] result: {}".format(companyList))
    return companyList


def updateCompany(id: int, name: str, code: int, industryID: int) -> CompanyType:
    url = "http://localhost:3000/company"
    result = requests.put(url, json=({"id": id, "props": {"name": name, "identificationCode": code, "industryID": industryID }}))
    company: Company = json.loads(result.content.decode('utf-8'))
    print("[updateCompany] result: {}".format(company))
    return company


def getCompany(id: int) -> CompanyType:
    url = "http://localhost:3000/company/{}".format(id)
    result = requests.get(url)
    company: Company = json.loads(result.content.decode('utf-8'))
    print("[getCompany] result: {}".format(company))
    return company


def deleteCompany(id: int) -> int:
    url = "http://localhost:3000/company/{}".format(id)
    result = requests.delete(url)
    company: Company = json.loads(result.content.decode('utf-8'))
    print("[deleteCompany] result: {}".format(company))
    return company


if __name__ == "__main__":
    # addCompany("test", 1, 3)
    # getCompany(1)
    getCompanyList()
