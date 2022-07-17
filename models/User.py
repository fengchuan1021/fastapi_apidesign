from component.snowFlakeId import snowFlack
from sqlalchemy import Column, DateTime, Float, ForeignKey, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, ENUM, INTEGER, VARCHAR
from sqlalchemy.orm import relationship

from .autogeneratedmodel import Base
from UserRole import UserRole
class User(Base):
    __tablename__ = 'user'
    __eager_defaults__ = ("user_role",)
    id = Column(BIGINT, primary_key=True,default=snowFlack.getId)
    username = Column(VARCHAR(32), nullable=False, unique=True)
    email = Column(VARCHAR(32), index=True)
    phone = Column(VARCHAR(16), index=True)
    balance = Column(Float(asdecimal=True), server_default=text("'0'"))
    password = Column(VARCHAR(512), nullable=False)
    gender = Column(ENUM('man', 'woman'))
    is_deleted = Column(INTEGER(255), server_default=text("'0'"))
    user_role = Column(INTEGER(11),nullable=False,default=0,server_default=text("'0'"))

    @property
    def is_admin(self)->int:
        if not self.user_role:
            self.user_role =0
        return self.user_role & UserRole.admin.value

    def set_admin(self, value:bool)->None:
        if not self.user_role:
            self.user_role = 0
        if value:
            self.user_role = self.user_role | UserRole.admin.value
        else:
            self.user_role=self.user_role & (UserRole.admin.value-1)
