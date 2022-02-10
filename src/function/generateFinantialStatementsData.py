from typing import Any, List, Tuple
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api import yfinance, getCompanyList, addFinantialStatements, addBalanceSheet, addCashFlow, addIncomeStatement, addIndex
from api.type import AddBalanceSheetRequestType, AddFinantialStatementsRequstType, AddCashFlowRequestType, AddIncomeStatementRequestType, AddIndexRequestType
from domain import FinantialStatements, Company, BalanceSheet, Cashflow, IncomeStatement, Index


# TODO: 株価データを扱えるようになったら実装する
"""
def calcIndex(ticker, Any, fsList: List[FinantialStatements], bsList: List[BalanceSheet], cfList: List[Cashflow], isList: List[IncomeStatement]) -> List[AddIndexRequestType]:
    listLen = len(fsList)

    indexRequestList: List[AddIndexRequestType] = []
    for i in range(listLen):
        indexRequest: AddIndexRequestType = { "finantialID": fsList[i]['id'] }
        indexRequest['capitalAdequacyRatio'] = bsList[i]['netAssets'] / bsList[i]['totalAssets']
        indexRequest['roe'] = isList[i]['netIncome'] / bsList[i]['netAssets'] * 100
        indexRequest['roa'] = isList[i]['netIncome'] / bsList[i]['totalAssets'] * 100
"""


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
        cfRequestList: List[AddCashFlowRequestType] = yfinance.getCompanyCFWithTicker(ticker, fsList)
        cfList: List[Cashflow] = []
        for cfRequest in cfRequestList:
            cf = addCashFlow(company['id'], cfRequest)
            cfList.append(cf)

        # 財務諸表データをベースにした損益計算書データを生成
        isRequestList: List[AddIncomeStatementRequestType] = yfinance.getCompanyISWithTicker(ticker, fsList)
        isList: List[IncomeStatement] = []
        for isRequest in isRequestList:
            istatement = addIncomeStatement(company['id'], isRequest)
            isList.append(istatement)

        # TODO: 株価データを取り扱えるようになったら実装する
        """
        # 財務諸表データをベースにした指標データを生成
        indexRequestList: List[AddIndexRequestType] = calcIndex(fsList, bsList, cfList, isList)
        indexList: List[Index] = []
        for indexRequest in indexRequestList:
            index = addIndex(company['id'], indexRequest)
            indexList.append(index)
        """
        
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