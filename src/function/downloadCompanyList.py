import requests
import pandas as pd
from typing import List, Dict, Union
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import Industry
from api import getIndustryList

def downloadCompanyList(industryList: List[Industry]) -> List[Dict[str, Union[int, str]]]:
    """JSXのサイトから企業情報が掲載されたxlsファイルを取得する

    その中で東証一部に上場している企業 & ETFなどを取り除いたものを取得する
    """

    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    result = requests.get(url)
    df = pd.read_excel(result.content)

    # 東証一部のみ + [コード(銘柄コード), 銘柄名, 33業種区分]にframeを整形
    df = df[df['市場・商品区分'] == "市場第一部（内国株）"]
    df = df.drop(['日付', '市場・商品区分', '33業種コード', '17業種コード', '17業種区分', '規模コード', '規模区分'], axis=1)

    # TODO: addCompanyする際の型を定義しておく
    companyList: List[Dict[str, Union[int, str]]] = []
    for _, row in df.iterrows():
        industry = next((x for x in industryList if x["name"] == row["33業種区分"]), None)
        companyList.append({"name": row["銘柄名"], "identificationCode": row["コード"], "industryID": industry["id"]})

    return companyList

if __name__ == "__main__":
    downloadCompanyList(getIndustryList())
