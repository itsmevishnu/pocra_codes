# pocra_assingment
This is a simple python code for downloding csv files from http://115.124.110.196:8080/epeek/
- Reguired packages and software
  - Pandas `pip install pandas`
  - Selenium `pip install selenium`
  - Beutifulsoup `pip install beautifulsoup4`
  - Requests
  - Firefox web browser
  - Python version: 3
  - OS: Linux
- Command : `python3 collect_data.py उन्हाळी amravati - -`
- Syntax : `python collect_data.py<space>season_name<space>division_name<space>district_name<space>village`
- '-' for all villages or district
- Files will be saved in data folder

## Fetch the value of the website and insert into Database.
The codes will create necessary tables to store division, district, block and village level information, which will not change frequently. These tables are called meta data tables for the actual dataset. 
Actual dataset contains the information about each farmer of the selected village and having account number, area of the land, crop details, season etc. 

The data fetching engine currently developed has two parts. One is for fetching and storing the metadata values.This is a one time process. The user dont need to follow the steps for metadata related computation if it already completed. The second one is filling the village level information based on district selected. The instruction for both steps are given below.
#### For initilaizing the meta database tables
1. To create database, move to `collect_village_data` folder
2. Run `meta_data_fill.py`
### For adding farmers' information to database tables
1. Run `pocra_data_fill.py`
2. Enter the district code and season code
**Initializing meta table is required for first time only**
