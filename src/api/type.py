from typing_extensions import TypedDict


class AddCompanyRequestType(TypedDict):
    name: str
    industryID: int
    identificationCode: int


class AddIndustryRequestType(TypedDict):
    name: str


class AddFinantialStatementsRequstType(TypedDict):
    companyID: int
    announcementDate: str
    isFiscal: bool


class AddIncomeStatementRequestType(TypedDict):
    finantialID: int
    totalSales: float
    operatingIncome: float
    ordinaryIncome: float
    netIncome: float


class AddIndexRequestType(TypedDict):
    finantialID: int
    capitalAdequacyRatio: float
    roe: float
    roa: float
    per: float
    pbr: float
    eps: float
    pcfr: float
    yieldGap: float


class AddBalanceSheetRequestType(TypedDict):
    finantialID: int
    totalAssets: float
    netAssets: float
    capitalStock: float
    profitSurplus: float