from typing import Any, List, Tuple, Dict, Optional
import sys
import os
from tqdm import tqdm

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api import yfinance, getCompanyList, addFinantialStatements, addBalanceSheet, addCashFlow, addIncomeStatement, addIndex, addPrice
from api.type import AddBalanceSheetRequestType, AddFinantialStatementsRequstType, AddCashFlowRequestType, AddIncomeStatementRequestType, AddIndexRequestType, AddStockPriceRequestType
from domain import FinantialStatements, Company, BalanceSheet, Cashflow, IncomeStatement, Index, StockPrice
from util import convertDateFromJS

def choiceStockPriceWithAnnouncementDate(announcementDate: str, spList: List[StockPrice]) -> Optional[StockPrice]:
    """決算日から一番近い && 決算日以降の日付の株情報を取得する

    Args:
        announcementDate (str): 決算日の情報
        spList (List[StockPrice]): 株価情報

    Returns:
        Optional[StockPrice]: 条件に該当する株価情報があればそれを、無ければNoneを返す
    """

    announcementDate = convertDateFromJS(announcementDate)

    for stockPrice in spList:
        priceDate = convertDateFromJS(stockPrice['date'])
        if announcementDate <= priceDate:
            return stockPrice

    return None

def calcIndex(spList: List[StockPrice], fsList: List[FinantialStatements], bsList: List[BalanceSheet], cfList: List[Cashflow], isList: List[IncomeStatement]) -> List[AddIndexRequestType]:
    listLen = len(fsList)

    indexRequestList: List[AddIndexRequestType] = []
    for i in range(listLen):
        indexRequest: AddIndexRequestType = { "finantialID": fsList[i]['id'] }
        indexRequest['capitalAdequacyRatio'] = bsList[i]['netAssets'] / bsList[i]['totalAssets']
        indexRequest['roe'] = isList[i]['netIncome'] / bsList[i]['netAssets'] * 100
        indexRequest['roa'] = isList[i]['netIncome'] / bsList[i]['totalAssets'] * 100

        relatedSP: StockPrice = choiceStockPriceWithAnnouncementDate(fsList[i]['announcementDate'], spList)
        indexRequest['eps'] = bsList[i]['printedNum'] / isList[i]['netIncome']
        indexRequest['per'] = relatedSP['closingPrice'] * indexRequest['eps']
        indexRequest['pbr'] = relatedSP['closingPrice'] * bsList[i]['printedNum'] / bsList[i]['netAssets']

        indexRequestList.append(indexRequest)
    
    return indexRequestList


def generateDataWithYahooAPI() -> List[Tuple[FinantialStatements, BalanceSheet]]:
    companyList: List[Company] = getCompanyList()
    companyListBar = tqdm(total = len(companyList))
    companyListBar.set_description('東証一部に上場している企業情報を生成中')

    if type(companyList) is not list:
        raise ValueError('企業情報の取得に失敗しました')

    elif len(companyList) == 0:
        raise ValueError('企業情報が登録されていません')

    for company in companyList:
        ticker: Any = yfinance.getTickerWithYahooAPI(company)
        dateList: List[str] = yfinance.getCompanyDateWithTicker(ticker)

        stockAmountList: List[Dict[str, int]] = yfinance.getCompanyStockAmountWithTicker(ticker, dateList)


        # 株価データを生成

        spList: List[StockPrice] = []
        spRequestList: List[AddStockPriceRequestType] = yfinance.getCompanyStockPriceWithTicker(ticker, company)

        stockPriceBar = tqdm(total = len(spRequestList))
        stockPriceBar.set_description("{}の株価情報を登録中".format(company['name']))
        for spRequest in spRequestList:
            sp = addPrice(spRequest)
            spList.append(sp)
            stockPriceBar.update(1)

        # 各表のベースとなる財務諸表データを生成
        fsList: List[FinantialStatements] = []
        for date in dateList:
            fs = addFinantialStatements({"companyID": company['id'], "announcementDate": date, "isFiscal": True})
            if fs is not None:
                fsList.append(fs)
        
        # 財務諸表データをベースにしたバランスシートデータを生成
        bsRequestList: List[AddBalanceSheetRequestType] = yfinance.getCompanyBSWithTicker(ticker, fsList, stockAmountList)
        bsList: List[BalanceSheet] = []
        for bsRequest in bsRequestList:
            bs = addBalanceSheet(company['id'], bsRequest)
            if bs is not None:
                bsList.append(bs)
        
        # 財務諸表データをベースにしたキャッシュ・フローデータを生成
        cfRequestList: List[AddCashFlowRequestType] = yfinance.getCompanyCFWithTicker(ticker, fsList)
        cfList: List[Cashflow] = []
        for cfRequest in cfRequestList:
            cf = addCashFlow(company['id'], cfRequest)
            if cf is not None:
                cfList.append(cf)

        # 財務諸表データをベースにした損益計算書データを生成
        isRequestList: List[AddIncomeStatementRequestType] = yfinance.getCompanyISWithTicker(ticker, fsList)
        isList: List[IncomeStatement] = []
        for isRequest in isRequestList:
            istatement = addIncomeStatement(company['id'], isRequest)
            if istatement is not None:
                isList.append(istatement)

        # 財務諸表データをベースにした指標データを生成
        indexRequestList: List[AddIndexRequestType] = calcIndex(spList, fsList, bsList, cfList, isList)
        indexList: List[Index] = []
        for indexRequest in indexRequestList:
            index = addIndex(company['id'], indexRequest)
            if index is not None:
                indexList.append(index)
        
        companyListBar.update(1)



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