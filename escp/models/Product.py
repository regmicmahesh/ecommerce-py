from datetime import datetime
import requests
import json
import re
import typing as ty

from sqlmodel import Field, SQLModel


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
    date: str

    @classmethod
    def from_json(cls, product: dict):
        data_layer = product['dataLayer']

        return cls(product_id=product['itemId'],
                   name=data_layer['pdt_name'],
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
        raise Exception(f"Can't get data from {url}")

    matches = PATTERN.findall(data)

    if len(matches) != 1:
        raise Exception(f"Can't parse data from {url}")

    product = json.loads(matches[0])

    return Product.from_json(product)


# url = "https://www.daraz.com.np/products/acer-aspire-5-a515-46-r14k-amd-ryzen-3-processor-8gb-ddr4-ram-256gb-ssd-amd-vega-6-graphic-15-fhd-1920x1080-screen-backlit-keyboard-pure-silver-metalicfingerprint-reader-win10-genuine-i104802647-s1026280482.html"
