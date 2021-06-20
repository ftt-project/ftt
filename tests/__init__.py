from trade.storage import Storage
from trade.storage.models import Base

storage = Storage(application_name="fams", environment="test")
manager = storage.get_manager()
manager.initialize_database()
manager.drop_tables(Base.__subclasses__())
manager.create_tables(storage.get_tables())
