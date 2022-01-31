from typing_extensions import TypedDict


class BalanceSheet(TypedDict):
    id: int
    finantialID: int
    totalAssets: float
    netAssets: float
    capitalStock: float
    profitSurplus: float
    cashEquivalent: float
    netCash: float
    depreciation: float
    capitalInvestment: float
    libilities: float
    createdAt: str
    updatedAt: str
