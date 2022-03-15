from typing_extensions import TypedDict

class Index(TypedDict):
    id: int
    finantialID: int
    capitalAdequacyRatio: float
    roe: float
    roa: float
    per: float
    pbr: float
    eps: float
    createdAt: str
    updatedAt: str