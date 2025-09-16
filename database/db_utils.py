from contextlib import contextmanager

import sqlalchemy
from database import models

Session = sqlalchemy.orm.sessionmaker(bind=models.engine)

@contextmanager
def getSession():
    session = Session()
    try:
        yield session
    finally:
        session.close()

def buildTables():
    models.Base.metadata.create_all(models.engine)
    print("Tables Successfully Built")
    return True
    
def dropTables():
    models.Base.metadata.drop_all(models.engine)
    print("Tables Successfully Dropped")
    return True