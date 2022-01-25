import json
from typing import List
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import Industry, IndustryType


def addIndustry(name: str) -> IndustryType:
    url = "http://localhost:3000/industry"
    result = requests.post(url, json=({"props": {"name": name}}))
    industry: Industry = json.loads(result.content.decode('utf-8'))
    print("[addIndustry] result: {}".format(industry))
    return result


def getIndustryList() -> List[IndustryType]:
    url = "http://localhost:3000/industry"
    result = requests.get(url)
    industryList: List[Industry] = json.loads(result.content.decode('utf-8'))
    print("[getIndustryList] result: {}".format(industryList))
    return industryList


def updateIndustry(id: int, name: str) -> IndustryType:
    url = "http://localhost:3000/industry"
    result = requests.put(url, json=({"props": {"id": id, "name": name}}))
    industry: Industry = json.loads(result.content.decode('utf-8'))
    print("[updateIndustry] result: {}".format(industry))
    return industry


def getIndustry(id: int) -> IndustryType:
    url = "http://localhost:3000/industry/{}".format(id)
    result = requests.get(url)
    industry: Industry = json.loads(result.content.decode('utf-8'))
    print("[getIndustry] result: {}".format(industry))
    return industry


def deleteIndustry(id: int) -> int:
    url = "http://localhost:3000/industry/{}".format(id)
    result = requests.delete(url)
    industry: Industry = json.loads(result.content.decode('utf-8'))
    print("[deleteIndustry] result: {}".format(industry))
    return industry


if __name__ == "__main__":
    # addIndustry("test")
    # getIndustry(1)
    getIndustryList()
