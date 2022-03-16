# ange

株式売買をする上で, 過去のデータや新しく追加されたデータをバックエンドに流し込むなどの機能置き場.
REST API で構成しています.

## ディレクトリ構造

```
.
├── bin
│    └─ bootstrap.sh # flaskを用いてAPIサーバーを起動するshell
│
├── src
│    ├─ api # 企業情報とかを管理するAPIを叩くコード置き場
│    │    ├─ *.py # toko API叩き場
│    │    └─ yfinance # yfinance API叩き場
│    │
│    ├─ domain # 型置き場
│    │    ├─ company.py # APIから取得した企業情報の型
│    │    ├─ companyResponse.py # yfinanceを用いて取得した企業情報の型
│    │    └─ industry.py # APIから取得した業績情報の型
│    │
│    ├─ function # 機能置き場
│    │    ├─ downloadCompanyList.py # xlsファイルから企業情報を抽出する
│    │    ├─ generateCompanyData.py # 企業情報を生成する
│    │    ├─ generateFinantialStatements.py # 企業に関係する情報を生成する(指標など)
│    │    └─ generateIndustryData.py # 業績情報を生成する
│    │
│    └─ util # 便利関数置き場
│
├─ index.py # flaskのroot(未設定)
└─Pipfile # pipenvの設定
```

## 導入

```
$ pipenv install
```

## 開発

```
# APIと連携して業種情報を生成する
$ pipenv run industry

# APIと連携して企業情報を生成する
$ pipenv run company
```
