from re import S
import yfinance as yf
from typing import Any, List, Dict, Optional
from requests.exceptions import ConnectionError
import pandas as pd
import sys
import os
import time
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from api import AddFinantialStatementsRequstType, AddBalanceSheetRequestType, AddCashFlowRequestType, AddIncomeStatementRequestType, AddIndexRequestType, AddStockPriceRequestType
from domain import FinantialStatements, Company
from util import convertDateFromJS

def convertDate(target: str) -> str:
    return target.strftime("%Y/%m/%d")

def getTickerWithYahooAPI(company: Company) -> Any:
    requestBody = "{}.T".format(company["identificationCode"])
    try:
        ticker = yf.Ticker(requestBody)
    except ConnectionError:
        print("yfinanceのAPIサーバーにアクセスが集中しているため一時休止します(10秒)")
        time.sleep(10)
        return getTickerWithYahooAPI(company)

    return ticker


def getCompanyDateWithTicker(ticker: Any) -> List[str]:
    try:
        df: pd.DataFrame = ticker.balance_sheet
    except ConnectionError:
        print("yfinanceのAPIサーバーにアクセスが集中しているため一時休止します(10秒)")
        time.sleep(10)
        return getCompanyDateWithTicker(ticker)

    dateList: List[str] = []
    for date, _ in df.iteritems():
        dateList.append(convertDate(date))

    return dateList

def getCompanyQuarterlyDateWithTicker(ticker: Any) -> List[str]:
    try:
        df: pd.DataFrame = ticker.quarterly_balance_sheet
    except ConnectionError:
        print("yfinanceのAPIサーバーにアクセスが集中しているため一時休止します(10秒)")
        time.sleep(10)
        return getCompanyQuarterlyDateWithTicker(ticker)

    dateList: List[str] = []
    for date, _ in df.iteritems():
        dateList.append(convertDate(date))
    

def getCompanyBSWithTicker(ticker: Any, finantialStatements: List[FinantialStatements], stockAmountList: List[Dict[str, int]]) -> List[AddBalanceSheetRequestType]:
    try:
        df: pd.DataFrame = ticker.balance_sheet
    except ConnectionError:
        print("yfinanceのAPIサーバーにアクセスが集中しているため一時休止します(10秒)")
        time.sleep(10)
        return getCompanyBSWithTicker(ticker, finantialStatements, stockAmountList)

    result: List[AddBalanceSheetRequestType] = []
    for date, item in df.iteritems():
        try:
            relatedFS: FinantialStatements = next(x for x in finantialStatements if x["announcementDate"][:7] == date.strftime("%Y-%m"))
        except StopIteration:
            continue

        balanceSheet: AddBalanceSheetRequestType = { "finantialID":  relatedFS["id"]}
        balanceSheet["totalAssets"] = item["Total Assets"]
        balanceSheet["netAssets"] = item["Total Assets"] - item["Total Liab"]
        balanceSheet["capitalStock"] = item["Common Stock"]
        balanceSheet["profitSurplus"] = item["Retained Earnings"]

        """
        stockAmountListという以下のような株式発行数の情報のうち
        連動している財務諸表に登録されている日付と合致するキーの株式発行数を["printedNum"]に登録する

        {
            "日付": "発行数"
        }
        """    
        searchKey = convertDateFromJS(relatedFS["announcementDate"])

        balanceSheet["printedNum"] = None
        for stockAmount in stockAmountList:
            if searchKey.strftime("%Y/%m/%d") in stockAmount:
                balanceSheet["printedNum"] = stockAmount[searchKey.strftime("%Y/%m/%d")]
                break

        result.append(balanceSheet)
    
    return result

def getCompanyCFWithTicker(ticker: Any, finantialStatements: List[FinantialStatements]) -> List[AddCashFlowRequestType]:
    try:
        df: pd.DataFrame = ticker.cashflow
    except ConnectionError:
        print("yfinanceのAPIサーバーにアクセスが集中しているため一時休止します(10秒)")
        time.sleep(10)
        return getCompanyCFWithTicker(ticker, finantialStatements)

    result: List[AddCashFlowRequestType] = []
    for date, item in df.iteritems():
        try:
            relatedFS: FinantialStatements = next(x for x in finantialStatements if x["announcementDate"][:7] == date.strftime("%Y-%m"))
        except StopIteration:
            continue

        cashflow: AddCashFlowRequestType = { "finantialID":  relatedFS["id"]}
        cashflow["salesCF"] = item["Change To Operating Activities"]
        cashflow["investmentCF"] = item["Total Cashflows From Investing Activities"]
        cashflow["financialCF"] = item["Total Cash From Financing Activities"]

        result.append(cashflow)

    return result

