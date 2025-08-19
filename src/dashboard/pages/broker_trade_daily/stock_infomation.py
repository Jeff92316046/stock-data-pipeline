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

    trades = get_broker_trade_daily(stock_symbol, start_date, end_date)

    if trades:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            broker_filter = st.text_input("輸入券商代號或名稱進行篩選")
            apply_filter = st.button("篩選")
        filtered_trades = trades
        if apply_filter and broker_filter:
            broker_filter_lower = broker_filter.lower()
            filtered_trades = [
                t for t in trades
                if broker_filter_lower == t.broker_code.lower()
                or broker_filter_lower == t.broker_name.lower()
            ]
        if filtered_trades:
            total_buy_value = sum(t.buy_volume * t.price for t in filtered_trades if t.buy_volume)
            total_buy_volume = sum(t.buy_volume for t in filtered_trades if t.buy_volume)

            total_sell_value = sum(t.sell_volume * t.price for t in filtered_trades if t.sell_volume)
            total_sell_volume = sum(t.sell_volume for t in filtered_trades if t.sell_volume)

            avg_buy_price = total_buy_value / total_buy_volume if total_buy_volume else 0
            avg_sell_price = total_sell_value / total_sell_volume if total_sell_volume else 0
        with col2:
            st.metric("買進加權平均價",f"{avg_buy_price:.2f}")
            st.metric("賣出加權平均價",f"{avg_sell_price:.2f}")
        with col3:
            st.metric("買進張數",f"{total_buy_volume//1000}")
            st.metric("賣出張數",f"{total_sell_volume//1000}")
        if filtered_trades:
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
                    for t in filtered_trades
                ],
                use_container_width=True,
                height=800,
            )

            

        else:
            st.info("查無符合的券商資料")
    else:
        st.info("查無交易資料")