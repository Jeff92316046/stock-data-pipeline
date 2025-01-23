from utils.selenuim_helper import get_driver, XPATH
from prefect import task
from prefect.logging import get_run_logger
from repository.stock_list_repository import upsert_stock_by_symbol


@task(log_prints=False)
def update_stock_list():
    with get_driver() as driver:
        logger = get_run_logger()
        try:
            logger.info("Starting to update stock list")
            driver.get("https://www.tdcc.com.tw/portal/zh/smWeb/psi")
            # 上市
            logger.info("Starting to update stock list of Listed(上市) stock list")
            driver.find_element(
                XPATH, "//*[@id='form1']/table/tbody/tr[6]/td/input"
            ).click()  # 查詢按鈕
            stock_list = driver.find_element(
                XPATH, "//*[@id='body']/div/main/div[6]/div/table/tbody"
            )  # 股票清單table
            stock_list = stock_list.find_elements(XPATH, "./*")  # list股票清單
            for i in stock_list:
                stock_symbol = i.find_element(XPATH, "./td[1]").text
                stock_name = i.find_element(XPATH, "./td[2]").text
                stock_symbol_lenght = len(stock_symbol)
                if stock_symbol_lenght == 4:
                    upsert_stock_by_symbol(
                        stock_symbol, stock_name
                    )  # 只蒐集股票代號長度為4的股票
            logger.info("Finished update stock list of Listed(上市) stock list")
            # 上櫃
            logger.info("Starting to update stock list of OTC(上櫃) stock list")
            driver.find_element(
                XPATH, "//*[@id='marketType1']/option[2]"
            ).click()  # 上櫃選項
            driver.find_element(
                XPATH, "//*[@id='form1']/table/tbody/tr[6]/td/input"
            ).click()  # 查詢按鈕
            stock_list = driver.find_element(
                XPATH, "//*[@id='body']/div/main/div[6]/div/table/tbody"
            )  # 股票清單table
            stock_list = stock_list.find_elements(XPATH, "./*")  # list股票清單
            for i in stock_list:
                stock_symbol = i.find_element(XPATH, "./td[1]").text
                stock_name = i.find_element(XPATH, "./td[2]").text
                stock_symbol_lenght = len(stock_symbol)
                if stock_symbol_lenght == 4:
                    upsert_stock_by_symbol(
                        stock_symbol, stock_name
                    )  # 只蒐集股票代號長度為4的股票
            logger.info("Finished update stock list of OTC(上櫃) stock list")
        except:
            logger.error("Error in update stock list")
