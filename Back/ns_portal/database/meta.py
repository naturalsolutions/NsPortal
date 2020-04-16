from sqlalchemy import (
    MetaData
)
from sqlalchemy.ext.declarative import (
    declarative_base
)


class Base(object):
    __table_args__ = {'implicit_returning': False}


# declarative_base will construct a base class for declarative
Base = declarative_base(cls=Base)

# create top level class for each database
# these class will be attached with each engine
# then for a given model
# sqlalchemy will automatically chose the 'good' engine with top level class


class Main_Db_Base(Base):
    __abstract__ = True
    metadata = MetaData()


class Log_Db_Base(Base):
    __abstract__ = True
    metadata = MetaData()
