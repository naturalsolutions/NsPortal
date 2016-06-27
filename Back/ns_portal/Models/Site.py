from sqlalchemy import (
   Column,
   DateTime,
   Index,
   Integer,
   Sequence,
   String,
   func,
   Boolean,
   VARBINARY
 )

from sqlalchemy.ext.hybrid import hybrid_property
from . import Base, dbConfig

db_dialect = dbConfig['dialect']

class Site(Base):
    __tablename__ = 'TSite'
    id = Column('TSit_PK_ID', Integer, primary_key=True)
    Name = Column( 'TSit_Name', String(50), nullable=False)
    Locality = Column( 'TSit_Locality', String(50), nullable=False)
    Country = Column( 'TSit_Country', String(50), nullable=False)
    ImagePathLogin = Column( 'TSit_ImagePathLogin', String(250))
    ImagePathMainMenu = Column( 'TSit_ImagePathMainMenu', String(250))
    ImagePathMainLogo = Column( 'TSit_ImagePathMainLogo', String(250))
    IpServeurHamachi = Column( 'TSit_IpServeurHamachi', String(20))

    Director = Column( 'TSit_Director', Integer)
    NetworkAdmin = Column( 'TSit_NetworkAdmin', Integer)
    BreedingChief = Column( 'TSit_BreedingChief', Integer)
    VetChief = Column( 'TSit_VetChief', Integer)
    IncubChief = Column( 'TSit_IncubChief', Integer)
    Project = Column( 'TSit_Project', String(250))
    LongName = Column( 'TSit_LongName', String(255))
    ImageBackPortal = Column( 'TSit_ImageBackPortal', VARBINARY)
    ImageLogoPortal = Column( 'Tsit_ImageLogoPortal', VARBINARY)
    BackgroundHomePage = Column( 'TSit_BackgroundHomePage', VARBINARY)
    UILabel = Column( 'TSit_UILabel', String(255))
