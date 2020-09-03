import numpy as np
import pandas as pd
import seaborn as sns

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'https://markets.businessinsider.com/commodities/realtime-list'


def extract_rows(table):
    rows = table.findAll('tr')
    return rows

def extract_cell(row):
    str_cells = str(row.findAll('td'))
    cleantext = BeautifulSoup(str_cells, "lxml").get_text()
    return cleantext[1:-1]

def extract_table(url):

    html = urlopen(url)
    soup  = BeautifulSoup(html, 'lxml')
    tables = soup.findAll('table')
    return tables

def extract_column_title(table):
    str_name = str(table.findAll('th'))
    cleantext = BeautifulSoup(str_name, "lxml").get_text()
    return cleantext

def start():
    tables = extract_table(url)
    # title = ''
    for item in tables:
        # title = extract_column_title(item)
        # print(title)
        # input()
        rows = extract_rows(item)
        data = []
        for row in rows:
            data.append(extract_cell(row))
        # print(data)
        df = pd.DataFrame(data)[0].str.split(', ', expand=True)
    df = df.rename(columns=pd.DataFrame(['market, Last, Previous Close, %, ABSOLUTE, Trade Time, Unit'])[0].str.split(', ', expand=True).iloc[0])
    df.dropna(inplace=True)
    print(df)
    
if __name__ == "__main__":
    start()