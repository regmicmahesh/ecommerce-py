from sqlmodel import create_engine


engine = create_engine('sqlite:///escp.db', echo=True)
