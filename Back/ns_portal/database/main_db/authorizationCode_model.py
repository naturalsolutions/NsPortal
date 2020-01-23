from ns_portal.database.meta import (
    Main_Db_Base
)
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Sequence,
    func
)
from sqlalchemy.dialects.mssql import (
    UNIQUEIDENTIFIER
)


class AuthorizationCode(Main_Db_Base):
    __tablename__ = 'AuthorizationCode'

    ID = Column(
        UNIQUEIDENTIFIER,
        primary_key=True
    )
    creationDate = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
