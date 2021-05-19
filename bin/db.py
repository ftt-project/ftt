import fire

from trade.models.setup import create_tables, create_database, drop_tables
from trade.models import Base


class DB:
    @staticmethod
    def create_database():
        create_database()

    @staticmethod
    def create_tables():
        models = Base.__subclasses__()
        create_tables(models)

    @staticmethod
    def reset_database():
        models = Base.__subclasses__()
        drop_tables(models)
        create_tables(models)


if __name__ == "__main__":
    fire.Fire(DB)
