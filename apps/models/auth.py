from apps.db.base import Base
import sqlalchemy as sa, datetime
from sqlalchemy.orm import relationship


class User(Base):
    name = sa.Column(sa.String(50))
    username = sa.Column(sa.String(100),unique=True)
    mobile = sa.Column(sa.String(100))
    password = sa.Column(sa.String(100))
    is_active = sa.Column(sa.Boolean,default=True)
    
    # relationship
    sessions = relationship("Token",back_populates="user")
    
    
class Session(Base):
    access_token = sa.Column(sa.String(255),nullable=True,default='')
    refresh_token = sa.Column(sa.String(255),nullable=True,default='')
    user_id = sa.Column(sa.Integer,sa.ForeignKey('users.id'))
    city = sa.Column(sa.String(255))
    country = sa.Column(sa.String(255))
    region = sa.Column(sa.String(255))
    ip = sa.Column(sa.String(255))
    user_agent = sa.Column(sa.String(255))
    timezone = sa.Column(sa.String(255))
    loc = sa.Column(sa.String(255))
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    
    # relationship 
    user = relationship("User",back_populates="sessions")

