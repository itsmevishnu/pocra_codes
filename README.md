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
#### For initilaizing the meta database tables
1. To create database, move to `collect_village_data` folder
2. Run `meta_data_fill.py`
### For adding farmers' information to database tables
1. Run `pocra_data_fill.py`
2. Enter the district code and season code
**Initializing meta table is required for first time only**