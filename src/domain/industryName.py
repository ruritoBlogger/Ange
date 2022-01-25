from enum import Enum
from typing import Type, TypeVar
from typing_extensions import TypedDict


IndustryNameType = TypeVar('IndustryNameType', bound='IndustryName')


class IndustryName(Enum):
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

    @classmethod
    def convertFromStr(cls: Type[IndustryNameType], target: str) -> IndustryNameType:
        for industry in IndustryName:
            if industry.value == target:
                return industry

        raise ValueError('{}は有効な業種名ではありません'.format(target))
