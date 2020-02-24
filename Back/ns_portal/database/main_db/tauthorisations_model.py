from ns_portal.database.meta import (
    Main_Db_Base
)
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    ForeignKey
)


class TAutorisations(Main_Db_Base):
    __tablename__ = 'TAutorisations'

    TAut_PK_ID = Column(
        Integer,
        primary_key=True
    )
    TAut_FK_TInsID = Column(
        Integer,
        nullable=True
    )
    TAut_FK_TUseID = Column(
        Integer,
        ForeignKey('TUsers.TUse_PK_ID'),
        nullable=True
    )
    TAut_FK_TRolID = Column(
        Integer,
        ForeignKey('TRoles.TRol_PK_ID'),
        nullable=True
    )
    TUse_Observer = Column(
        Boolean,
        nullable=False,
        server_default='0'
    )
