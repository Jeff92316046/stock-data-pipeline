import json
from utils.db_helper import Base
from sqlalchemy import (
    String,
    Integer,
    UnicodeText,
    TIMESTAMP,
    ForeignKey,
    Column
)

class HelperMixin:
    def to_dict(self):
        return json.loads(self.to_json())

class StockList(Base,HelperMixin):
    __tablename__ = "stock_list"
    stock_symbol = Column(String(length=20),primary_key=True,nullable=False)
    stock_name = Column(UnicodeText(),nullable=True)
    last_updated_at = Column(TIMESTAMP(),nullable=True)

class stockShareDistribution(Base,HelperMixin):
    __tablename__ = "stock_share_distribution"
    id = Column(Integer(),primary_key=True,nullable=False, autoincrement=True)
    stock_symbol = Column(String(length=20),ForeignKey("stock_list.stock_symbol"))
    date_time = Column(TIMESTAMP())
    holding_order = Column(Integer())
    number_of_holder = Column(Integer())
    shares = Column(Integer())