def getCompanyISWithTicker(ticker: Any, finantialStatements: List[FinantialStatements]) -> List[AddIncomeStatementRequestType]:
    try:
        df: pd.DataFrame = ticker.financials
    except ConnectionError:
        print("yfinanceのAPIサーバーにアクセスが集中しているため一時休止します(10秒)")
        time.sleep(10)
        return getCompanyISWithTicker(ticker, finantialStatements)

    result: List[AddIncomeStatementRequestType] = []
    for date, item in df.iteritems():
        try:
            relatedFS: FinantialStatements = next(x for x in finantialStatements if x["announcementDate"][:7] == date.strftime("%Y-%m"))
        except StopIteration:
            continue

        incomeStatement: AddIncomeStatementRequestType = { "finantialID":  relatedFS["id"]}
        incomeStatement["totalSales"] = item["Cost Of Revenue"] + item["Gross Profit"]
        incomeStatement["operatingIncome"] = item["Operating Income"]
        incomeStatement["ordinaryIncome"] = item["Total Revenue"]
        incomeStatement["netIncome"] = item["Net Income"]

        result.append(incomeStatement)
    
    return result

def getCompanyStockPriceWithTicker(ticker: Any, company: Company) -> List[AddStockPriceRequestType]: 
    try:
        df: pd.DataFrame = ticker.history(period="max")
    except ConnectionError:
        print("yfinanceのAPIサーバーにアクセスが集中しているため一時休止します(10秒)")
        time.sleep(10)
        return getCompanyStockPriceWithTicker(ticker, company)

    result: List[AddStockPriceRequestType] = []
    for date, item in df.iterrows():
        stockPrice: AddStockPriceRequestType = { "companyID": company["id"]}
        stockPrice["openingPrice"] = item["Open"]
        stockPrice["closingPrice"] = item["Close"]
        stockPrice["highPrice"] = item["High"]
        stockPrice["lowPrice"] = item["Low"]
        stockPrice["date"] = convertDate(date)
        result.append(stockPrice)
    
    return result

@timeout_decorator.timeout(120)
def getCompanyStockAmountWithTicker(ticker: Any, dateList: List[str], cache: Optional[int] = None) -> Optional[List[Dict[str, int]]]:
    """現在の株式数及び分割情報を用いて過去の株式数を算出し返却する
    

    Args:
        ticker (Any): yfinance周りの情報を保持しているオブジェクト
        dateList (List[str]): 取得したい過去の年月

    Returns:
        List[Dict[str, int]]: 過去の年月をキーに株式数をデータに割り当てた辞書
            {
                "YYYY/mm/dd": "stock amount(number)",
                "YYYY/mm/dd": "stock amout(number)",
            }
    """

    # NOTE: 1回目のAPIアクセスに既に成功している場合 == cacheの中身に欲しい情報が格納済み
    if cache == None:
        try:
            currentStockAmount: int = ticker.info["sharesOutstanding"]
        except ConnectionError:
            print("yfinanceのAPIサーバーにアクセスが集中しているため一時休止します(10秒)")
            time.sleep(10)
            return getCompanyStockAmountWithTicker(ticker, dateList)
        except KeyError:
            return None

    try:
        splitData: pd.DataFrame = ticker.splits
    except ConnectionError:
            print("yfinanceのAPIサーバーにアクセスが集中しているため一時休止します(10秒)")
            time.sleep(10)
            return getCompanyStockAmountWithTicker(ticker, dateList, currentStockAmount)

    stockAmountData: List[Dict[str, int]] = []

    for splitDate, splitRate in splitData.iteritems():
        for targetDate in dateList:
            # FIXME: 終わり
            # if splitDate.strftime("%Y") > targetDate[:4] or (splitDate.strftime("%Y") == targetDate[:4] and int(float(splitDate.strftime("%m"))) >= int(float(targetDate[5:]))):
            if splitDate > datetime.strptime(targetDate, "%Y/%m/%d"):
                currentStockAmount = currentStockAmount / splitRate
            
            stockAmountData.append({targetDate: currentStockAmount})
    
    return stockAmountData

def getCompanyFSWithYahooAPI(company: Company) -> List[AddFinantialStatementsRequstType]:
    requestBody = "{}.T".format(company["identificationCode"])
    response = yf.Ticker(requestBody)

    result: List[AddFinantialStatementsRequstType] = []
    df: pd.DataFrame = response.financials
    for date, _ in df.iteritems():
        finantialStatements: AddFinantialStatementsRequstType = { "companyID": company["id"], "announcementDate": convertDate(date), "isFiscal": True }
        result.append(finantialStatements)

    return result


if __name__ == "__main__":
    getCompanyWithYahooAPI(9984, 1)