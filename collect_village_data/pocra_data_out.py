import psycopg2
import os

from pocra_database import DatabaseOperations


def create_file(district, season):
    """
    Map the seasons to Marati names
    Call the function to fetch the values
    """
    os.makedirs(f"output/{district}", exist_ok=True) #Create output folder with distcit code

    db_opertation = DatabaseOperations()

    if season == 1:
        season_mr = 'खरीप'
        season_en = 'Kharif'
    elif season == 2:
        season_mr = "रब्बी"
        season_en = 'Rabi'
    else:
        season_mr = "ग्रीष्म"
    
    file_name = f"output/{district}/data_{district}_{season_en}.csv"
        
    db_opertation.fetch_village_values(district, season_mr, file_name)


def main():
    district = int(input("Enter the district code\n"))
    season = int(input("Select the season\n1.Garip\n2.Rabi\n3.Summer\n"))
    result = create_file(district, season)

if __name__ == "__main__":
    main()
