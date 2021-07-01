from nubia import command, argument

from trade.storage import Storage


@command
@argument("environment", description="Environment name", positional=True)
def bootstrap(environment: str):
    """
    Initialize application and all its components
    """
    Storage.initialize_database(application_name="fams", environment=environment)
    manager = Storage.storage_manager()
    manager.create_tables(Storage.get_models())
    # manager.check_and_run_migration()
    # manager.seed_data()
