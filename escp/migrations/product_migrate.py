from sqlmodel import Field, Session, SQLModel, create_engine

from escp.models.Product import Product, ProductPrice


engine = create_engine('sqlite:///escp.db', echo=True)

SQLModel.metadata.create_all(engine)
