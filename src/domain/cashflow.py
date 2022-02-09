from typing_extensions import TypedDict


class Cashflow(TypedDict):
    id: int
    finantialID: int
    salesCF: float
    investmentCF: float
    finantialCF: float
    createdAt: str
    updatedAt: str
