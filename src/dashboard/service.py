from itertools import groupby
from functools import lru_cache
from database.repository.stock_share_distribution_repository import (
    get_stock_share_distribution_by_date,
)
from database.repository.stock_list_repository import (
    search_stocks_by_name_keyword,
    search_stocks_by_symbol_keyword,
)


@lru_cache
def parse_stocksd_data(stock_symbol: str):
    stock_data = get_stock_share_distribution_by_date(stock_symbol)
    stock_data = {
        date_str: list(records)
        for date_str, records in groupby(
            stock_data, key=lambda x: x.date_time.strftime("%Y%m%d")
        )
    }
    return stock_data


@lru_cache
def handle_stocksd_chart(stock_symbol: str, range_values: tuple[int, int]):
    stock_data = parse_stocksd_data(stock_symbol)

    dates = []
    total_holders_list = []
    major_share_ratio_list = []

    for date_str, records in stock_data.items():
        # 直接透過 index 取得 holding_order == 16 的資料
        key_record = records[15]

        # 計算總股東人數
        total_holders = key_record.number_of_holder or 0

        # 計算大股東持有率
        major_share_sum = sum(
            r.shares for r in records[range_values[0] - 1 : range_values[1]]
        )
        major_share_ratio = (
            (major_share_sum / key_record.shares) * 100 if key_record.shares else 0
        )

        # 存入對應列表
        dates.append(date_str)
        total_holders_list.append(total_holders)
        major_share_ratio_list.append(round(major_share_ratio, 2))

    return {
        "日期": dates,
        "總股東人數": total_holders_list,
        "大股東持有率": major_share_ratio_list,
    }


@lru_cache
def search_stock_by_name(name: str):
    results = search_stocks_by_name_keyword(name)
    return [
        (f"{result.stock_symbol} - {result.stock_name}", result.stock_symbol)
        for result in results
    ]


@lru_cache
def search_stock_by_symbol(symbol: str):
    results = search_stocks_by_symbol_keyword(symbol)
    return [
        (f"{result.stock_symbol} - {result.stock_name}", result.stock_symbol)
        for result in results
    ]
