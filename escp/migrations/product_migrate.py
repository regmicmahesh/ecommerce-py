from sqlmodel import Field, Session, SQLModel, create_engine

from escp.models.Product import Product


engine = create_engine('sqlite:///escp.db', echo=True)

SQLModel.metadata.create_all(engine)


