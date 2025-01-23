from sqlalchemy import create_engine, Column, Integer, Text
from model import Base, StockShareDistribution, StockList
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from utils.db_helper import SessionLocal
from twstock import codes
from sqlalchemy.dialects.postgresql import insert


class StockShareDistributionInSqlite(Base):
    __tablename__ = "data"
    id = Column(Integer(), primary_key=True)
    stock = Column(Text())
    date_time = Column(Text())
    number = Column(Integer())
    people = Column(Integer())
    share = Column(Integer())


class StockListInSqlite(Base):
    __tablename__ = "stock_list_1"
    stock = Column(Text(), primary_key=True)
    do_flag = Column(Integer())


sqlite_engine = create_engine("sqlite:///database.db")
SQLiteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SQLiteSession()
postgres_session = SessionLocal()


def stock_data_transfer():
    today = datetime.today()
    sqlite_stock_list = sqlite_session.query(StockListInSqlite).all()
    for j in sqlite_stock_list:
        sqlite_data = (
            sqlite_session.query(StockShareDistributionInSqlite)
            .filter_by(stock=j.stock)
            .distinct()
        )
        print(j.stock)
        for i in sqlite_data:
            temp_date = datetime.strptime(i.date_time, "%Y%m%d").date()
            postgres_stock_data = StockShareDistribution(
                stock_symbol=i.stock,
                date_time=temp_date,
                holding_order=i.number,
                number_of_holder=i.people if i.people != "nod" else None,
                shares=i.share,
                created_at=today,
            )
            new_data = {
                "stock_symbol": postgres_stock_data.stock_symbol,
                "date_time": postgres_stock_data.date_time,
                "holding_order": postgres_stock_data.holding_order,
                "number_of_holder": postgres_stock_data.number_of_holder,
                "shares": postgres_stock_data.shares,
                "created_at": postgres_stock_data.created_at,
            }
            stmt = insert(StockShareDistribution).values(new_data)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=["stock_symbol", "date_time", "holding_order"]
            )
            postgres_session.execute(stmt)

        postgres_session.commit()


def fill_stock_name():
    sqlite_stock_list = sqlite_session.query(StockListInSqlite).all()
    for i in sqlite_stock_list:
        code = codes.get(i.stock, False)
        codes_name = code.name if code else ""
        print(code, codes_name)
        postgres_data = StockList(stock_symbol=i.stock, stock_name=codes_name)
        postgres_session.add(postgres_data)
    postgres_session.commit()
