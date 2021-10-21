from ftt.storage import Storage
from ftt.storage.models.base import Base

Storage.initialize_database(application_name="ftt", environment="test")
manager = Storage.storage_manager()
manager.drop_tables(Base.__subclasses__())
manager.create_tables(Storage.get_models())
