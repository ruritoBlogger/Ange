from enum import Enum


class Industry(Enum):
    fish = "水産・農林業"
    mining = "鉱業"
    construction = "建設業"
    food = "食料品"
    fiber = "繊維製品"
    paper = "パルプ・紙"
    chemistry = "化学"
    medical = "医薬品"
    oil = "石油・石炭製品"
    rubber = "ゴム製品"
    glass = "ガラス・土石製品"
    iron = "鉄鋼"
    metal = "非鉄金属"
    metalProducts = "金属製品"
    machine = "機械"
    electronicEquipment = "電気機器"
    transport = "輸送用機器"
    precise = "精密機器"
    other = "その他製品"
    electronic = "電気・ガス業"
    landTransportation = "陸運業"
    shipping = "海運業"
    air = "空運業"
    warehouse = "倉庫・運輸関連業"
    infromation = "情報・通信"
    wholesale = "卸売業"
    retail = "小売業"
    bank = "銀行業"
    securities = "証券業"
    insurance = "保険業"
    otherFinancial = "その他金融業"
    realEstate = "不動産業"
    service = "サービス業"


# NOTE: 業種コードはスクレイピング先に依存してます
class IndustryCode(Enum):
    fish = 321
    mining = 322
    construction = 323
    food = 324
    fiber = 325
    paper = 326
    chemistry = 327
    medical = 328
    oil = 329
    rubber = 330
    glass = 331
    iron = 332
    metal = 333
    metalProducts = 334
    machine = 335
    electronicEquipment = 336
    transport = 337
    precise = 338
    other = 339
    electronic = 340
    landTransportation = 341
    shipping = 342
    air = 343
    warehouse = 344
    infromation = 345
    wholesale = 346
    retail = 347
    bank = 348
    securities = 349
    insurance = 350
    otherFinancial = 351
    realEstate = 352
    service = 353
