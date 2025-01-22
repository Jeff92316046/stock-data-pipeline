from model import StockList
from utils.db_helper import get_db
from sqlalchemy.dialects.postgresql import insert
from prefect import task
from prefect.logging import get_run_logger

@task
def get_all_stock():
    db_session = next(get_db())
    stock_list = db_session.query(StockList).all()
    return stock_list

@task
def get_stock_by_symbol(stock_symbol):
    db_session = next(get_db())
    stock = db_session.query(StockList).filter_by(stock_symbol=stock_symbol).first()
    return stock

@task
def get_stock_last_updated_date_by_symbol(stock_symbol):
    db_session = next(get_db())
    stock = db_session.query(StockList).filter_by(stock_symbol=stock_symbol).first()
    return stock.last_updated_at

@task
def upsert_stock_by_symbol(stock_symbol, stock_name):
    db_session = next(get_db())
    stmt = insert(StockList).values(
        {"stock_symbol": stock_symbol, "stock_name": stock_name}
    )
    stmt = stmt.on_conflict_do_nothing(index_elements=["stock_symbol"])
    result = db_session.execute(stmt)
    if result.rowcount == 1:
        get_run_logger().info(f"Stock {stock_symbol} stock name {stock_name} inserted")
    db_session.commit()
    
    
@task
def update_stock_date_by_symbol(stock_symbol, last_updated_at):
    db_session = next(get_db())
    stock = db_session.query(StockList).filter_by(stock_symbol=stock_symbol).first()
    stock.last_updated_at = last_updated_at
    db_session.commit()
    get_run_logger().info(f"Stock {stock_symbol} last updated at {last_updated_at}")