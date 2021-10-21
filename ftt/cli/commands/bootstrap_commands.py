from nubia import argument, command

from ftt.storage import Storage


@command
@argument("environment", description="Environment name", positional=True)
def bootstrap(environment: str):
    """
    Initialize application and all its components
    """
    # TODO: take from context
    Storage.initialize_database(application_name="ftt", environment=environment)
    manager = Storage.storage_manager()
    manager.create_tables(Storage.get_models())
    # manager.check_and_run_migration()
    # manager.seed_data()
