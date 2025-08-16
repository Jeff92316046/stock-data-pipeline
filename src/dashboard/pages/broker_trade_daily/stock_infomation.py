from datetime import date
import streamlit as st
from streamlit_searchbox import st_searchbox
from dashboard.service import (
    search_stock_by_name,
    search_stock_by_symbol,
    get_broker_trade_daily
)

st.title("買賣日報表")

search_mode = st.radio(
    "查詢方式", ["股票代號搜尋", "名稱搜尋"], index=0, horizontal=True
)
stock_symbol = None

if search_mode == "名稱搜尋":
    selected = st_searchbox(
        search_stock_by_name, key="stock_name_search", placeholder="搜尋股票名稱"
    )
    if selected:
        stock_symbol = selected

elif search_mode == "股票代號搜尋":
    selected = st_searchbox(
        search_stock_by_symbol,
        key="stock_symbol_search",
        placeholder="搜尋股票代碼",
    )
    if selected:
        stock_symbol = selected

if stock_symbol:
    st.write("你選擇的是：", stock_symbol)
else:
    st.write("請完成輸入以繼續")

if stock_symbol:
    st.subheader(f"券商交易日報 - {stock_symbol}")

    date_range = st.date_input(
        "選擇日期或日期區間",
        value=(date.today(), date.today())
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

    trades = get_broker_trade_daily(stock_symbol,start_date,end_date)

    if trades:
        st.dataframe(
            [
                {
                    "日期": t.trade_date,
                    "券商代號": t.broker_code,
                    "券商名稱": t.broker_name,
                    "價格": t.price,
                    "買進股數": t.buy_volume,
                    "賣出股數": t.sell_volume,
                }
                for t in trades
            ],
            use_container_width=True,
            height=1000,
        )
    else:
        st.info("查無交易資料")