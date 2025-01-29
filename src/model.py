from sqlmodel import TEXT, String, SQLModel, Field, Relationship,BIGINT,Column
from datetime import date, datetime
from sqlalchemy import UniqueConstraint,Column


class Stocks(SQLModel, table=True):  # 加上 table=True 表示這是一個數據表
    __tablename__ = "stocks"
    stock_symbol: str = Field(primary_key=True, max_length=20,sa_type=String)
    stock_name: str | None = Field(default=None,sa_type=TEXT)
    last_updated_at: date | None = Field(default=None)

    distributions: list["StockShareDistribution"] = Relationship(back_populates="stock")


class StockShareDistribution(SQLModel, table=True):
    __tablename__ = "stock_share_distribution"
    id: int | None = Field(default=None, primary_key=True)
    stock_symbol: str = Field(foreign_key="stocks.stock_symbol", max_length=20,sa_type=String)
    date_time: date = Field(default=None)
    holding_order: int = Field(default=None)
    number_of_holder: int | None = Field(default=None)
    shares: int | None = Field(default=None,sa_column=Column(BIGINT))
    created_at: date | None = Field(default=None)

    __table_args__ = (
        UniqueConstraint(
            "stock_symbol", "date_time", "holding_order", name="uix_stock_distribution"
        ),
    )

    stock: Stocks = Relationship(back_populates="distributions")
