from sqlmodel import TEXT, String, SQLModel, Field, Relationship, BIGINT, Column
from datetime import date
from sqlalchemy import UniqueConstraint, Column


class Stocks(SQLModel, table=True):
    __tablename__ = "stocks"
    stock_symbol: str = Field(primary_key=True, max_length=20, sa_type=String)
    stock_name: str | None = Field(default=None, sa_type=TEXT)
    last_updated_at: date | None = Field(default=None)

    distributions: list["StockShareDistribution"] = Relationship(back_populates="stock")


class StockShareDistribution(SQLModel, table=True):
    __tablename__ = "stock_share_distribution"
    id: int | None = Field(default=None, primary_key=True)
    stock_symbol: str = Field(
        foreign_key="stocks.stock_symbol", max_length=20, sa_type=String
    )
    date_time: date = Field(default=None)
    holding_order: int = Field(default=None)
    number_of_holder: int | None = Field(default=None)
    shares: int | None = Field(default=None, sa_column=Column(BIGINT))
    created_at: date | None = Field(default=None)

    __table_args__ = (
        UniqueConstraint(
            "stock_symbol", "date_time", "holding_order", name="uix_stock_distribution"
        ),
    )

    stock: Stocks = Relationship(back_populates="distributions")


class BrokerTradeDaily(SQLModel, table=True):
    __tablename__ = "broker_trade_daily"

    id: int | None = Field(default=None, primary_key=True)
    stock_symbol: str = Field(
        foreign_key="stocks.stock_symbol", max_length=20, sa_type=String
    )
    trade_date: date = Field(default=None)
    sequence_no: int = Field(default=None, description="序號")
    broker_code: str = Field(max_length=10, description="券商代號")
    broker_name: str = Field(max_length=50, description="券商名稱")
    price: float = Field(default=None, description="成交價格")
    buy_volume: int | None = Field(
        default=None, sa_column=Column(BIGINT), description="買進股數"
    )
    sell_volume: int | None = Field(
        default=None, sa_column=Column(BIGINT), description="賣出股數"
    )

    __table_args__ = (
        UniqueConstraint(
            "stock_symbol", "trade_date", "sequence_no", name="uix_broker_trade_daily"
        ),
    )

    stock: "Stocks" = Relationship()


class BrokerTradeWatchlist(SQLModel, table=True):
    __tablename__ = "broker_trade_watchlist"

    id: int | None = Field(default=None, primary_key=True)
    stock_symbol: str = Field(foreign_key="stocks.stock_symbol", max_length=20)
    created_at: date = Field(default=None)

    stock: "Stocks" = Relationship()
