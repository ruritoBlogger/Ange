from typing import List, Set
import sys
import os
import pandas as pd
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from domain import Industry
from api import addIndustry, AddIndustryRequestType


def generateIndustryData() -> List[Industry]:
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    result = requests.get(url)
    df = pd.read_excel(result.content)['33業種区分']

    industrySet: Set[str] = set()
    for data in df:
        industrySet.add(data)

    # NOTE: ETFなどの業種区分が存在しないケースを考慮
    industrySet.remove('-')

    industryList: List[Industry] = []
    for name in industrySet:
        props: AddIndustryRequestType = { "name" : name}
        industryList.append(addIndustry(props))

    return industryList


if __name__ == "__main__":
    generateIndustryData()
