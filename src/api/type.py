from typing_extensions import TypedDict


class addCompanyRequestType(TypedDict):
    name: str
    industryID: int
    identificationCode: int


class addIndustryRequestType(TypedDict):
    name: str