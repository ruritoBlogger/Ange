from typing_extensions import TypedDict
from typing import List, Any, Union, Dict


class FinantialStatements(TypedDict):
    companyID: int
    # TODO: JSの日付(string型) -> pythonの日付に変換する
    announcementDate: str
    isFiscal: bool