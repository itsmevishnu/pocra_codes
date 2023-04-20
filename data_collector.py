#importing necessary packages and modules
from time import time_ns
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd

def generate_url(kargs):
    """
    This function generate appropriate urls for request.
    The values are taken from the input
    """
    base_url = "http://115.124.110.196:8080/epeek/"
    # ccode
    village_code = kargs["village_code"]
    # blk
    block_code = kargs["block_code"]
    # dist
    district_code = kargs["district_code"]
    # div
    en_division_name = kargs["en_division_name"]
    # season
    mr_season_name = kargs["mr_season_name"]
    # divName
    mr_division_name = kargs["mr_division_name"]
    # distName
    mr_district_name = kargs["mr_district_name"]
    # blkName
    mr_block_name = kargs["mr_block_name"]
    # ccodeName
    mr_village_name = kargs["mr_village_name"]

    url_params = ''

    if en_division_name == '-':
        url_params =  f"rptViewDiv.jsp?div=pune&season={mr_season_name}&divName={mr_division_name}&distName={mr_district_name}&blkName={mr_block_name}&ccodeName={mr_village_name}&seasonName={mr_season_name}"
    elif district_code == '-':
        url_params = f"rptViewDist.jsp?ccode={village_code}&blk={block_code}&dist={district_code}&div={en_division_name}&season={mr_season_name}&divName={mr_division_name}&distName={mr_district_name}&blkName={mr_block_name}&ccodeName={mr_village_name}&seasonName={mr_season_name}"
    elif block_code == '-':
        url_params = f"rptViewBlk.jsp?ccode={village_code}&blk={block_code}&dist={district_code}&div={en_division_name}&season={mr_season_name}&divName={mr_division_name}&distName={mr_district_name}&blkName={mr_block_name}&ccodeName={mr_village_name}&seasonName={mr_season_name}"
    elif village_code == '-':
        url_params = f"rptViewVill.jsp?ccode={village_code}&blk={block_code}&dist={district_code}&div={en_division_name}&season={mr_season_name}&divName={mr_division_name}&distName={mr_district_name}&blkName={mr_block_name}&ccodeName={mr_village_name}&seasonName={mr_season_name}"
    else:
        url_params = f"rptViewKhateNew.jsp?ccode={village_code}&blk={block_code}&dist={district_code}&div={en_division_name}&season={mr_season_name}&divName={mr_division_name}&distName={mr_district_name}&blkName={mr_block_name}&ccodeName={mr_block_name}&seasonName={mr_season_name}"

    url = base_url + url_params

    return url

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

def generate_csv(data_list, headers):
    """
    Function generate a csv file using pandas
    """
    data_set = pd.DataFrame(data_list, columns=headers)
    data_set.to_csv(f"data/data_{time_ns()}.csv")

def read_values():
    """
    Function reading all necessary values from keyboard
    """
    required_values = {}

    required_values["village_code"] = input("Enter village code or enter -\n")
    # blk
    required_values["block_code"]= input("Enter block code or enter -\n")
    # dist
    required_values["district_code"] = input("Enter district code or enter -\n")
    # div
    required_values["en_division_name"] = input("Enter division name in English or enter -\n")
    # season
    required_values["mr_season_name"] = input("Enter seson name in Marathi\n")
    # divName
    required_values["mr_division_name"] = input("Enter division name in Marathi\n")
    # distName
    required_values["mr_district_name"] = input("Enter disttrict name in Marathi\n")
    # blkName
    required_values["mr_block_name"] = input("Enter block name in Marathi\n")
    # ccodeName
    required_values["mr_village_name"] = input("Enter village name in Marathi\n")

    return required_values

def main():
    """
    Main function
    """
    values = read_values()

    print("Fetching the data started")
    
    url = generate_url(values)

    print(f"URL generated:{url}")

    print("Collecting data from the URL...")

    headers, data = get_data(url)

    print("Generating data file...")
    generate_csv(data, headers)

    print("Process completed!")


if __name__ == '__main__':
    main()
