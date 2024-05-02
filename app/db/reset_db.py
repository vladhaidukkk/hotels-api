from app.db.core import Base, sync_engine

# Import all models to register them in the metadata object
from app.hotels.model import HotelModel  # noqa


def reset_db():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


if __name__ == "__main__":
    reset_db()
