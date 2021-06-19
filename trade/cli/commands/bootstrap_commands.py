from nubia import command, argument

from trade.storage import Storage


@command
@argument("environment", description="Environment name", positional=True)
def bootstrap(environment: str):
    """
    Initialize application and all its components
    """
    storage = Storage(application_name="fams", environment=environment)
    manager = storage.get_manager()
    manager.initialize_database()
    manager.create_tables(storage.get_tables())
    # manager.check_and_run_migration()
    # manager.seed_data()
