import database as _database

def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)