#dont modified this file,it is autogenerated
from component.snowFlakeId import snowFlack
from datetime import datetime
# coding: utf-8
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.dialects.mysql import DATETIME
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .User import User
class MyBase(object):
    id = Column(BIGINT, primary_key=True,default=snowFlack.getId)
    is_deleted=Column(INTEGER)
Base = declarative_base(cls=MyBase)#constructor=defaults_included_constructor


metadata = Base.metadata


class Product(Base):
    __tablename__ = 'product'

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
    is_deleted = Column(DateTime, nullable=False)
    id = Column(BIGINT, primary_key=True,default=snowFlack.getId)
    name = Column(String(64), nullable=False, index=True)
    price = Column(Float, nullable=False)
    presale_starttime = Column(DateTime)
    presale_endtime = Column(DateTime)
    in_presale = Column(INTEGER(11), index=True, server_default=text("'0'"))


class Role(Base):
    __tablename__ = 'role'

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
    is_deleted = Column(DateTime, nullable=False)
    id = Column(BIGINT, primary_key=True,default=snowFlack.getId)
    name = Column(String(16), nullable=False, unique=True)
    mark = Column(String(16))


class Test(Base):
    __tablename__ = 'test'

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
    is_deleted = Column(DateTime, nullable=False)
    id = Column(BIGINT, primary_key=True,default=snowFlack.getId)
    name = Column(String(32))


class Order(Base):
    __tablename__ = 'order'

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
    is_deleted = Column(DateTime, nullable=False)
    id = Column(BIGINT, primary_key=True,default=snowFlack.getId)
    user_id :int = Column(ForeignKey('user.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)

    user:'User' = relationship('User')


class Permission(Base):
    __tablename__ = 'permission'

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
    is_deleted = Column(DateTime, nullable=False)
    id = Column(BIGINT, primary_key=True,default=snowFlack.getId)
    baseurl = Column(String(255), nullable=False)
    action = Column(String(32), nullable=False)
    actionmark = Column(String(32), nullable=False)
    role_id:int = Column(ForeignKey('role.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)

    role:Role = relationship('Role')


class Userrole(Base):
    __tablename__ = 'userrole'

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
    is_deleted = Column(DateTime, nullable=False)
    id = Column(BIGINT, primary_key=True,default=snowFlack.getId)
    role_id:int = Column(ForeignKey('role.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    user_id: int = Column(ForeignKey('user.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)

    role:Role = relationship('Role')
    user:'User' = relationship('User')


class Orderitem(Base):
    __tablename__ = 'orderitem'

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
    is_deleted = Column(DateTime, nullable=False)
    id = Column(BIGINT, primary_key=True,default=snowFlack.getId)
    order_id : int= Column(ForeignKey('order.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    product_id : int  = Column(ForeignKey('product.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)

    order:Order = relationship('Order')
    product:Product = relationship('Product')
