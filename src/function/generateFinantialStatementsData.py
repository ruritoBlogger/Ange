from typing import Any, List, Tuple, Dict, Optional
import sys
import os
from tqdm import tqdm
import itertools

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api import yfinance, getCompanyList, addFinantialStatements, addBalanceSheet, addCashFlow, addIncomeStatement, addIndex, addPrice, getFinantialStatementsList, getBalanceSheetList, getCashFlowList, getIncomeStatementList, getPriceList, getIndexList
from api.type import AddBalanceSheetRequestType, AddFinantialStatementsRequstType, AddCashFlowRequestType, AddIncomeStatementRequestType, AddIndexRequestType, AddStockPriceRequestType
from domain import FinantialStatements, Company, BalanceSheet, Cashflow, IncomeStatement, Index, StockPrice
from util import convertDateFromJS
from validator import validateFS, validateBS, validateCF, validateIndex, validateIS, validateStockPrice


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
    indexRequestList: List[AddIndexRequestType] = []
    for finantialStatement in fsList:
        try:
            relatedBS = next(x for x in bsList if x['finantialID'] == finantialStatement['id'])
            relatedIS = next(x for x in isList if x['finantialID'] == finantialStatement['id'])
        except StopIteration:
            continue

        indexRequest: AddIndexRequestType = { "finantialID": finantialStatement['id'] }
        indexRequest['capitalAdequacyRatio'] = relatedBS['netAssets'] / relatedBS['totalAssets']
        indexRequest['roe'] = relatedIS['netIncome'] / relatedBS['netAssets'] * 100
        indexRequest['roa'] = relatedIS['netIncome'] / relatedBS['totalAssets'] * 100

        relatedSP: StockPrice = choiceStockPriceWithAnnouncementDate(finantialStatement['announcementDate'], spList)
        if relatedSP is None:
            continue

        indexRequest['eps'] = relatedBS['printedNum'] / relatedIS['netIncome']
        indexRequest['per'] = relatedSP['closingPrice'] * indexRequest['eps']
        indexRequest['pbr'] = relatedSP['closingPrice'] * relatedBS['printedNum'] / relatedBS['netAssets']

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

        print("{} の情報を生成開始".format(company['name']))
        fsList: List[FinantialStatements] = getFinantialStatementsList(company['id'])
        spList: List[StockPrice] = getPriceList(company['id'])

        bsList: List[BalanceSheet] = []
        for fs in fsList:
            bsList.append(getBalanceSheetList(company['id'], fs['id']))
        # FIXME: 邪悪
        # flatten
        bsList = list(itertools.chain.from_iterable(bsList))

        cfList: List[Cashflow] = []
        for fs in fsList:
            cfList.append(getCashFlowList(company['id'], fs['id']))
        # flatten
        cfList = list(itertools.chain.from_iterable(cfList))

        isList: List[IncomeStatement] = []
        for fs in fsList:
            isList.append(getIncomeStatementList(company['id'], fs['id']))
        # flatten
        isList = list(itertools.chain.from_iterable(isList))

        indexList: List[Index] = []
        for fs in fsList:
            indexList.append(getIndexList(company['id'], fs['id']))
        # flatten
        indexList = list(itertools.chain.from_iterable(indexList))

        # 既に生成済みの場合はスキップ
        if( len(indexList) != 0 ):
            companyListBar.update(1)
            continue

        # yfinance APIを叩く準備
        handler: yfinance.TickerHandler = yfinance.TickerHandler()
        handler.registTicker(company)

        dateList: Optional[List[str]] = yfinance.getCompanyDate(handler)
        if dateList is None:
            continue

        stockAmountList: Optional[List[Dict[str, int]]] = yfinance.getCompanyStockAmount(handler, dateList)
        if stockAmountList is None:
            continue

        # 株価データを生成
        spRequestList: List[AddStockPriceRequestType] = yfinance.getCompanyStockPrice(handler, company)

        stockPriceBar = tqdm(total = len(spRequestList))
        stockPriceBar.set_description("{}の株価情報を登録中".format(company['name']))
        for spRequest in spRequestList:
            stockPriceBar.update(1)
            sp = addPrice(spRequest)
            if sp is None:
                continue
            validateStockPrice(sp)
            spList.append(sp)

        # 各表のベースとなる財務諸表データを生成
        if(len(fsList) == 0):
            for date in dateList:
                fs = addFinantialStatements({"companyID": company['id'], "announcementDate": date, "isFiscal": True})
                validateFS(fs)
                fsList.append(fs)
        
        # 財務諸表データをベースにしたバランスシートデータを生成
        if(len(bsList) == 0): 
            bsRequestList: List[AddBalanceSheetRequestType] = yfinance.getCompanyBS(handler, fsList, stockAmountList)
            for bsRequest in bsRequestList:
                bs = addBalanceSheet(company['id'], bsRequest)
                if bs is None:
                    continue
                validateBS(bs)
                bsList.append(bs)
        
        # 財務諸表データをベースにしたキャッシュ・フローデータを生成
        if(len(cfList) == 0):
            cfRequestList: List[AddCashFlowRequestType] = yfinance.getCompanyCF(handler, fsList)
            for cfRequest in cfRequestList:
                cf = addCashFlow(company['id'], cfRequest)
                if cf is None:
                    continue
                validateCF(cf)
                cfList.append(cf)

        # 財務諸表データをベースにした損益計算書データを生成
        if(len(isList) == 0):
            isRequestList: List[AddIncomeStatementRequestType] = yfinance.getCompanyIS(handler, fsList)
            for isRequest in isRequestList:
                istatement = addIncomeStatement(company['id'], isRequest)
                if istatement is None:
                    continue
                validateIS(istatement)
                isList.append(istatement)

        # 財務諸表データをベースにした指標データを生成
        if(len(indexList) == 0):
            indexRequestList: List[AddIndexRequestType] = calcIndex(spList, fsList, bsList, cfList, isList)
            for indexRequest in indexRequestList:
                index = addIndex(company['id'], indexRequest)
                validateIndex(index)
                indexList.append(index)
        
        companyListBar.update(1)


if __name__ == "__main__":
    generateDataWithYahooAPI()