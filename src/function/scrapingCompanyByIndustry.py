from requests_html import HTMLSession
from typing import List, Dict
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from domain import IndustryCodeForMyKabu, companyResponse


def scrapingCompanyByIndustry(industryCode: IndustryCodeForMyKabu) -> companyResponse:
	url = "https://my.kabumap.com/market/sector/{}?key=nameSector".format(industryCode.value)

	# requests_htmlを用いたスクレイピング
	session = HTMLSession()
	r = session.get(url)
	r.html.render()

	# 取得した要素を分解
	table = r.html.find("#resultTableTop", first=True)
	# NOTE: 先頭の要素は必ず空配列になったので対応
	trList = table.find("tr")[1:]

	"""
	NOTE
	perなどはここでも取得できるが,
	yahoo finance APIを使ったほうが安全なのでここではやらない.
	my株はスクレイピング問題無さそう(個人利用に限る)だが,
	絶対問題が無いとは言い切れないので.
	"""

	companyList: List[Dict[str, str]] = []
	for tr in trList:
		tdList = tr.find("td")
		codeTd = tdList[0] # <td ~~~><span ~~~>code</span></td>
		nameTd = tdList[1] # <td ~~~><span ~~~>name</span></td>

		companyList.append({"name": nameTd.find("span", first=True).text, "identificationCode": (int)(codeTd.find("span", first=True).text)})

	print(companyList)
	# TODO: 企業を登録するAPIを生やして叩く


if __name__ == "__main__":
    scrapingCompanyByIndustry(IndustryCodeForMyKabu(321))
