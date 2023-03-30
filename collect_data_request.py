#import necessary modules and packages
import sys
from time import time_ns

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


def collect_data(**args):
    """
    Send a request to the server and parse the table, and return the dataset
    """
    static_url = "http://115.124.110.196:8080/epeek/rptViewDist.jsp?ccode=-&blk=-&\
                dist=-&div=amravati&season=खरीप&divName=अमरावती&distName=सर्व&blkName=सर्व&ccodeName=सर्व&seasonName=खरीप"
    URL = f"http://115.124.110.196:8080/epeek/rptViewDist.jsp?ccode=-&blk=-&dist=-&\
        div={args['division_en']}&season={args['season']}&divName={args['division']}&distName={args['district']}\
        &blkName=सर्व&ccodeName=सर्व&seasonName={args['season']}"
    page = requests.get(static_url) # reads html pages

    html_content = bs(page.content, "html.parser") #parsing using beautiful soup

    print(URL)
    print(static_url)

    html_result_table =  html_content.find('table')# find out table
    rows = html_result_table.find_all('tr')

    row = 1 # header row is not required, since manually added
    data_list = []
    while(row < len(rows)-2): # last row is not requered. Since the table is common, and for easy and clean code, avoided another loop
        data = {}
        data['sl_no'] = rows[row].find_all('td')[0].text.strip() # identified column value and strip to avoid spaces
        data['village'] = rows[row].find_all('td')[1].text.strip()
        data['survey_account_number'] = rows[row].find_all('td')[2].text.strip()
        data['peak_monitoring_area'] = rows[row].find_all('td')[3].text.strip()
        data['permanent_area'] = rows[row].find_all('td')[4].text.strip()
        data['current_area'] = rows[row].find_all('td')[5].text.strip()
        data['total_area'] = rows[row].find_all('td')[6].text.strip()
        row +=1
        data_list.append(data)
    
    return data_list

def create_csv(data_list):
    """
    Function to create a csv file
    """
    df = pd.DataFrame(data_list)
    df.to_csv(f'data/data_{time_ns()}.csv')

def main():
    """
    Main funtion
    """
    data_set = collect_data(division_en=sys.argv[1], season=sys.argv[2], division=sys.argv[3], district=sys.argv[4])
    create_csv(data_set)

if __name__ == '__main__':
    main()

