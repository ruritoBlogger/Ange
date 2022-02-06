from ast import Add
from domain.balanceSheet import BalanceSheet
import yfinance as yf
from typing import Any, Tuple, List
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from api import AddFinantialStatementsRequstType, AddBalanceSheetRequestType
from domain import FinantialStatements, Company

def getCompanyWithYahooAPI(company: Company) -> List[Tuple[AddFinantialStatementsRequstType, AddBalanceSheetRequestType]]:
    requestBody = "{}.T".format(company["identificationCode"])
    response = yf.Ticker(requestBody)

    df: pd.DataFrame = response.financials
    for date, _ in df.iteritems():
        finantialStatements: AddFinantialStatementsRequstType = { "companyID": company["id"], "announcementDate": date.strftime("%Y/%m/%d"), "isFiscal": True }


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


def getCompanyBSWithYahooAPI(response: Any, finantialStatements: List[FinantialStatements]) -> List[AddBalanceSheetRequestType]:
    df: pd.DataFrame = response.balance_sheet
    result: List[AddBalanceSheetRequestType] = []
    for date, item in df.iteritems():
        relatedFS: FinantialStatements = next(x for x in finantialStatements if x["announcementDate"] == date.strftime("%Y/%m/%d"))
        balanceSheet: AddBalanceSheetRequestType = { "finantialID":  relatedFS["id"]}
        balanceSheet["totalAssets"] = item["Total Assets"]
        balanceSheet["netAssets"] = item["Total Assets"] - item["Total Liab"]
        balanceSheet["capitalStock"] = item["Common Stock"]
        balanceSheet["profitSurplus"] = item["Retained Earnings"]

        result.append(balanceSheet)
    
    return result



if __name__ == "__main__":
    getCompanyWithYahooAPI(9984, 1)