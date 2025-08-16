import streamlit as st

if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="expanded"
    )
    broker_trade_daily_stock = st.Page(
        "dashboard/pages/broker_trade_daily/stock_infomation.py",
        title="股票資訊",
        icon=":material/dashboard:",
        url_path="trade-daily",
    )
    broker_trade_daily_watchlist = st.Page(
        "dashboard/pages/broker_trade_daily/watchlist_edition.py",
        title="監視名單",
        icon=":material/playlist_add_check:",
        url_path="trade-daily-watchlist",
    )
    share_distribution_stock = st.Page(
        "dashboard/pages/share_distribution/stock_infomation.py",
        title="股票資訊",
        icon=":material/dashboard:",
        default=True,
        url_path="share-distribution",
    )

    pg = st.navigation(
        {
            "集保戶股權分散表": [share_distribution_stock],
            "買賣日報": [broker_trade_daily_stock, broker_trade_daily_watchlist],
        }
    )

    pg.run()