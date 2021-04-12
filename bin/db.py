import fire

from peewee import Database
from trade.db.setup import create_tables
from trade.db.base import Base


class DB:
    def create(self):
        models = Base.__subclasses__()
        create_tables(models)


if __name__ == "__main__":
    fire.Fire(DB)
