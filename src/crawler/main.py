from scraping.get_stock_data import update_all_stocksd_data
from scraping.update_stock_list import update_stock_list
from prefect import flow

@flow
def main():
    update_stock_list()
    update_all_stocksd_data()

if __name__ == "__main__":
    main.serve(name="stock-crawler")