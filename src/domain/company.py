from typing import TypeVar
from typing_extensions import TypedDict

CompanyType = TypeVar('CompanyType', bound='Company')


class Company(TypedDict):
    # TODO: APIから得た情報をCompany型に変換する関数を用意する
    id: int
    industryID: int
    name: str
    identificationCode: int
    createdAt: str
    updatedAt: str
