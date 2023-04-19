#Imports necessary files
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


#global variables
base_url = "http://115.124.110.196:8080/epeek"


def get_all_districts(division):
    """
    Get the list of all districts from the web portal
    Input : Division name
    Return : Array of object of districts with name and code.
    """
    url = f"{base_url}/fillDistrict.jsp?div={division}"
    district_response = requests.get(url)

    try:
        html_content = bs(district_response.content, "html.parser")
    except Exception as e:
        print("Some error occured during collecting information of districts")
        return

    values  = html_content.findAll("option")
    values.pop(0) # remove the first values for every line
    districts = []
    for value in values:
        row = {}
        row["division"] = division
        row['district_code'] = value["value"]
        row['district'] = value.text
        districts.append(row)
    
    return districts


def get_all_talukas(district):
    """
    Get the list of all taluka under the district.
    Input: District name
    Return : Array of Object of taluka with name and code.
    """
   
    url = f"{base_url}/fillTaluka.jsp?dist={district['district_code']}&div={district['division']}"
    try:
        taluka_response = requests.get(url)
    except Exception as e:
        print("Some error occure during collecting information of taluka")
        return

    html_content = bs(taluka_response.content, "html.parser")
    values  = html_content.findAll("option")
    values.pop(0) # remove the first values for every line
    taluka = []
    for value in values:
        row = {}
        row["division"] = district['division']
        row["district"] = district["district"]
        row['district_code'] = district["district_code"]
        row['taluka_code'] = value["value"]
        row['taluka'] = value.text
        taluka.append(row)
    
    return taluka

def get_all_villages(taluka):
    """
    Get the list of all villages under the given taluka
    Input: all information about the taluka
    Return: Arry of objects of villages with name and code
    """
    url = f"{base_url}/fillVillage.jsp?dist={taluka['district_code']}&blk={taluka['taluka_code']}&div={taluka['division']}"
    try:
        village_response = requests.get(url)
    except Exception as e:
        print("Some error occured during the village data collection")
        return

    html_content = bs(village_response.content, 'html.parser')
    values =  html_content.findAll("option")
    values.pop(0) #remove the first element (for all)
    village = []
    for value in values:
        row = {}
        row["division"] = taluka['division']
        row["district"] = taluka["district"]
        row['district_code'] = taluka["district_code"]
        row['taluka_code'] = taluka["taluka_code"]
        row['taluka'] = taluka["taluka"]
        row["village_code"] = value["value"]
        row["village"] = value.text
        village.append(row)
    
    return village

def get_villages(district_code, taluka_code, division):
    """
    Get the list of all villages under a paricular village
    Input: all information about the taluka
    Return: Arry of objects of villages with name and code
    """
    url = f"{base_url}/fillVillage.jsp?dist={district_code}&blk={taluka_code}&div={division}"
    village_response = requests.get(url)
    html_content = bs(village_response.content, 'html.parser')
    values =  html_content.findAll("option")
    values.pop(0) #remove the first element (for all)
    villages = []
    for value in values:
        row = {}
        row["division"] = division
        # row["district"] = taluka["district"]
        row['district_code'] = district_code
        row['taluka_code'] =taluka_code
        row["village_code"] = value["value"]
        row["village"] = value.text
        villages.append(row)
    
    return villages


def create_data_file(dataset, file_name="all_village_data"):
    """
    Creates a file in data folder.
    """
    village_data_set = pd.DataFrame(dataset)
    village_data_set.to_csv(f"data/{file_name}.csv")


def get_all_village_info_file():
    """
    Calls all functions and write the data into file
    """
    divisions = ["amravati", "aurangabad", "kokan", "nagpur", "nashik", "pune"] 
    district_set = []
    taluka_set = []
    village_set = []
    
    
    print("Start reading district values...")
    for division in divisions: #iterate through all division and collect district data
        district_set += get_all_districts(division)
    
    print("Start reading Taluka values")
    for district in district_set: #iterate through all district and collect taluk data
        taluka_set += get_all_talukas(district)


    print("Start reading village values...")
    for taluka in taluka_set:#iterate through all taluka and collect all village info
        village_set += get_all_villages(taluka)

    print("Start writing to file...")
    create_data_file(village_set)

def read_villages_of_taluka():
    district_code = input("Enter the district code\n")
    taluka_code = input("Enter the taluka_code\n")
    division = input("Enter the division code\n")
    file_name = input("Enter the filenme required\n")

    print("Reading village information")
    village_set = get_villages(district_code, taluka_code, division)

    print("Start writing to file...")
    create_data_file(village_set, file_name)
    
    
def main():
    """
    Main funtion
    """
    choice = int(input("Enter the option\n1. Get all village information\n2. Get village information of a Taluka\n"))
    
    print("Fetching started...")
    if choice == 1:
        get_all_village_info_file()
    else:
        read_villages_of_taluka()
    
    print("The process completed")

if __name__ == '__main__':
    main()