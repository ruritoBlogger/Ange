from typing import List, Dict, Union
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from downloadCompanyList import downloadCompanyList
from api import getIndustryList, addCompany
from api.type import AddCompanyRequestType
from domain import Industry

def generateCompanyData():
    industryList: List[Industry] = getIndustryList()

    if type(industryList) is not list:
        raise ValueError('業種情報の取得に失敗しました')

    elif len(industryList) == 0:
        raise ValueError('業種情報が登録されていません')
    

    companyList: List[AddCompanyRequestType] = downloadCompanyList(industryList)
    for company in companyList:
        addCompany(company)




if __name__ == "__main__":
    generateCompanyData()