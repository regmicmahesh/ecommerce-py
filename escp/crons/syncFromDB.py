from escp.models.Product import Product
from sqlmodel import select, Session, create_engine

def syncFromDB():
    engine = create_engine('sqlite:///escp.db')
    with Session(engine) as sess:
        product = select(Product)
        products = sess.exec(product)
        print(products)

if __name__ == '__main__':
    syncFromDB()
    

