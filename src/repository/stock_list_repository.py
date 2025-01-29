from model import Stocks
from sqlalchemy.dialects import postgresql
from prefect import task
from prefect.logging import get_run_logger
from sqlmodel import select
from sqlalchemy.engine.cursor import CursorResult

from utils.db_helper import get_db, engine


@task
def get_all_stock():
    session = next(get_db())
    stmt = select(Stocks)
    stock_list = session.exec(stmt).all()
    return stock_list


@task
def get_all_stock_symbol():
    session = next(get_db())
    stmt = select(Stocks.stock_symbol)
    stock_list = session.exec(stmt).all()
    return stock_list


@task
def get_stock_by_symbol(stock_symbol):
    session = next(get_db())
    stmt = select(Stocks).where(Stocks.stock_symbol == stock_symbol)
    stock = session.exec(stmt).one()
    return stock


@task
def get_stock_last_updated_date_by_symbol(stock_symbol):
    session = next(get_db())
    stmt = select(Stocks).where(Stocks.stock_symbol == stock_symbol)
    stock = session.exec(stmt).one()
    return stock.last_updated_at


@task
def upsert_stock_by_symbol(stock_symbol, stock_name):
    session = next(get_db())
    stmt = postgresql.insert(Stocks).values(
        {"stock_symbol": stock_symbol, "stock_name": stock_name}
    )
    stmt = stmt.on_conflict_do_nothing(index_elements=["stock_symbol"])
    result: CursorResult = session.exec(stmt)
    if result.rowcount == 1:
        get_run_logger().info(f"Stock {stock_symbol} stock name {stock_name} inserted")
    session.commit()


@task
def update_stock_date_by_symbol(stock_symbol, last_updated_at):
    session = next(get_db())
    statment = select(Stocks).where(Stocks.stock_symbol == stock_symbol)
    stock = session.exec(statment).one()
    stock.last_updated_at = last_updated_at
    session.commit()
    get_run_logger().info(f"Stock {stock_symbol} last updated at {last_updated_at}")
