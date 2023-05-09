#importing necessary packages and modules
import os

from time import time_ns
# from selenium import webdriver
# from selenium.webdriver.common.by import By
import requests

from bs4 import BeautifulSoup as bs
import pandas as pd

def get_data(url):
    """
    Function open selenium driver and collect required information using beautiful soup
    """
    # browser = webdriver.Firefox() #open web browser
    # browser.implicitly_wait(4)
    # browser.get(url)
    # #Below code execute if the object present in the result page
    # try:
    #     object_content = browser.find_element(By.TAG_NAME, 'object')
    #     if bool(object_content):
    #         browser.switch_to.frame(object_content)
    # except Exception as e: 
    #     pass 
    
    response = requests.get(url)
    
    #Checks the response is 200 OK.
    if response.status_code != 200:
        raise(f"There is some error in response,{response.status_code}")

    #Starts parsing html content
    html_content = bs(response.content, "html.parser")
    # browser.close()

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

def get_data_for_db(url):
    response = requests.get(url['url'])
    #Starts parsing html content
    html_content = bs(response.content, "html.parser")
    html_result_table =  html_content.find('table')
    rows = html_result_table.findAll("tr")
    data_list = []
    for i in range(1, len(rows)-2):
        data_row = {}
        cols = rows[i].find_all('td')
        data_row['name'] = cols[1].text.strip()
        data_row['account_number'] = cols[2].text.strip()
        data_row['group_number'] = cols[3].text.strip()
        data_row['crop_inspection_date'] = cols[4].text.strip()
        data_row['crop_name'] = cols[5].text.strip()
        data_row['crop_type'] = cols[6].text.strip()
        data_row['area'] = cols[7].text.strip()
        data_row['season'] = url['season']
        data_row['village'] = url['village_code']
        data_list.append(data_row)
    
    return data_list 

