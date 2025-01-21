import json
from utils.db_helper import Base
from sqlalchemy import (
    String,
    Integer,
    UnicodeText,
    Date,
    ForeignKey,
    Column,
    BIGINT,
    UniqueConstraint
)
from sqlalchemy.inspection import inspect

class HelperMixin:
    def to_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }

class StockList(Base,HelperMixin):
    __tablename__ = "stock_list"
    stock_symbol = Column(String(length=20),primary_key=True,nullable=False)
    stock_name = Column(UnicodeText(),nullable=True)
    last_updated_at = Column(Date(),nullable=True)

class StockShareDistribution(Base,HelperMixin):
    __tablename__ = "stock_share_distribution"
    id = Column(Integer(),primary_key=True,nullable=False, autoincrement=True)
    stock_symbol = Column(String(length=20),ForeignKey("stock_list.stock_symbol"))
    date_time = Column(Date())
    holding_order = Column(Integer())
    number_of_holder = Column(Integer())
    shares = Column(BIGINT())
    created_at = Column(Date())
    __table_args__ = (
        UniqueConstraint('stock_symbol','date_time','holding_order',name='uix_stock_distribution'),
    )