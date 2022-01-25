import yfinance as yf
from typing import List
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from domain import IndustryType, IndustryName
from api import addIndustry


def generateIndustryData() -> List[IndustryType]:
    industryList: List[IndustryType] = []
    for industry in IndustryName:
        result = addIndustry(industry.value)
        industryList.append(result)

    return industryList


if __name__ == "__main__":
    generateIndustryData()
