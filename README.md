# ange

株式売買をする上で, 過去のデータや新しく追加されたデータをバックエンドに流し込むなどの機能置き場.
REST API で構成しています.

## ディレクトリ構造

```
.
├── bin
│    ├─ bootstrap.sh # flaskを用いてAPIサーバーを起動するshell
│    └─ bootstrap.prod.sh # ↑のproduction用shell
│
├── src
│    ├─ api # 企業情報とかを管理するAPIを叩くコード置き場
│    │    ├─ *.py # toko API叩き場
│    │    ├─ type.py # toko APIに関する型置き場
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
│    ├─ validator # 型チェック用関数置き場
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
# 開発用サーバー起動
$ pipenv run dev

# 本番用サーバー起動
$ pipenv run prod

# APIと連携して業種情報を生成する
$ pipenv run industry

# APIと連携して企業情報を生成する
$ pipenv run company

# APIと連携して財務情報を生成する
$ pipenv run sheets
```
