from sqlalchemy import create_engine, text

from app.config import DB_URL

engine = create_engine(url=DB_URL, echo=True)

with engine.connect() as conn:
    res = conn.execute(text("SELECT VERSION()"))
    version = res.first()[0]
    print(version)
