from typing import List
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import Industry, IndustryName, IndustryCodeForMyKabu
from function import scrapingCompanyByIndustry
from api import getIndustryList

def generateCompanyData():
    industryList: List[Industry] = getIndustryList()

    for industry in industryList:
        industryKey: IndustryName = IndustryName.convertFromStr(industry["name"])
        scrapingCompanyByIndustry(industry["id"], IndustryCodeForMyKabu.convertFromIndustryName(industryKey))
        
        # NOTE: スクレイピング先に負荷を掛けない用
        time.sleep(2)



if __name__ == "__main__":
    generateCompanyData()