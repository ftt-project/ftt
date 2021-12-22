def reload_record(record):
    """
    Reloads the record from the database.
    """
    return record.__class__.get_by_id(record.id)
