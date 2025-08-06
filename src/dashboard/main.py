import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.service import handle_stocksd_chart


def reset_slider(change_key,change_value):
    st.session_state[change_key] = change_value


def main():
    st.title("股票數據分析")

    stock_symbol = st.text_input("輸入股票代號")
    if st.button("確認"):
        st.write(f"目前選擇的股票: {stock_symbol}")

    col1, col2 = st.columns([4, 1])

    if "range_values1" not in st.session_state:
        st.session_state.range_values1 = (10, 15)

    with col1:
        st.slider("大股東範圍", min_value=1, max_value=15, key="range_values1")

    with col2:
        st.markdown("")
        st.markdown("")
        st.button("重置",key="button1", on_click=reset_slider, args=["range_values1",(10, 15)])

    col1, col2 = st.columns([4, 1])

    if "range_values2" not in st.session_state:
        st.session_state.range_values2 = (1, 100)

    with col1:
        st.slider(
            "大股東持有率%上下限", min_value=1, max_value=100, key="range_values2"
        )

    with col2:
        st.markdown("")
        st.markdown("")
        st.button("重置",key="button2",on_click=reset_slider, args=["range_values2",(1, 100)])

    dark_mode = st.session_state.get("theme", "") == "dark"
    bar_color = "#00BFFF" if dark_mode else "#1E90FF"
    line_color = "#00FF7F" if dark_mode else "#32CD32"

    data = handle_stocksd_chart(stock_symbol, st.session_state.range_values1)
    df = pd.DataFrame(data)
    df["日期"] = pd.to_datetime(df["日期"], format="%Y%m%d")

    fig = px.bar(
        df,
        x="日期",
        y="總股東人數",
        title="股東人數變化",
        color_discrete_sequence=[bar_color],
    )
    fig.add_scatter(
        x=df["日期"],
        y=df["大股東持有率"],
        mode="lines+markers",
        name="大股東持有率",
        yaxis="y2",
        line={"color": line_color},
    )

    fig.update_layout(
        xaxis={"type": "date", "tickformat": "%Y-%m-%d"},
        yaxis={"title": "總股東人數"},
        yaxis2={
            "overlaying": "y",
            "side": "right",
            "title": "大股東持有率 (%)",
            "range": [
                st.session_state.range_values2[0],
                st.session_state.range_values2[1],
            ],
            "showgrid": False,
        },
        title="股東人數變化與大股東持有率",
    )

    st.plotly_chart(fig)

    st.subheader("歷史數據")
    df["日期"] = df["日期"].dt.strftime("%Y-%m-%d")
    st.dataframe(df[::-1],hide_index=True,use_container_width=True)


if __name__ == "__main__":
    main()
