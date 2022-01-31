from typing_extensions import TypedDict


class IncomeStatement(TypedDict):
    id: int
    finantialID: int
    totalSales: float
    operatingIncome: float
    ordinaryIncome: float
    netIncome: float
    createdAt: str
    updatedAt: str