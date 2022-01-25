from typing_extensions import TypedDict
from typing import List, Any, Union, Dict


class companyResponse(TypedDict):
    # FIXME: 特殊なキーの管理をなんとかしたい
    zip: str
    sector: str
    fullTimeEmployees: int
    longBusinessSummary: str
    city: str
    phone: str
    country: str
    companyOfficers: List[Any]
    website: str
    maxAge: int
    address1: str
    industry: str
    address2: str
    ebitdaMargins: float
    profitMargins: float
    grossMargins: float
    operatingCashflow: int
    revenueGrowth: float
    operatingMargins: float
    ebitda: int
    targetLowPrice: Union[int, float]
    recommendationKey: str
    grossProfits: int
    freeCashflow: int
    targetMedianPrice: Union[int, float]
    currentPrice: Union[int, float]
    earningsGrowth: Any
    currentRatio: float
    returnOnAssets: float
    numberOfAnalystOpinions: int
    targetMeanPrice: Union[int, float]
    debtToEquity: float
    returnOnEquity: float
    targetHighPrice: Union[int, float]
    totalCash: int
    totalDebt: int
    totalRevenue: int
    totalCashPerShare: float
    financialCurrency: str
    revenuePerShare: float
    quickRatio: float
    recommendationMean: float
    exchange: str
    shortName: str
    longName: str
    exchangeTimezoneName: str
    exchangeTimezoneShortName: str
    isEsgPopulated: bool
    gmtOffSetMilliseconds: str
    quoteType: str
    # TODO: 銘柄番号はいい感じに管理したい
    symbol: str
    messageBoardId: str
    market: str
    annualHoldingsTurnover: Any
    enterpriseToRevenue: float
    beta3Year: Any
    enterpriseToEbitda: float
    _52WeekChange: float
    morningStarRiskRating: Any
    forwardEps: float
    revenueQuarterlyGrowth: Any
    sharesOutstanding: int
    fundInceptionDate: Any
    annualReportExpenseRatio: Any
    totalAssets: Any
    bookValue: float
    sharesShort: Any
    sharesPercentSharesOut: Any
    fundFamily: Any
    lastFiscalYearEnd: int
    heldPercentInstitutions: float
    netIncomeToCommon: int
    trailingEps: float
    lastDividendValue: int
    SandP52WeekChange: float
    priceToBook: float
    heldPercentInsiders: float
    nextFiscalYearEnd: int
    _yield: Any
    mostRecentQuarter: int
    shortRatio: Any
    sharesShortPreviousMonthDate: Any
    floatShares: int
    beta: float
    enterpriseValue: int
    priceHint: int
    threeYearAverageReturn: Any
    lastSplitDate: int
    lastSplitFactor: str
    legalType: Any
    lastDividendDate: int
    morningStarOverallRating: Any
    earningsQuarterlyGrowth: Any
    priceToSalesTrailing12Months: float
    dateShortInterest: Any
    pegRatio: float
    ytdReturn: Any
    forwardPE: int
    lastCapGain: Any
    shortPercentOfFloat: Any
    sharesShortPriorMonth: Any
    impliedSharesOutstanding: Any
    category: Any
    fiveYearAverageReturn: Any
    previousClose: int
    regularMarketOpen: int
    twoHundredDayAverage: float
    trailingAnnualDividendYield: float
    payoutRatio: float
    volume24Hr: Any
    regularMarketDayHigh: int
    navPrice: Any
    averageDailyVolume10Day: int
    regularMarketPreviousClose: int
    fiftyDayAverage: float
    trailingAnnualDividendRate: int
    open: int
    toCurrency: Any
    averageVolume10days: int
    expireDate: Any
    algorithm: Any
    dividendRate: int
    exDividendDate: int
    circulatingSupply: Any
    startDate: Any
    regularMarketDayLow: int
    currency: str
    trailingPE: float
    regularMarketVolume: int
    lastMarket: Any
    maxSupply: Any
    openInterest: Any
    marketCap: int
    volumeAllCurrencies: Any
    strikePrice: Any
    averageVolume: int
    dayLow: int
    ask: int
    askSize: int
    volume: int
    fiftyTwoWeekHigh: int
    fromCurrency: Any
    fiveYearAvgDividendYield: float
    fiftyTwoWeekLow: int
    bid: int
    tradeable: bool
    dividendYield: float
    bidSize: int
    dayHigh: int
    regularMarketPrice: Union[int, float]
    preMarketPrice: Any
    logo_url: str


def exportAsCompany(response: companyResponse) -> Dict[str, Union[str, int, float]]:
    return {
        "name": response["longName"],
        # TODO: XXXX.T -> XXXXに変換する
        "identificationCode": response["symbol"],
        # TODO: companyResponseの業種情報は日本形式ではないので変換する
        "industry": response["industry"]
    }
