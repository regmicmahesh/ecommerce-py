from datetime import datetime
import json
import re
import typing as ty

import requests
from sqlmodel import Field, SQLModel, UniqueConstraint

from escp.utils.errors import CantFetchException, CantParseException


PATTERN = re.compile(r'skuInfos":\{"0":(\{.*\}),"\d')


class Product(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("product_id"),)
    id: int = Field(primary_key=True)
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

        return cls(product_id=product['itemId'],  # type: ignore
                   name=data_layer['pdt_name'],
                   url=url,
                   original_price=product['price']['originalPrice']['value'],
                   sale_price=product['price']['salePrice']['value'],
                   seller_name=data_layer['seller_name'],
                   stock=product['stock'],
                   image=data_layer['pdt_photo'],
                   date=str(datetime.today().strftime('%Y-%m-%d'))
                   )


class ProductPrice(SQLModel, table=True):
    id: ty.Optional[int] = Field(default=None, primary_key=True)
    current_price: int
    date: str
    product_id: int = Field(foreign_key="product.id")

    @classmethod
    def from_initial_product(cls, product: Product):
        return cls(current_price=product.sale_price,
                   date=product.date,
                   product_id=product.id)


def parseResponseFromURL(url: str) -> ty.Tuple[Product, ProductPrice]:

    res = requests.get(url)

    if res.status_code == 200:
        data = res.text
    else:
        raise CantFetchException(f'Cant fetch {url}')

    matches = PATTERN.findall(data)

    if len(matches) != 1:
        raise CantParseException(f'Cant parse {url}')

    product = json.loads(matches[0])

    product = Product.from_json(url, product)
    product_price = ProductPrice.from_initial_product(product)

    return product, product_price
