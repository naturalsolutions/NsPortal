from ns_portal.database.meta import (
    Main_Db_Base
)
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    ForeignKey
)


class TInstance(Main_Db_Base):
    __tablename__ = 'TInstance'

    TIns_PK_ID = Column(
        Integer,
        primary_key=True
    )
    TIns_Label = Column(
        String(250),
        nullable=False
    )
    TIns_ApplicationPath = Column(
        String(500),
        nullable=True
    )
    TIns_ImagePath = Column(
        String(500),
        nullable=True
    )
    TIns_IconePath = Column(
        String(500),
        nullable=True
    )
    TIns_Theme = Column(
        String(500),
        nullable=True
    )
    TIns_Database = Column(
        String(500),
        nullable=True
    )
    TIns_Order = Column(
        Integer,
        nullable=False
    )
    TIns_FK_TAppID = Column(
        Integer,
        ForeignKey('TApplications.TApp_PK_ID'),
        nullable=False
    )
    TIns_FK_TSitID = Column(
        Integer,
        ForeignKey('TSite.TSit_PK_ID'),
        nullable=False
    )
    TIns_PK_ID_OLD = Column(
        Integer,
        nullable=True
    )
    TIns_ReadOnly = Column(
        Boolean,
        nullable=False,
        server_default='0'
    )
