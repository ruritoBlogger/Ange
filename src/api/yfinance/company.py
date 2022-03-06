from ast import Add
import yfinance as yf
from typing import Any, List
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from api import AddFinantialStatementsRequstType, AddBalanceSheetRequestType, AddCashFlowRequestType, AddIncomeStatementRequestType, AddIndexRequestType, AddStockPriceRequestType
from domain import FinantialStatements, Company

def convertDate(target: str) -> str:
    return target.strftime("%Y/%m/%d")

def getTickerWithYahooAPI(company: Company) -> Any:
    requestBody = "{}.T".format(company["identificationCode"])
    ticker = yf.Ticker(requestBody)
    return ticker


def getCompanyDateWithTicker(ticker: Any) -> List[str]:
    df: pd.DataFrame = ticker.balance_sheet
    dateList: List[str] = []
    for date, _ in df.iteritems():
        dateList.append(convertDate(date))

    return dateList

def getCompanyQuarterlyDateWithTicker(ticker: Any) -> List[str]:
    df: pd.DataFrame = ticker.quarterly_balance_sheet
    dateList: List[str] = []
    for date, _ in df.iteritems():
        dateList.append(convertDate(date))
    

def getCompanyBSWithTicker(ticker: Any, finantialStatements: List[FinantialStatements]) -> List[AddBalanceSheetRequestType]:
    df: pd.DataFrame = ticker.balance_sheet
    result: List[AddBalanceSheetRequestType] = []
    for date, item in df.iteritems():
        relatedFS: FinantialStatements = next(x for x in finantialStatements if x["announcementDate"][:7] == date.strftime("%Y-%m"))
        balanceSheet: AddBalanceSheetRequestType = { "finantialID":  relatedFS["id"]}
        balanceSheet["totalAssets"] = item["Total Assets"]
        balanceSheet["netAssets"] = item["Total Assets"] - item["Total Liab"]
        balanceSheet["capitalStock"] = item["Common Stock"]
        balanceSheet["profitSurplus"] = item["Retained Earnings"]

        result.append(balanceSheet)
    
    return result

def getCompanyCFWithTicker(ticker: Any, finantialStatements: List[FinantialStatements]) -> List[AddCashFlowRequestType]:
    df: pd.DataFrame = ticker.cashflow
    result: List[AddCashFlowRequestType] = []
    for date, item in df.iteritems():
        relatedFS: FinantialStatements = next(x for x in finantialStatements if x["announcementDate"][:7] == date.strftime("%Y-%m"))
        cashflow: AddCashFlowRequestType = { "finantialID":  relatedFS["id"]}
        cashflow["salesCF"] = item["Change To Operating Activities"]
        cashflow["investmentCF"] = item["Total Cashflows From Investing Activities"]
        cashflow["financialCF"] = item["Total Cash From Financing Activities"]

        result.append(cashflow)

    return result

def getCompanyISWithTicker(ticker: Any, finantialStatements: List[FinantialStatements]) -> List[AddIncomeStatementRequestType]:
    df: pd.DataFrame = ticker.financials
    result: List[AddIncomeStatementRequestType] = []
    for date, item in df.iteritems():
        relatedFS: FinantialStatements = next(x for x in finantialStatements if x["announcementDate"][:7] == date.strftime("%Y-%m"))
        incomeStatement: AddIncomeStatementRequestType = { "finantialID":  relatedFS["id"]}
        incomeStatement["totalSales"] = item["Cost Of Revenue"] + item["Gross Profit"]
        incomeStatement["operatingIncome"] = item["Operating Income"]
        incomeStatement["ordinaryIncome"] = item["Total Revenue"]
        incomeStatement["netIncome"] = item["Net Income"]

        result.append(incomeStatement)
    
    return result

def getCompanyStockPriceWithTicker(ticker: Any, company: Company) -> List[AddStockPriceRequestType]: 
    df: pd.DataFrame = ticker.history(period="max")
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