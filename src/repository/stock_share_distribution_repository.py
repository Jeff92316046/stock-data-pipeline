from model import StockShareDistribution as stockSD
from prefect import task
from prefect.logging import get_run_logger
from utils.db_helper import get_db
from sqlmodel import insert, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.orm import Session

@task
def upsert_stock_share_distribution(
    stock_symbol, date_time, holding_order, number_of_holder, shares, created_at
):
    session = next(get_db())
    stmt = postgresql.insert(stockSD).values(
        {
            "stock_symbol": stock_symbol,
            "date_time": date_time,
            "holding_order": holding_order,
            "number_of_holder": number_of_holder,
            "shares": shares,
            "created_at": created_at,
        }
    )
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["stock_symbol", "date_time", "holding_order"]
    )
    result: CursorResult = session.exec(stmt)
    if result.rowcount == 0:
        get_run_logger().warning(
            f"Stock {stock_symbol} date {date_time} holding order {holding_order} already exists"
        )
    session.commit()


# @task
def upsert_stock_share_distributions(stock_SDs: list[stockSD]):
    session = next(get_db())
    stmt = postgresql.insert(stockSD).values(
        [stock_SD.model_dump(exclude_none=True) for stock_SD in stock_SDs]
    )
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["stock_symbol", "date_time", "holding_order"]
    )
    result: CursorResult = session.exec(stmt)
    session.commit()
    if result.rowcount == 0:
        get_run_logger().warning(
            f"Stock {stock_SDs[0].stock_symbol} date {stock_SDs[0].date_time} already exists"
        )
    elif result.rowcount == len(stock_SDs):
        get_run_logger().info(
            f"Stock {stock_SDs[0].stock_symbol} date {stock_SDs[0].date_time} inserted"
        )
    else:
        get_run_logger().warning(
            f"Stock {stock_SDs[0].stock_symbol} date {stock_SDs[0].date_time} some inserted {result.rowcount} of {len(stock_SDs)}"
        )
    
