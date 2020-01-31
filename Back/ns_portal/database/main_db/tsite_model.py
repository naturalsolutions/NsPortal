from ns_portal.database.meta import (
    Main_Db_Base
)
from sqlalchemy import (
    Column,
    Integer,
    String,
    VARBINARY
)


class TSite(Main_Db_Base):
    __tablename__ = 'TSite'
    TSit_PK_ID = Column(
        Integer,
        primary_key=True
        )
    TSit_Name = Column(
        String(50),
        nullable=False
        )
    TSit_Locality = Column(
        String(50),
        nullable=False
        )
    TSit_Country = Column(
        String(50),
        nullable=False
        )
    TSit_ImagePathLogin = Column(
        String(250),
        nullable=True
        )
    TSit_ImagePathMainMenu = Column(
        String(250),
        nullable=True
        )
    TSit_ImagePathMainLogo = Column(
        String(250),
        nullable=True
        )
    TSit_IpServeurHamachi = Column(
        String(20),
        nullable=True
        )
    TSit_Director = Column(
        Integer,
        nullable=True
        )
    TSit_NetworkAdmin = Column(
        Integer,
        nullable=True
        )
    TSit_BreedingChief = Column(
        Integer,
        nullable=True
        )
    TSit_VetChief = Column(
        Integer,
        nullable=True
        )
    TSit_IncubChief = Column(
        Integer,
        nullable=True
        )
    TSit_Project = Column(
        String(250),
        nullable=True
        )
    TSit_LongName = Column(
        String(255),
        nullable=True
        )
    TSit_ImageBackPortal = Column(
        VARBINARY,
        nullable=True
        )
    Tsit_ImageLogoPortal = Column(
        VARBINARY,
        nullable=True
        )
    TSit_BackgroundHomePage = Column(
        VARBINARY,
        nullable=True
        )
    TSit_UILabel = Column(
        String(255),
        nullable=True
        )
