from sqlalchemy.dialects.mysql import DATETIME
#def defaults_included_constructor(instance, **kwds):
#    for attr, value in kwds.items():
#        setattr(instance, attr, value)
#    for attr in set(getattr(instance, "__eager_defaults__", ())) - set(kwds):
#        column = getattr(type(instance), attr)
#        setattr(instance, attr, column.default.arg)
class Base(object):
    id = Column(BIGINT, primary_key=True,default=snowFlack.getId)
    is_deleted=
Base = declarative_base(cls=MyBase)#constructor=defaults_included_constructor
