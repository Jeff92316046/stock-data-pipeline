from model import StockList, StockShareDistribution as stockSD

from utils.db_helper import get_db


def find_last_date_and_set():
    db_session = next(get_db())
    stock_list = db_session.query(StockList).all()
    for i in stock_list:
        last_updated_date = (
            db_session.query(stockSD)
            .filter_by(stock_symbol=i.stock_symbol)
            .order_by(stockSD.date_time.desc())
            .first()
        )
        i.last_updated_at = last_updated_date.date_time
        print(i.stock_symbol, last_updated_date.date_time)
    db_session.commit()
