import time
from repository.stock_list_repository import get_all_stock
from repository.stock_share_distribution_repository import (
    upsert_stock_share_distributions,
)
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from model import Stocks, StockShareDistribution as StockSD
from utils.selenuim_helper import TAG_NAME, XPATH, get_driver
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime


MAX_CONCURRENT_TASKS = 1
STOCK_SHARE_DISTRIBUTION_URL = "https://www.tdcc.com.tw/portal/zh/smWeb/qryStock"


def parse_stockSD_data(table: WebElement, stock_symbol: str, date: str):
    rows = table.find_elements(TAG_NAME, "tr")
    stockSDs: list[StockSD] = []
    for row in rows:
        columns = row.find_elements(TAG_NAME, "td")
        stockSDs.append(
            StockSD(
                stock_symbol=stock_symbol,
                date_time=datetime.strptime(date, "%Y%m%d").date(),
                holding_order=int(columns[0].text.strip()),
                number_of_holder=int(columns[2].text.strip().replace(",", "")),
                shares=int(columns[3].text.strip().replace(",", "")),
                created_at=datetime.today().date(),
            )
        )
        print(
            (
                stock_symbol,
                datetime.strptime(date, "%Y%m%d").date(),
                int(columns[0].text.strip()),
                int(columns[2].text.strip().replace(",", "")),
                int(columns[3].text.strip().replace(",", "")),
                datetime.today().date(),
            )
        )
    upsert_stock_share_distributions(stockSDs)
    # TODO: update last_updated_at in stocks


def fetch_stockSD_data_by_symbol(stock: Stocks):
    with get_driver(debug=True) as driver:
        try:
            driver.get(STOCK_SHARE_DISTRIBUTION_URL)
            select = driver.find_element(XPATH, "//*[@id='scaDate']")  # 確保 ID 正確
            options = select.find_elements(TAG_NAME, "option")
            last_updated_at = (
                stock.last_updated_at.strftime("%Y%m%d")
                if stock.last_updated_at
                else ""
            )
            newer_dates = [
                option.get_attribute("value")
                for option in options
                if option.get_attribute("value") > last_updated_at
            ]
            driver.find_element(
                XPATH,
                "//*[@id='StockNo']",
            ).send_keys(stock.stock_symbol)
            time.sleep(0.3)
            for date in newer_dates:
                select.find_element(XPATH, f".//option[@value='{date}']").click()
                time.sleep(0.3)
                driver.find_element(
                    XPATH, "//*[@id='form1']/table/tbody/tr[4]/td/input"
                ).click()
                table = driver.find_element(
                    XPATH, "//*[@id='body']/div/main/div[6]/div/table/tbody"
                )
                parse_stockSD_data(table, stock.stock_symbol, date)
                time.sleep(0.3)
            return True
        except Exception as e:
            print(f"Error fetching {stock.stock_symbol}: {e}")
            return False


def update_all_stockSD_data():
    stock_list = get_all_stock()
    success_count = 0
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_TASKS) as executor:
        future_to_code = {
            executor.submit(fetch_stockSD_data_by_symbol, stock): stock
            for stock in stock_list
        }
        for future in as_completed(future_to_code):
            if future.result():
                success_count += 1
    return success_count
