from typing import Any, List, Tuple
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api import yfinance, getCompanyList, addFinantialStatements, addBalanceSheet
from api.type import AddBalanceSheetRequestType, AddFinantialStatementsRequstType
from domain import FinantialStatements, Company, BalanceSheet

def generateDataWithYahooAPI() -> List[Tuple[FinantialStatements, BalanceSheet]]:
    companyList: List[Company] = getCompanyList()

    if type(companyList) is not list:
        raise ValueError('企業情報の取得に失敗しました')

    elif len(companyList) == 0:
        raise ValueError('企業情報が登録されていません')

    for company in companyList:
        ticker: Any = yfinance.getTickerWithYahooAPI(company)
        dateList: List[str] = yfinance.getCompanyDateWithTicker(ticker)


        # 各表のベースとなる財務諸表データを生成
        fsList: List[FinantialStatements] = []
        for date in dateList:
            fs = addFinantialStatements({"companyID": company['id'], "announcementDate": date, "isFiscal": True})
            fsList.append(fs)
        
        # 財務諸表データをベースにしたバランスシートデータを生成
        bsRequestList: List[AddBalanceSheetRequestType] = yfinance.getCompanyBSWithTicker(ticker, fsList)
        bsList: List[BalanceSheet] = []
        for bsRequest in bsRequestList:
            bs = addBalanceSheet(company['id'], bsRequest)
            bsList.append(bs)
        
        # 財務諸表データをベースにしたキャッシュ・フローデータを生成
        
        break



def generateFinantialStatementsData() -> List[FinantialStatements]:
    companyList: List[Company] = getCompanyList()

    if type(companyList) is not list:
        raise ValueError('企業情報の取得に失敗しました')

    elif len(companyList) == 0:
        raise ValueError('企業情報が登録されていません')


    companyListWithFSRequest: List[List[AddFinantialStatementsRequstType]] = []
    for company in companyList:
        companyListWithFSRequest.append(yfinance.getCompanyFSWithYahooAPI(company))

    result: List[FinantialStatements] = []
    for FSRequstList in companyListWithFSRequest:
        for request in FSRequstList:
            result.append(addFinantialStatements(request))
    
    return result


if __name__ == "__main__":
    # generateFinantialStatementsData()
    generateDataWithYahooAPI()