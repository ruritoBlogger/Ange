from typing import Optional
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import FinantialStatements, BalanceSheet, Cashflow, IncomeStatement, StockPrice, Index
from validator.isKeyExist import isKeyExist

def validateFS(target: FinantialStatements) -> Optional[FinantialStatements]:
    if isKeyExist(target, FinantialStatements.__annotations__.keys()):
        return target
    else:
        print("[FS]: validate errored: {}".format(target))
        raise KeyError
        return None


def validateBS(target: BalanceSheet) -> Optional[BalanceSheet]:
    if isKeyExist(target, BalanceSheet.__annotations__.keys()):
        return target
    else:
        print("[BS]: validate errored: {}".format(target))
        raise KeyError
        return None


def validateCF(target: Cashflow) -> Optional[Cashflow]:
    if isKeyExist(target, Cashflow.__annotations__.keys()):
        return target
    else:
        print("[CS]: validate errored: {}".format(target))
        raise KeyError
        return None


def validateIS(target: IncomeStatement) -> Optional[IncomeStatement]:
    if isKeyExist(target, IncomeStatement.__annotations__.keys()):
        return target
    else:
        print("[IS]: validate errored: {}".format(target))
        raise KeyError
        return None


def validateStockPrice(target: StockPrice) -> Optional[StockPrice]:
    if isKeyExist(target, StockPrice.__annotations__.keys()):
        return target
    else:
        print("[StockPrice]: validate errored: {}".format(target))
        raise KeyError
        return None


def validateIndex(target: Index) -> Optional[Index]:
    if isKeyExist(target, Index.__annotations__.keys()):
        return target
    else:
        print("[Index]: validate errored: {}".format(target))
        raise KeyError
        return None