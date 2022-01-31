from typing_extensions import TypedDict


class FinantialStatements(TypedDict):
    companyID: int
    # TODO: JSの日付(string型) -> pythonの日付に変換する
    announcementDate: str
    isFiscal: bool
    createdAt: str
    updatedAt: str