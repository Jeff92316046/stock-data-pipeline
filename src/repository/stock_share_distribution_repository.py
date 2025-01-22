from model import StockShareDistribution as stockSD
from prefect import task
from prefect.logging import get_run_logger
from utils.db_helper import get_db
from sqlalchemy.dialects.postgresql import insert


@task
def upsert_stock_share_distribution(
    stock_symbol, date_time, holding_order, number_of_holder, shares, created_at
):
    db_session = next(get_db())
    stmt = insert(stockSD).values(
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
    result = db_session.execute(stmt)
    if result.rowcount == 0:
        get_run_logger().warning(
            f"Stock {stock_symbol} date {date_time} holding order {holding_order} already exists"
        )
    db_session.commit()
    return True
