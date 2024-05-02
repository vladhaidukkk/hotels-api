from app.db.core import metadata, sync_engine

# Import all tables to register them in the metadata object
from app.hotels.table import hotels_table  # noqa


def reset_db():
    metadata.drop_all(sync_engine)
    metadata.create_all(sync_engine)


if __name__ == "__main__":
    reset_db()
