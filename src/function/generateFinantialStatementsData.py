from typing import Any, List, Tuple, Dict
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api import yfinance, getCompanyList, addFinantialStatements, addBalanceSheet, addCashFlow, addIncomeStatement, addIndex, addPrice
from api.type import AddBalanceSheetRequestType, AddFinantialStatementsRequstType, AddCashFlowRequestType, AddIncomeStatementRequestType, AddIndexRequestType, AddStockPriceRequestType
from domain import FinantialStatements, Company, BalanceSheet, Cashflow, IncomeStatement, Index, StockPrice


def calcIndex(ticker, Any, spList: List[StockPrice], fsList: List[FinantialStatements], bsList: List[BalanceSheet], cfList: List[Cashflow], isList: List[IncomeStatement]) -> List[AddIndexRequestType]:
    listLen = len(fsList)

    indexRequestList: List[AddIndexRequestType] = []
    for i in range(listLen):
        indexRequest: AddIndexRequestType = { "finantialID": fsList[i]['id'] }
        indexRequest['capitalAdequacyRatio'] = bsList[i]['netAssets'] / bsList[i]['totalAssets']
        indexRequest['roe'] = isList[i]['netIncome'] / bsList[i]['netAssets'] * 100
        indexRequest['roa'] = isList[i]['netIncome'] / bsList[i]['totalAssets'] * 100

        # FIXME: 邪悪 + 決算日の日付を取得して直す
        relatedSP: StockPrice = next(x for x in spList if x['date'] == fsList[i]['announcementDate'].strftime("%Y/%m/1"))
        # TODO: 株の発行部数を取得しておく
        # TODO: PCFRを削除する
        # TODO: yieldGapを削除する
        """
        indexRequest['eps'] = 発行部数 / isList[i]['netIncome']
        indexRequest['per'] = relatedSP["ClosingPrice"] * indexRequest['eps']
        indexRequest['pbr'] = relatedSP["ClosingPrice"] * 発行部数 / bsList[i]['netAssets']
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

        stockAmountList: List[Dict[str, int]] = yfinance.getCompanyStockAmountWithTicker(ticker, dateList)


        """
        # 株価データを生成
        spList: List[StockPrice] = []
        spRequestList: List[AddStockPriceRequestType] = yfinance.getCompanyStockPriceWithTicker(ticker, company)
        for spRequest in spRequestList:
            sp = addPrice(spRequest)
            spList.append(sp)
        """

        # 各表のベースとなる財務諸表データを生成
        fsList: List[FinantialStatements] = []
        for date in dateList:
            fs = addFinantialStatements({"companyID": company['id'], "announcementDate": date, "isFiscal": True})
            fsList.append(fs)
        
        # 財務諸表データをベースにしたバランスシートデータを生成
        bsRequestList: List[AddBalanceSheetRequestType] = yfinance.getCompanyBSWithTicker(ticker, fsList, stockAmountList)
        bsList: List[BalanceSheet] = []
        for bsRequest in bsRequestList:
            bs = addBalanceSheet(company['id'], bsRequest)
            bsList.append(bs)
        
        break
        
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

        # 財務諸表データをベースにした指標データを生成
        indexRequestList: List[AddIndexRequestType] = calcIndex(spList, fsList, bsList, cfList, isList)
        indexList: List[Index] = []
        for indexRequest in indexRequestList:
            index = addIndex(company['id'], indexRequest)
            indexList.append(index)
        
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