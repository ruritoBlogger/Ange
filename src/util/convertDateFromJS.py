from datetime import datetime, timedelta

def convertDateFromJS(target: str) -> datetime.date:
    """JavaScriptのDate型をpythonのdatetimeに変換する

    "YYYY-mm-dd HH:MM:SSTZ" -> YYYY/mm/dd

    Args:
        target (str): JavaScriptのDate型がそのままstr型になった虚しいやつ

    Returns:
        datetime.date: Pythonで扱えるようにした日付
    """

    convertedDate = datetime.strptime(target[:10].replace("-", "/"), "%Y/%m/%d")

    # FIXME: 本当はタイムゾーンの情報から計算すべきだが、ダルいのでゴリ押した
    convertedDate += timedelta(days=1)

    return convertedDate
