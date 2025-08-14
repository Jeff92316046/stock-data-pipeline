from sqlmodel import select
from database.model import BrokerTradeDaily, BrokerTradeWatchlist
from database.db_helper import get_db
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.cursor import CursorResult


def upsert_broker_trade_dailies(records: list[BrokerTradeDaily]):
    with get_db() as session:
        stmt = postgresql.insert(BrokerTradeDaily).values(
            [record.model_dump(exclude={"id"}) for record in records]
        )
        stmt = stmt.on_conflict_do_nothing(
            index_elements=["stock_symbol", "trade_date", "sequence_no"]
        )
        result: CursorResult = session.exec(stmt)
        session.commit()
        return result.rowcount


def get_all_broker_trade_watchlist() -> list[str]:
    with get_db() as session:
        stmt = select(BrokerTradeWatchlist.stock_symbol)
        stock_list = session.exec(stmt).all()
        return stock_list
