from datetime import datetime
import json
import re
import typing as ty

import requests
from sqlmodel import Field, SQLModel

from escp.utils.errors import CantFetchException, CantParseException


PATTERN = re.compile(r'skuInfos":\{"0":(\{.*\}),"\d')


class Product(SQLModel, table=True):
    id: ty.Optional[int] = Field(default=None, primary_key=True)
    product_id: str
    name: str
    original_price: int
    sale_price: int
    stock: int
    image: str
    seller_name: str
    url: str
    date: str

    @classmethod
    def from_json(cls, url: str, product: dict):
        data_layer = product['dataLayer']

        return cls(product_id=product['itemId'],
                   name=data_layer['pdt_name'],
                   url=url,
                   original_price=product['price']['originalPrice']['value'],
                   sale_price=product['price']['salePrice']['value'],
                   seller_name=data_layer['seller_name'],
                   stock=product['stock'],
                   image=data_layer['pdt_photo'],
                   date=str(datetime.now())
                   )


def parseResponseFromURL(url: str) -> Product:

    res = requests.get(url)

    if res.status_code == 200:
        data = res.text
    else:
        raise CantFetchException(f'Cant fetch {url}')

    matches = PATTERN.findall(data)

    if len(matches) != 1:
        raise CantParseException(f'Cant parse {url}')

    product = json.loads(matches[0])

    return Product.from_json(url, product)
