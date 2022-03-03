from typing import TypeVar
from typing_extensions import TypedDict

StockPriceType = TypeVar('StockPriceType', bound='StockPrice')


class StockPrice(TypedDict):
    id: int
    companyID: int
    openingPrice: float
    closingPrice: float
    highPrice: float
    lowPrice: float
    date: str
    createdAt: str
    updatedAt: str
