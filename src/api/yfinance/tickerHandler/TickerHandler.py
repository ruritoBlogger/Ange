from typing import Any, Callable, Optional, Union, Dict
from requests.exceptions import ConnectionError
import sys
import os
import time
import pandas as pd
import yfinance as yf
from timeout_decorator import timeout

# NOTE: プロジェクトのrootにパスを通しておく
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from domain import Company
from api.yfinance.tickerHandler.cacheList import CacheList


class TickerHandler:
    """yfinance.tickerを取り扱うwrapper

    アクセス制限された場合の再処理などを盛り込んでいる
    またAPIを出来るだけ叩かない様にキャッシュを保持する
    """


    # yfinanceで提供されるticker
    _ticker: Optional[Any]

    # どの企業のtickerかを取り扱う
    _company: Optional[Company]

    """ APIのアクセス結果のキャッシュ
    {
        cacheList.incomeStatement.value: Any
        cacheList.info.value: Any
        ・
        ・
        ・
    }
    """
    _cache: Dict[str, Any]


    def __init__(self) -> None:
        self._ticker = None
        self._company = None
        self._cache = {}


    def _retryFuncWhenTimeout(self, func: Callable[[], Union[pd.DataFrame, Dict[str, Any]]]) -> Union[pd.DataFrame, Dict[str, Any]]:
        """yfinanceのAPIを叩く, またタイムアウトした際はもう一度処理を挟む

        Args:
            target (Callable[[Any], Any]): 叩きたい関数

        Returns:
            Any: 関数の結果
        """
        try:
            result = func()
            return result
        except ConnectionError:
            print("[handler] yfinanceのAPIサーバーにアクセスが集中しているため一時休止します(10秒)")
            time.sleep(10)
            return self._retryFuncWhenTimeout(func)
        except Exception as err:
            # NOTE: 本当はtimeout_decorator.TimeoutErrorをキャッチしたいが、何故か出来ないので
            print("[handler] yfinance APIからの応答が存在しないため再度実行します")
            print("[handler] error log: {}".format(err))
            time.sleep(10)
            return self._retryFuncWhenTimeout(func)


    def _setTicker(self, requestBody: str) -> None:
        ticker = yf.Ticker(requestBody) 
        self._ticker = ticker

    @timeout(120)
    def _getBalanceSheet(self) -> pd.DataFrame:
        if CacheList.balanceSheet.value in self._cache:
            return self._cache[CacheList.balanceSheet.value]
        else:
            balanceSheet = self._ticker.balance_sheet
            self._cache[CacheList.balanceSheet.value] = balanceSheet
            return balanceSheet
    
    @timeout(120)
    def _getIncomeStatement(self) -> pd.DataFrame:
        if CacheList.incomeStatement.value in self._cache:
            return self._cache[CacheList.incomeStatement.value]
        else:
            incomeStatement = self._ticker.financials
            self._cache[CacheList.incomeStatement.value] = incomeStatement
            return incomeStatement


    @timeout(120)
    def _getCashflow(self) -> pd.DataFrame:
        if CacheList.cashflow.value in self._cache:
            return self._cache[CacheList.cashflow.value]
        else:
            cashflow = self._ticker.cashflow
            self._cache[CacheList.cashflow.value] = cashflow
            return cashflow


    @timeout(120)
    def _getStockPrice(self) -> pd.DataFrame:
        if CacheList.stockPrice.value in self._cache:
            return self._cache[CacheList.stockPrice.value]
        else:
            stockPriceList = self._ticker.history(period="max")
            self._cache[CacheList.stockPrice.value] = stockPriceList
            return stockPriceList


    @timeout(120)
    def _getInfo(self) -> Dict[str, Any]:
        if CacheList.info.value in self._cache:
            return self._cache[CacheList.info.value]
        else:
            info = self._ticker.info
            self._cache[CacheList.info.value] = info
            return info


    @timeout(120)
    def _getSplits(self) -> pd.DataFrame:
        if CacheList.splits.value in self._cache:
            return self._cache[CacheList.splits.value]
        else:
            splits = self._ticker.splits
            self._cache[CacheList.splits.value] = splits
            return splits


    def registTicker(self, company: Company) -> None:
        self._company = company
        requestBody = "{}.T".format(company["identificationCode"])

        self._setTicker(requestBody)


    def getBalanceSheet(self) -> pd.DataFrame:
        return self._retryFuncWhenTimeout(self._getBalanceSheet)


    def getCashflow(self) -> pd.DataFrame:
        return self._retryFuncWhenTimeout(self._getCashflow)


    def getIncomeStatement(self) -> pd.DataFrame:
        return self._retryFuncWhenTimeout(self._getIncomeStatement)


    def getStockPrice(self) -> pd.DataFrame:
        return self._retryFuncWhenTimeout(self._getStockPrice)


    def getInfo(self) -> Dict[str, Any]:
        return self._retryFuncWhenTimeout(self._getInfo)
    

    def getSplits(self) -> pd.DataFrame:
        return self._retryFuncWhenTimeout(self._getSplits)
