from enum import Enum

class CacheList(Enum):
    # yfinance.tickerから取得出来る情報の種類を列挙したもの

    balanceSheet = "balanceSheet"
    quarterlyBalanceSheet = "quarterlyBalanceSheet"
    cashflow = "cashflow"
    quarterlyCashflow = "quarterlyCashflow"
    incomeStatement = "incomeStatement"
    quarterlyIncomeStatement = "quarterlyIncomeStatement"
    stockPrice = "stockPrice"
    info = "info"
    splits = "splits"