from escp.models.Product import Product, ProductPrice, parseResponseFromURL
from escp.utils.db import engine
from sqlmodel import select, Session, create_engine


def syncFromDB():
    with Session(engine) as sess:
        product = select(Product, ProductPrice).where(
            Product.id == ProductPrice.product_id)
        products = sess.exec(product)

        for dbp, dbpp in products:
            product, product_price = parseResponseFromURL(dbp.url)
            product_price.product_id = dbp.id
            with Session(engine) as sess:
                sess.add(product_price)
                sess.commit()


if __name__ == '__main__':
    syncFromDB()
