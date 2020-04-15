from ns_portal.database.meta import (
    Log_Db_Base
)
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Sequence,
    func
)


class TLOG_MESSAGES(Log_Db_Base):
    __tablename__ = 'TLOG_MESSAGES'

    ID = Column(
        Integer,
        Sequence('Equipment__id_seq'),
        primary_key=True
    )
    JCRE = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    LOG_LEVEL = Column(
        Integer,
        nullable=True
    )
    ORIGIN = Column(
        String(8000),
        nullable=True
    )
    SCOPE = Column(
        String(400),
        nullable=True
    )
    LOGUSER = Column(
        String(8000),
        nullable=True
    )
    DOMAINE = Column(
        String(8000),
        nullable=True
    )
    MESSAGE_NUMBER = Column(
        String(8000),
        nullable=True
    )
    LOG_MESSAGE = Column(
        String(8000),
        nullable=True
    )
    OTHERSINFOS = Column(
        String('max'),
        nullable=True
    )
