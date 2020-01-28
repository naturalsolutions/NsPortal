from ns_portal.database.meta import (
    Main_Db_Base
)
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    func
)


class TUsers(Main_Db_Base):
    __tablename__ = 'TUsers'

    TUse_PK_ID = Column(
        Integer,
        primary_key=True
    )
    TUse_LastName = Column(
        String(100),
        nullable=True
    )
    TUse_FirstName = Column(
        String(100),
        nullable=True
    )
    TUse_CreationDate = Column(
        DateTime,
        nullable=True
    )
    TUse_Login = Column(
        String(255),
        nullable=False
    )
    TUse_Password = Column(
        String(50),
        nullable=True
    )
    TUse_Language = Column(
        String(5),
        nullable=True
    )
    TUse_ModificationDate = Column(
        DateTime,
        nullable=True,
        server_default=func.now()
    )
    TUse_HasAccess = Column(
        Boolean,
        nullable=False
    )
    TUse_Photo = Column(
        String(255),
        nullable=False
    )
    TUse_PK_ID_OLD = Column(
        Integer,
        nullable=False,
        server_default=func.now()
    )
