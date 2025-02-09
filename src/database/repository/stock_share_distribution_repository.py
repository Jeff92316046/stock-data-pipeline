from model import StockShareDistribution as stockSD
from db_helper import get_db
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.cursor import CursorResult


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
    session.commit()
    return result.rowcount

def upsert_stock_share_distributions(stock_sds: list[stockSD]):
    session = next(get_db())
    stmt = postgresql.insert(stockSD).values(
        [stock_sd.model_dump(exclude={"id"}) for stock_sd in stock_sds]
    )
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["stock_symbol", "date_time", "holding_order"]
    )
    result: CursorResult = session.exec(stmt)
    session.commit()
    return result.rowcount
