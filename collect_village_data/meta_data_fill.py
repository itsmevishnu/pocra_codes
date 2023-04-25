#Imports necessary files

import pandas as pd
from pocra_database import DatabaseOperations

db_opertation = DatabaseOperations()
db_opertation.connect_db()

db_opertation.create_tables()

data_set = pd.read_csv('config/all_village_data.csv')

def fill_division():
    divisions = data_set["division"].unique()
    #available tables - divisions, districts, talukas, village
    # #inserting divsion values
    for division in divisions:
        db_opertation.fill_data(table_name='divisions', values={'name': division})
    print("Division successfully inserted")

def fill_district():
    districts = data_set[['district_code', 'district']].drop_duplicates()
    dist_data = districts.to_dict(orient="records")
    for district in dist_data:
        db_opertation.fill_data(table_name="districts", values={"district_id":district['district_code'], "name":district['district']} )
    

def fill_taluka():
    talukas =  data_set[['taluka', 'taluka_code', 'district_code']].drop_duplicates()
    taluka_dict = talukas.to_dict(orient='records')
    for taluka in taluka_dict:
        db_opertation.fill_data(table_name="talukas", values={"district_id":taluka['district_code'],"taluka_id":taluka['taluka_code'],"name":taluka['taluka']} )

def fill_village():
    villages = data_set[['village', 'village_code', 'district_code', "taluka"]]
    vilalge_dict = villages.to_dict(orient="records")
    for village in vilalge_dict:
        db_opertation.fill_data(table_name="villages", values={"village_id":village["village_code"], "village_name":village["village"],\
             "taluka": village["taluka"], "district_id": village['district_code'] })

# fill_division()
# fill_district()
fill_village()