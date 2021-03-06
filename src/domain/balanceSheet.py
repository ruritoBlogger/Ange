from typing_extensions import TypedDict


class BalanceSheet(TypedDict):
    id: int
    finantialID: int
    totalAssets: float
    netAssets: float
    capitalStock: float
    profitSurplus: float
    printedNum: int
    createdAt: str
    updatedAt: str
