from enum import Enum
from typing import Type, TypeVar
from .industryName import IndustryName


IndustryCodeForMyKabuType = TypeVar('IndustryCodeForMyKabuType', bound='IndustryCodeForMyKabu')


class IndustryCodeForMyKabu(Enum):
    # スクレイピング先にて使用されている独自の業種コード
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

    @classmethod
    def convertFromIndustryName(cls: Type[IndustryCodeForMyKabuType], target: IndustryName) -> IndustryCodeForMyKabuType:
        for industryCode in IndustryCodeForMyKabu:
            if industryCode.name == target.name:
                return industryCode
        
        raise ValueError('{}は有効な業種名ではありません'.format(target.value))