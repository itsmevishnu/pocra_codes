#import necessary packages
import pandas as pd
import requests

from bs4 import BeautifulSoup
from pocra_database import DatabaseOperations
from pocra_datamine import get_data_for_db

class PocraDataFill:
    db_opertation = None

    def __init__(self):
       self.db_opertation = DatabaseOperations()

    def get_urls(self, id, season):
        """
        Find out all the village based information from the database 
        Generate url array for fetching the values
        """
        base_url = "http://115.124.110.196:8080/epeek/rptViewPeekPahani.jsp?"
        url_list = []
        season_code = ''
        if season == 1:
            season_code = 'खरीप' 
        elif  season == 2:
            season_code = 'रब्बी' 
        elif season == 3:
            season_code = 'उन्हाळी'
        
        self.db_opertation.connect_db()
        try:
            query = f"SELECT * FROM villages WHERE district={id}"
            meta_data = self.db_opertation.fetch_data(query)

        except Exception as e:
            print(f"Some error occured. Error{e}")

        finally:
            self.db_opertation.disconnect_db()

        print('Creating URLs for the district...')

        for item in meta_data:
            data = {}
            url = f"ccode={item[1]}&blk={item[5]}&dist={item[4]}&div={item[6]}&season={season_code}"
            data['url'] = base_url+url
            data['village_code'] = item[0]
            data['season'] = season_code
            url_list.append(data)
        
        return url_list
    
    def insert_values(self, urls):
        self.db_opertation.connect_db()
        try:
            for i, url in enumerate(urls):
                print(f"Collectiong information of village {i+1}/{len(urls)} and inserting into database")
                data_set = get_data_for_db(url)
                for num, values in enumerate(data_set):
                    print(f"Inserting account holder {num+1} of village {i+1}/{len(urls)} ")
                    self.db_opertation.fill_data('account_holders', values)
        except Exception as e:  
            print(f"There are some error occured. Error is {e}")
        finally:
            self.db_opertation.disconnect_db()

if __name__ == '__main__':
    
    data_fill = PocraDataFill()

    district_code = int(input("Enter the district code\n"))
    season = int(input("Select the season\n1.Garip\n2.Rabi\n3.Summer\n"))
    urls = data_fill.get_urls(district_code, season)
    data_fill.insert_values(urls)
   
    
       
    