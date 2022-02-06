from typing import List
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api import getCompanyList, addFinantialStatements
from api.type import AddFinantialStatementsRequstType
from api.yfinance import getCompanyFSWithYahooAPI
from domain import FinantialStatements, Company

def generateFinantialStatementsData() -> List[FinantialStatements]:
    companyList: List[Company] = getCompanyList()

    if type(companyList) is not list:
        raise ValueError('企業情報の取得に失敗しました')

    elif len(companyList) == 0:
        raise ValueError('企業情報が登録されていません')


    companyListWithFSRequest: List[List[AddFinantialStatementsRequstType]] = []
    for company in companyList:
        companyListWithFSRequest.append(getCompanyFSWithYahooAPI(company))

    result: List[FinantialStatements] = []
    for FSRequstList in companyListWithFSRequest:
        for request in FSRequstList:
            result.append(addFinantialStatements(request))
    
    return result


if __name__ == "__main__":
    generateFinantialStatementsData()