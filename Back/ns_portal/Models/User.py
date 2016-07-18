from sqlalchemy import (
   Column,
   DateTime,
   Index,
   Integer,
   Sequence,
   String,
   func,
   Boolean
 )

from sqlalchemy.ext.hybrid import hybrid_property
from . import Base, dbConfig

db_dialect = dbConfig['dialect']

class User(Base):
    __tablename__ = 'TUsers'
    id = Column('TUse_PK_ID', Integer, primary_key=True)
    Lastname = Column( 'TUse_LastName', String(50), nullable=False)
    Firstname = Column( 'TUse_FirstName', String(50), nullable=False)
    CreationDate = Column( 'TUse_CreationDate', DateTime, nullable=False,server_default=func.now())
    Login = Column( 'TUse_Login', String(255), nullable=False)
    Password = Column( 'TUse_Password', String(50), nullable=False)
    Language = Column( 'TUse_Language', String(5))
    ModificationDate = Column( 'TUse_ModificationDate', DateTime, nullable=False,server_default=func.now())
    HasAccess = Column( 'TUse_HasAccess', Boolean)
    Photos = Column( 'TUse_Photo', String(255))
    IsObserver = Column( 'TUse_Observer', Boolean)

    @hybrid_property
    def fullname(self):
        """ Return the fullname of a user.
        """
        return self.Lastname + ' ' + self.Firstname
    
    def check_password(self, given_pwd):
        """Check the password of a user.
        
        Parameters
        ----------
        given_pwd : string
            The password to check, assumed to be an SHA1 hash of the real one.
            
        Returns
        -------
        boolean
            Either the password matches or not
        """
        return self.Password == given_pwd.lower()
