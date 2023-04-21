#importing necessary packages and modules
import os

from time import time_ns
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd

def get_data(url):
    """
    Function open selenium driver and collect required information using beautiful soup
    """
    browser = webdriver.Firefox() #open web browser
    browser.implicitly_wait(4)
    browser.get(url)
    #Below code execute if the object present in the result page
    try:
        object_content = browser.find_element(By.TAG_NAME, 'object')
        if bool(object_content):
            browser.switch_to.frame(object_content)
    except Exception as e: 
        pass 
    
    #Starts parsing html content
    html_content = bs(browser.page_source, "html.parser")
    browser.close()

    html_result_table =  html_content.find('table')
    rows = html_result_table.find_all('tr')

    # Fetch the values for header
    header_row_elements = rows[0].find_all('td')
    headers = []
    for col in  header_row_elements:
        headers.append(col.text.strip())
    
    # Fetch the values for rows
    data_list = []
    for i in range(1, len(rows)-2): # dont want the last row
        row_elements = rows[i].find_all('td')
        data_elements = []
        for col in row_elements:
            data_elements.append(col.text.strip())
        
        data_list.append(data_elements)
    
    return (headers, data_list)

def generate_csv(data_list, headers, **args):
    """
    Function generate a csv file using pandas
    Create a folder for each taluka and create csv file with village name as filename
    """
    if not os.path.exists(f"data/{args['district']}/{args['taluka']}"):
        os.makedirs(f"data/{args['district']}/{args['taluka']}")
    data_set = pd.DataFrame(data_list, columns=headers)
    
    data_set.to_csv(f"data/{args['district']}/{args['taluka']}/{args['village']}.csv")