from ns_portal.database.meta import (
    Main_Db_Base
)
from sqlalchemy import (
    Column,
    Integer,
    String
)


class TApplications(Main_Db_Base):
    __tablename__ = 'TApplications'

    TApp_PK_ID = Column(
        Integer,
        primary_key=True
    )
    TApp_Name = Column(
        String(50),
        nullable=True
    )
    TApp_Description = Column(
        String(255),
        nullable=True
    )
