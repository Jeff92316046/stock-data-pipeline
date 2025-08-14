import csv
import re
import time
import cv2
import numpy as np
import requests
from datetime import date
from crawler.utils.selenuim_helper import ID, XPATH, get_driver
from crawler.utils.ocr_helper import ocr_captcha_onnx
from database.model import BrokerTradeDaily
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver as LocalWebDriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from prefect import task
from prefect.logging import get_run_logger
from prefect.cache_policies import NO_CACHE

from database.repository.broker_trade_dialy_repository import (
    get_all_broker_trade_watchlist,
    upsert_broker_trade_dailies,
)

URL = "https://bsr.twse.com.tw/bshtm/bsMenu.aspx"


@task
def get_stock_broker_trade_daily_in_watchlist():
    stock_list = get_all_broker_trade_watchlist()
    with get_driver(True) as driver:
        for stock_symbol in stock_list:
            fetch_single_broker_trade_daily(driver, stock_symbol)


@task(cache_policy=NO_CACHE, retries=10)
def fetch_single_broker_trade_daily(
    driver: LocalWebDriver | RemoteWebDriver, stock_symbol: str
):
    try:
        driver.get(URL)
        driver.implicitly_wait(5)

        img = driver.find_element(
            XPATH,
            '//*[@id="Panel_bshtm"]/table/tbody/tr/td/table/tbody/tr[1]/td/div/div[1]/img',
        )
        img_bytes = img.screenshot_as_png
        img_array = np.frombuffer(img_bytes, np.uint8)
        img_mat = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        predicted_string = ocr_captcha_onnx(img_mat)

        captcha_input = driver.find_element(
            XPATH,
            '//*[@id="Panel_bshtm"]/table/tbody/tr/td/table/tbody/tr[1]/td/div/div[2]/input',
        )
        captcha_input.clear()
        captcha_input.send_keys(predicted_string)
        print(f"[DEBUG] Captcha: {predicted_string}")
        time.sleep(2)

        stock_symbol_inputbox = driver.find_element(XPATH, '//*[@id="TextBox_Stkno"]')
        stock_symbol_inputbox.clear()
        stock_symbol_inputbox.send_keys(stock_symbol)
        time.sleep(2)

        driver.find_element(XPATH, '//*[@id="btnOK"]').click()
        time.sleep(3)

        error_label = driver.find_element(ID, "Label_ErrorMsg").text.strip()
        if error_label == "查無資料":
            get_run_logger().info(
                f"stock {stock_symbol} date {date.today()} data not exist"
            )
            return

        stock_data_link = driver.find_element(ID, "HyperLink_DownloadCSV")
        download_url = stock_data_link.get_attribute("href")

        cookies = {c["name"]: c["value"] for c in driver.get_cookies()}

        resp = requests.get(download_url, cookies=cookies)

        result = parse_broker_trade_daily(
            resp.content, stock_symbol=stock_symbol, trade_date=date.today()
        )
        if result == 0:
            get_run_logger().warning(
                f"stock {stock_symbol} date {date.today()} is already exists"
            )
        else:
            get_run_logger().info(f"stock {stock_symbol} date {date.today()} inserted")

        get_run_logger().info(f"stock {stock_symbol} date {date.today()} inserted")
    except NoSuchElementException:
        get_run_logger().error(f"ocr error {stock_symbol}, retrying...")
        raise NoSuchElementException("ocr error")
    except Exception as e:
        get_run_logger().error(f"Skipping {stock_symbol}\n{e}")


def parse_broker_trade_daily(file_bytes: bytes, stock_symbol: str, trade_date: date):
    results: list["BrokerTradeDaily"] = []

    decoded_text = file_bytes.decode("big5", errors="ignore")

    reader = csv.reader(decoded_text.splitlines())
    next(reader)  # 券商買賣股票成交價量資訊
    next(reader)  # 股票代碼,0050
    next(reader)  # 序號,券商,價格,買進股數,賣出股數,,序號,券商,價格,買進股數,賣出股數
    for row in reader:
        if row[0].strip():
            code, name = split_broker_code_name(row[1])
            results.append(
                BrokerTradeDaily(
                    stock_symbol=stock_symbol,
                    trade_date=trade_date,
                    sequence_no=int(row[0]),
                    broker_code=code,
                    broker_name=name,
                    price=float(row[2]),
                    buy_volume=int(row[3]),
                    sell_volume=int(row[4]),
                )
            )

        if len(row) >= 11 and row[6].strip():
            code, name = split_broker_code_name(row[7])
            results.append(
                BrokerTradeDaily(
                    stock_symbol=stock_symbol,
                    trade_date=trade_date,
                    sequence_no=int(row[6]),
                    broker_code=code,
                    broker_name=name,
                    price=float(row[8]),
                    buy_volume=int(row[9]),
                    sell_volume=int(row[10]),
                )
            )
    result = upsert_broker_trade_dailies(results)
    return result


def split_broker_code_name(text: str) -> tuple[str, str]:
    """
    broker name format example:
    '1020合　　庫'  → ('1020', '合庫')
    '592a元富松德' → ('592a', '元富松德')
    """
    cleaned = text.replace("\u3000", "").replace(" ", "").strip()

    match = re.match(r"^([0-9a-zA-Z]+)(.+)$", cleaned)
    if match:
        return match.group(1), match.group(2).strip()
    return "", cleaned
