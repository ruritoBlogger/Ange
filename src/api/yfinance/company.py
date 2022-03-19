from re import S
import yfinance as yf
from typing import Any, List, Dict, Optional
import pandas as pd
import sys
import os
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from api import AddFinantialStatementsRequstType, AddBalanceSheetRequestType, AddCashFlowRequestType, AddIncomeStatementRequestType, AddIndexRequestType, AddStockPriceRequestType
from .tickerHandler import TickerHandler
from domain import FinantialStatements, Company
from util import convertDateFromJS

def convertDate(target: str) -> str:
    return target.strftime("%Y/%m/%d")

# TODO: 4半期毎のデータも取得出来るようにする

def getCompanyDate(handler: TickerHandler) -> List[str]:
    balanceSheet: pd.DataFrame = handler.getBalanceSheet()

    dateList: List[str] = []
    for date, _ in balanceSheet.iteritems():
        dateList.append(convertDate(date))

    return dateList

def getCompanyBS(handler: TickerHandler, finantialStatements: List[FinantialStatements], stockAmountList: List[Dict[str, int]]) -> List[AddBalanceSheetRequestType]:
    balanceSheet: pd.DataFrame = handler.getBalanceSheet()

    result: List[AddBalanceSheetRequestType] = []
    for date, item in balanceSheet.iteritems():

        # TODO: 例外が発生する原因を突き止める
        try:
            relatedFS: FinantialStatements = next(x for x in finantialStatements if x["announcementDate"][:7] == date.strftime("%Y-%m"))
        except StopIteration:
            print("BalanceSheetに関連するFinantialStatementsが取得出来てません")
            print("BalanceSheet: {}".format(balanceSheet))
            print("FinantialStatementsList: {}".format(finantialStatements))
            raise StopIteration

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

def getCompanyCF(handler: TickerHandler, finantialStatements: List[FinantialStatements]) -> List[AddCashFlowRequestType]:
    cashflow: pd.DataFrame = handler.getCashflow()

    result: List[AddCashFlowRequestType] = []
    for date, item in cashflow.iteritems():

        # TODO: 例外が発生する原因を突き止める
        try:
            relatedFS: FinantialStatements = next(x for x in finantialStatements if x["announcementDate"][:7] == date.strftime("%Y-%m"))
        except StopIteration:
            print("Cashflowに関連するFinantialStatementsが取得出来てません")
            print("Cashflow: {}".format(cashflow))
            print("FinantialStatementsList: {}".format(finantialStatements))
            raise StopIteration

        cashflow: AddCashFlowRequestType = { "finantialID":  relatedFS["id"]}
        cashflow["salesCF"] = item["Change To Operating Activities"]
        cashflow["investmentCF"] = item["Total Cashflows From Investing Activities"]
        cashflow["financialCF"] = item["Total Cash From Financing Activities"]

        result.append(cashflow)

    return result

def getCompanyIS(handler: TickerHandler, finantialStatements: List[FinantialStatements]) -> List[AddIncomeStatementRequestType]:
    incomeStatement: pd.DataFrame = handler.getIncomeStatement()
    result: List[AddIncomeStatementRequestType] = []

    for date, item in incomeStatement.iteritems():

        # TODO: 例外が発生する原因を突き止める
        try:
            relatedFS: FinantialStatements = next(x for x in finantialStatements if x["announcementDate"][:7] == date.strftime("%Y-%m"))
        except StopIteration:
            print("IncomeStatementに関連するFinantialStatementsが取得出来てません")
            print("IncomeStatement: {}".format(incomeStatement))
            print("FinantialStatementsList: {}".format(finantialStatements))
            raise StopIteration

        incomeStatement: AddIncomeStatementRequestType = { "finantialID":  relatedFS["id"]}
        incomeStatement["totalSales"] = item["Cost Of Revenue"] + item["Gross Profit"]
        incomeStatement["operatingIncome"] = item["Operating Income"]
        incomeStatement["ordinaryIncome"] = item["Total Revenue"]
        incomeStatement["netIncome"] = item["Net Income"]

        result.append(incomeStatement)
    
    return result

def getCompanyStockPrice(handler: TickerHandler, company: Company) -> List[AddStockPriceRequestType]: 
    stockPrice: pd.DataFrame = handler.getStockPrice()
    result: List[AddStockPriceRequestType] = []

    for date, item in stockPrice.iterrows():
        stockPrice: AddStockPriceRequestType = { "companyID": company["id"]}
        stockPrice["openingPrice"] = item["Open"]
        stockPrice["closingPrice"] = item["Close"]
        stockPrice["highPrice"] = item["High"]
        stockPrice["lowPrice"] = item["Low"]
        stockPrice["date"] = convertDate(date)
        result.append(stockPrice)
    
    return result

def getCompanyStockAmount(handler: TickerHandler, dateList: List[str] ) -> Optional[List[Dict[str, int]]]:
    """現在の株式数及び分割情報を用いて過去の株式数を算出し返却する
    

    Args:
        ticker (Any): yfinance周りの情報を保持しているオブジェクト
        dateList (List[str]): 取得したい過去の年月

    Returns:
        Optional[List[Dict[str, int]]]:
        過去の年月をキーに株式数をデータに割り当てた辞書
        現在の発行部数が取得出来ない場合はNoneが返却される

        ex:
            {
                "YYYY/mm/dd": "stock amount(number)",
                "YYYY/mm/dd": "stock amout(number)",
            }
    """

    info: Dict[str, Any] = handler.getInfo()
    if "sharesOutstanding" not in info:
        return None
    currentStockAmount = info["sharesOutstanding"]

    splits: pd.DataFrame = handler.getSplits()
    stockAmountData: List[Dict[str, int]] = []

    for splitDate, splitRate in splits.iteritems():
        for targetDate in dateList:
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