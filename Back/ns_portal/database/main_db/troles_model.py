from ns_portal.database.meta import (
    Main_Db_Base
)
from sqlalchemy import (
    Column,
    Integer,
    String
)


class TRoles(Main_Db_Base):
    __tablename__ = 'TRoles'

    TRol_PK_ID = Column(
        Integer,
        primary_key=True
    )
    TRol_Label = Column(
        String(250),
        nullable=False
    )
    TRol_Definition = Column(
        String(250),
        nullable=True
    )
