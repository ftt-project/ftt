import fire

from trade.db.setup import create_tables, create_database
from trade.db.base import Base


class DB:
    def create_database(self):
        create_database()

    def create_tables(self):
        models = Base.__subclasses__()
        create_tables(models)


if __name__ == "__main__":
    fire.Fire(DB)
