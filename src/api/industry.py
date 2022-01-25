import json
from typing import NoReturn
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import Industry, IndustryType


def addIndustry(name: str) -> NoReturn:
    url = "http://localhost:3000/industry"
    result = requests.post(url, json=({"props": {"name": name}}))
    print(result.content.decode('utf-8'))


def getIndustry(id: int) -> IndustryType:
    url = "http://localhost:3000/industry/{}".format(id)
    result = requests.get(url)
    industry: Industry = json.loads(result.content.decode('utf-8'))
    print(industry)


if __name__ == "__main__":
    # addIndustry("test")
    getIndustry(1)
