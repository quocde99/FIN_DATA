import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

Symbols = ["DXG", "FLC", "FPT"]
FIN_DATA_URL = "http://ra.vcsc.com.vn/Financial/PV_BalanceSheet?ticker={stock_symbol}&filter=0&unit=1000000000"


def getHTMLdocument(url, symbol):
    print(url.format(stock_symbol=symbol))
    response = requests.get(url.format(stock_symbol=symbol))
    return response.text


def get_data_table(group):
    array_data = []
    dict = {"class": "financial-block", "group": group}
    financial_block = soup.findAll("div", dict)
    for elements in financial_block:
        p_element = elements.findAll("p")
        arr = []
        for p in p_element:
            arr.append(p.get_text().strip())
        array_data.append(arr)
    result = pd.DataFrame(array_data[1:len(array_data)], columns=array_data[0])
    return result


def find_start_year(soup):
    li_tag = soup.find("li")
    year_start = li_tag.find("p").get_text().strip()
    return int(year_start)


if __name__ == '__main__':
    all = pd.DataFrame()
    for symbol in Symbols:
        html_document = getHTMLdocument(FIN_DATA_URL, symbol)
        soup = BeautifulSoup(html_document, 'html.parser')
        year_start = find_start_year(soup)
        print(year_start)
        result = pd.DataFrame()
        for i in range(1, 8, 1):
            df = get_data_table(i)
            result = pd.concat([result, df], axis=1)
        year = pd.DataFrame(np.arange(year_start, 2022, 1), columns=["Year"])
        sym = pd.DataFrame(np.full((1, 2022 - year_start), symbol).flatten(), columns=["Symbol"])
        result = pd.concat([result, year, sym], axis=1)
        all = pd.concat([all, result], ignore_index=True)
    all = all.to_csv("info.csv", encoding='utf-8-sig')
