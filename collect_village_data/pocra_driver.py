import pocra_datamine as pocra
import pandas as pd

base_url = "http://115.124.110.196:8080/epeek/rptViewKhateNew.jsp"

def generate_info(disrtict_code):
    """ Fetch the data and create the required url for collecting data from the portal"""
    village_config_data = pd.read_csv('config/all_village_data.csv')
    required_villages = village_config_data[village_config_data['district_code']==disrtict_code]
    required_info = required_villages.filter(items=["district", "taluka", "village"])
    required_info['url'] = required_villages.apply(lambda row: f"{base_url}?season=खरीप&ccode={row['village_code']}&blk={row['taluka_code']}&dist={row['district_code']}&div={row['division']}", axis=1 )
    return required_info


def start_data_collection():
    district = int(input("Enter the disrict code, Eg:7 for Amravati\n"))

    info = generate_info(district)

    for item in info.itertuples():
        print(f"Fetching the information of {item.Index+1} village/{len(info)}")
        headers, data_list = pocra.get_data(item.url)

        print(f"Start writing file..")
        pocra.generate_csv(data_list, headers, district=item.district, taluka=item.taluka, village=item.village)
        print(f"Created file {item.Index+1} village/{len(info)}")

def main():
    start_data_collection()


if __name__ =='__main__':
    main()