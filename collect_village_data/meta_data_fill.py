#Imports necessary files

import pandas as pd
from pocra_database import DatabaseOperations


data_set = pd.read_csv('config/all_village_data.csv')

def fill_division():
    """
    Read the information from the file and insert divisons values to the database
    This is a helper function to read and modify the from file
    """
    divisions = data_set["division"].unique()
    #available tables - divisions, districts, talukas, village
    # #inserting divsion values
    for i, division in enumerate(divisions):
        values={'name': division}
        insert_to_table(table_name='divisions', value_dict=values, num=i, total_num = len(divisions))
        
    print("Division successfully inserted")

def fill_district():
    """
    Read the information from the file and insert into district database
    This is a helper function to read and modify the from file
    """
    districts = data_set[['district_code', 'district']].drop_duplicates()
    dist_data = districts.to_dict(orient="records")
    for i, district in enumerate(dist_data):
        insert_to_table(table_name="districts", value_dict={"district_id":district['district_code'], \
            "name":district['district']} ,
            num=i, total_num=len(dist_data))
    
    print("Districts successfully inserted")
    

def fill_taluka():
    """
    This is a helper function to read and modify the from file
    Read taluka information and store to the database
    """
    talukas =  data_set[['taluka', 'taluka_code', 'district_code']].drop_duplicates()
    taluka_dict = talukas.to_dict(orient='records')
    for i, taluka in enumerate(taluka_dict):
        insert_to_table(table_name="talukas", value_dict={"district_id":taluka['district_code'],\
            "taluka_id":taluka['taluka_code'],"name":taluka['taluka']},
            num=i, total_num=len(taluka_dict) )

    print("Taluka successfully inserted")

def fill_village():
    """
    This is a helper function to read and modify the file and store all the village values.
    """
    villages = data_set[['village', 'village_code', 'district_code', "taluka", "taluka_code", "division"]]
    vilalge_dict = villages.to_dict(orient="records")
    for i,village in enumerate(vilalge_dict):
        insert_to_table(table_name="villages", value_dict={"village_id":village["village_code"], "village_name":village["village"],\
             "taluka": village["taluka"], "taluka_code": village["taluka_code"], "district_id": village['district_code'], 'division':village['division']},\
                num=i, total_num=len(vilalge_dict))
    print("Villages successfully inserted")


def insert_to_table(table_name, value_dict, num, total_num):
    """
    Insert the value into the database and prints the notifications
    """
    inserted = db_opertation.fill_data(table_name=table_name, values=value_dict)
    if inserted:
        print(f"Row {num+1}/{total_num} inserted to {table_name}")
    else:
        print("Some error occured!")
        exit() #force fully exit from the process
        

# database operations
db_opertation = DatabaseOperations()
db_opertation.connect_db()

db_opertation.create_tables()

fill_division()
fill_district()
fill_village()

db_opertation.disconnect_db()
