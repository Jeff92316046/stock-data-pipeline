from datetime import date
from sqlmodel import select
from database.model import BrokerTradeDaily, BrokerTradeWatchlist, Stocks
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


def get_all_watchlist_with_stock_name():
    with get_db() as session:
        result = session.exec(
            select(BrokerTradeWatchlist.stock_symbol, Stocks.stock_name, BrokerTradeWatchlist.id)
            .join(Stocks, BrokerTradeWatchlist.stock_symbol == Stocks.stock_symbol)
            .order_by(BrokerTradeWatchlist.stock_symbol)
        ).all()
        return result


def insert_stock_to_watchlist(stock_symbol):
    with get_db() as session:
        watch = BrokerTradeWatchlist(stock_symbol=stock_symbol, created_at=date.today())
        session.add(watch)
        session.commit()


def delete_stock_from_watchlist(stock_id):
    with get_db() as session:
        stock = session.get(BrokerTradeWatchlist, stock_id)
        if stock:
            session.delete(stock)
            session.commit()

def get_broker_trade_daily_with_date_and_stoke_symbol(stock_symbol:str,start_date:date,end_date:date):
    with get_db() as session:
        trades = session.exec(
            select(BrokerTradeDaily)
            .where(
                (BrokerTradeDaily.stock_symbol == stock_symbol) &
                (BrokerTradeDaily.trade_date >= start_date) &
                (BrokerTradeDaily.trade_date <= end_date)
            )
            .order_by(BrokerTradeDaily.trade_date, BrokerTradeDaily.sequence_no)
        ).all()
    return trades