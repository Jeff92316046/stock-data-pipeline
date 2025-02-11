from model import Stocks
from sqlalchemy.dialects import postgresql
from sqlmodel import select
from sqlalchemy.engine.cursor import CursorResult

from db_helper import get_db


def get_all_stock():
    with get_db() as session:
        stmt = select(Stocks).order_by(Stocks.stock_symbol)
        stock_list = session.exec(stmt).all()
        return stock_list

def get_all_stock_symbol():
    with get_db() as session:
        stmt = select(Stocks.stock_symbol)
        stock_list = session.exec(stmt).all()
        return stock_list

def get_stock_by_symbol(stock_symbol):
    with get_db() as session:
        stmt = select(Stocks).where(Stocks.stock_symbol == stock_symbol)
        stock = session.exec(stmt).one()
        return stock

def get_stock_last_updated_date_by_symbol(stock_symbol):
    with get_db() as session:
        stmt = select(Stocks).where(Stocks.stock_symbol == stock_symbol)
        stock = session.exec(stmt).one()
        return stock.last_updated_at

def upsert_stock_by_symbol(stock_symbol, stock_name):
    with get_db() as session:
        stmt = postgresql.insert(Stocks).values(
            {"stock_symbol": stock_symbol, "stock_name": stock_name}
        )
        stmt = stmt.on_conflict_do_nothing(index_elements=["stock_symbol"])
        result: CursorResult = session.exec(stmt)
        session.commit()
        return result.rowcount

def upsert_stock_date_by_symbol(stock_symbol, last_updated_at):
    with get_db() as session:
        statement = select(Stocks).where(Stocks.stock_symbol == stock_symbol)
        stock = session.exec(statement).first()
        if stock.last_updated_at is None or last_updated_at > stock.last_updated_at:
            stock.last_updated_at = last_updated_at
            session.commit()
