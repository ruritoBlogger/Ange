from ast import Add
import yfinance as yf
from typing import Tuple, List
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from api import AddFinantialStatementsRequstType

def getCompanyWithYF(identificationCode: int, companyID: int) -> List[Tuple[AddFinantialStatementsRequstType]]:
    requestBody = "{}.T".format(identificationCode)
    response = yf.Ticker(requestBody)

    df: pd.DataFrame = response.financials
    for date, item in df.iteritems():
        finantialStatements: AddFinantialStatementsRequstType = { "companyID": companyID, "announcementDate": date.strftime("%Y/%m/%d"), "isFiscal": True }
        print(item)
        break

if __name__ == "__main__":
    getCompanyWithYF(9984, 1)