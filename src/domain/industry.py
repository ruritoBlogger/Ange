from enum import Enum
from typing import TypeVar
from typing_extensions import TypedDict

IndustryType = TypeVar('IndustryType', bound='Industry')


class Industry(TypedDict):
    # TODO: APIから得た情報をIndustry型に変換する関数を用意する
    id: int
    name: str
    createdAt: str
    updatedAt: str
