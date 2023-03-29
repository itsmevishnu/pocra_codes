"""
This is a small script for dowloading all table information
into csv format for http://115.124.110.196:8080/epeek/
Inorder to work properly, please install
1. Selenium -  pip install selenium
2. Pandas -pip install pandas
"""

#importing necessary packages
import sys
from time import sleep, time_ns

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import pandas as pd

browser = ''
def modify_inputs(season, division="-", district="-", village="-"):
    """
    This function used to set the fields in the forms given
    By defult the values of division, district and village should be all(-)
    """
    global browser

    #Select the value from the season dropdown
    season_drop = Select(browser.find_element(By.ID, 'seasonOpt'))
    season_drop.select_by_value(season)
    sleep(1)

    #Select the value from the division dropdown
    div_drop = Select(browser.find_element(By.ID, 'divOpt'))
    div_drop.select_by_value(division)
    sleep(1)

    #Select the value from the district dropdown
    dist_drop = Select(browser.find_element(By.ID, 'distOpt'))
    dist_drop.select_by_value(district)
    sleep(1)

    #Select the values from the village dropdown
    village_drop = Select(browser.find_element(By.ID, 'villOpt'))
    village_drop.select_by_value(village)

    #Select button
    button = browser.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/table/tbody/tr[11]/td/button')
    button.click()
    sleep(20)

def generate_csv():
    """
    This method generate the function
    """
    global browser
    object_content = browser.find_element(By.TAG_NAME, 'object')
    browser.switch_to.frame(object_content)

    rows = len(browser.find_elements(By.CSS_SELECTOR, 'tr')) # identify the total rows required
    row = 2
    data_list = []
    while(row < rows-1): # last row is not required for the csv.
        data = {}
        try:
            data['sl_no'] = browser.find_element(By.XPATH,f'//*[@id="tbl_exporttable_to_xls"]/tbody/tr[{row}]/td[1]').text
            data['village'] = browser.find_element(By.XPATH,f'//*[@id="tbl_exporttable_to_xls"]/tbody/tr[{row}]/td[2]').text
            data['survey_account_number'] = browser.find_element(By.XPATH,f'//*[@id="tbl_exporttable_to_xls"]/tbody/tr[{row}]/td[3]').text
            data['peak_monitoring_area'] = browser.find_element(By.XPATH,f'//*[@id="tbl_exporttable_to_xls"]/tbody/tr[{row}]/td[4]').text
            data['permanent_area'] = browser.find_element(By.XPATH,f'//*[@id="tbl_exporttable_to_xls"]/tbody/tr[{row}]/td[5]').text
            data['current_area'] = browser.find_element(By.XPATH,f'//*[@id="tbl_exporttable_to_xls"]/tbody/tr[{row}]/td[6]').text
            data['total_area'] = browser.find_element(By.XPATH,f'//*[@id="tbl_exporttable_to_xls"]/tbody/tr[{row}]/td[7]').text
            
            data_list.append(data)
            row += 1

        except NoSuchElementException:
            break  
        
    data_set = pd.DataFrame(data_list)
    data_set.to_csv(f'data/data_{time_ns()}.csv')
    

def main():
    global browser
    
    URL = "http://115.124.110.196:8080/epeek/"
    
    browser =webdriver.Firefox()
    browser.get(URL)

    browser.implicitly_wait(2) #wait for two second to load the website fully
    modify_inputs(sys.argv[1],sys.argv[2], sys.argv[3],sys.argv[4] )
    generate_csv()
    browser.close()
   

if __name__ == '__main__':
    main()
