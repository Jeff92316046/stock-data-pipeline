import streamlit as st
from database.repository.broker_trade_dialy_repository import (
    insert_stock_to_watchlist,
    delete_stock_from_watchlist,
    get_all_watchlist_with_stock_name,
)

st.subheader("新增股票")
new_stock = st.text_input("輸入股票代號（例: 2330, 2317）")
if st.button("新增"):
    for code in new_stock.split(","):
        insert_stock_to_watchlist(code.strip())
    st.rerun()

st.subheader("追蹤名單")
watchlist = get_all_watchlist_with_stock_name()
if watchlist:
    for idx, (symbol, name, wid) in enumerate(get_all_watchlist_with_stock_name()):
        col = st.container(horizontal=True)
        with col:
            st.markdown(f"##### {symbol} - {name}",width="content")
            if st.button("❌", key=f"del_{wid}"):
                delete_stock_from_watchlist(wid)
                st.rerun()
        if idx < len(watchlist) - 1:
            st.divider()
else:
    st.info("目前沒有任何追蹤股票")
