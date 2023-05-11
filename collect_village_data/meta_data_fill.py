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
    divisions = [(divison,) for divison in divisions]
    #available tables - divisions, districts, talukas, village
    # #inserting divsion values
    insert_to_table(table_name='divisions', values=divisions)

def fill_district():
    """
    Read the information from the file and insert into district database
    This is a helper function to read and modify the from file
    """
    districts = data_set[['district_code', 'district']].drop_duplicates()
    dist_data = districts.to_dict(orient="records")
    districts = [(x['district_code'],x['district'])for x in dist_data]
    insert_to_table(table_name="districts", values=districts)
    

def fill_taluka():
    """
    This is a helper function to read and modify the from file
    Read taluka information and store to the database
    """
    talukas =  data_set[['taluka', 'taluka_code', 'district_code']].drop_duplicates()
    taluka_dict = talukas.to_dict(orient='records')
    talukas = [(x["district_code"], x['taluka_code'], x['taluka']) for x in taluka_dict]
    insert_to_table(table_name="talukas", values=talukas)

def fill_village():
    """
    This is a helper function to read and modify the file and store all the village values.
    """
    villages = data_set[['village', 'village_code', 'district_code', "taluka", "taluka_code", "division"]]
    vilalge_dict = villages.to_dict(orient="records")
    villages = [(x['village_code'], x['village'], x['taluka'], x['district_code'], x['taluka_code'], x['division'] ) for x in vilalge_dict]
    insert_to_table(table_name="villages", values=villages)
    


def insert_to_table(table_name, values):
    """
    Insert the value into the database and prints the notifications
    """
    inserted = db_opertation.fill_data(table_name=table_name, values=values)
    if inserted:
        print(f"Data inserted into table '{table_name}' successfully")
    else:
        print("Some error occured!")
        exit() #force fully exit from the process
        

# database operations
db_opertation = DatabaseOperations()
db_opertation.connect_db()

db_opertation.create_tables()

fill_division()
fill_district()
fill_taluka()
fill_village()

db_opertation.disconnect_db()
