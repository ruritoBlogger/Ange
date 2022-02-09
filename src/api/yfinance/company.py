from ast import Add
from domain.balanceSheet import BalanceSheet
import yfinance as yf
from typing import Any, List
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from api import AddFinantialStatementsRequstType, AddBalanceSheetRequestType
from domain import FinantialStatements, Company

def getTickerWithYahooAPI(company: Company) -> Any:
    requestBody = "{}.T".format(company["identificationCode"])
    ticker = yf.Ticker(requestBody)
    return ticker


def getCompanyDateWithTicker(ticker: Any) -> List[str]:
    df: pd.DataFrame = ticker.balance_sheet
    dateList: List[str] = []
    for date, _ in df.iteritems():
        dateList.append(date.strftime("%Y/%m/%d"))

    return dateList

def getCompanyQuarterlyDateWithTicker(ticker: Any) -> List[str]:
    df: pd.DataFrame = ticker.quarterly_balance_sheet
    dateList: List[str] = []
    for date, _ in df.iteritems():
        dateList.append(date.strftime("%Y/%m/%d"))
    

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


def getCompanyFSWithYahooAPI(company: Company) -> List[AddFinantialStatementsRequstType]:
    requestBody = "{}.T".format(company["identificationCode"])
    response = yf.Ticker(requestBody)

    result: List[AddFinantialStatementsRequstType] = []
    df: pd.DataFrame = response.financials
    for date, _ in df.iteritems():
        convertedDate = date.strftime("%Y/%m/%d")
        finantialStatements: AddFinantialStatementsRequstType = { "companyID": company["id"], "announcementDate": convertedDate, "isFiscal": True }
        result.append(finantialStatements)

    return result


if __name__ == "__main__":
    getCompanyWithYahooAPI(9984, 1)