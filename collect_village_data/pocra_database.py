#import necessary packages
import psycopg2

class DatabaseOperations:

    # Dtabase informations
    database = "pocra_db"
    username = "postgres"
    password = "postgres"
    host = "localhost"

    db_connection = None
    db_cursor = None

    def connect_db(self):
        """
        Establish the database connection
        """
        try:
            self.db_connection = psycopg2.connect(host=self.host, database=self.database, user=self.username, password=self.password)
            if(self.db_connection):
                print("Successfully connected to the database")
                self.db_cursor = self.db_connection.cursor()
        except Exception as e:
            raise Exception(f"Error occured: {e}")


    def disconnect_db(self):
        """
        Disconnect the database
        """
        self.db_connection.close()
        print("Successfully disconnected from the database")


    def create_tables(self):
        """
        Creates necessary database tables. 
        Major tables are divisions, districts, talukas, villages, account holder and status
        """

        tables = [
            """
            CREATE TABLE IF NOT EXISTS divisions(
                id INTEGER GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(100) NOT NULL UNIQUE,
                PRIMARY KEY(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS districts(
                district_id INTEGER,
                name VARCHAR(100) NOT NULL UNIQUE,
                PRIMARY KEY(district_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS talukas(
                id INTEGER GENERATED ALWAYS AS IDENTITY,
                district INTEGER,
                name VARCHAR(100) NOT NULL UNIQUE,
                PRIMARY KEY(id),
                FOREIGN KEY(district) REFERENCES districts(district_id)
            )
            """, 
            """
            CREATE TABLE IF NOT EXISTS villages(
                id INTEGER GENERATED ALWAYS AS IDENTITY,
                village_id VARCHAR(100) NOT NULL,
                village_name VARCHAR(100) NOT NULL,
                taluka VARCHAR(100) NOT NULL,
                district INTEGER,
                taluka_code INTEGER,
                division VARCHAR(100),
                PRIMARY KEY(id),
                FOREIGN KEY(district) REFERENCES districts(district_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS account_holders (
                id INTEGER GENERATED ALWAYS AS IDENTITY,
                name VARCHAR(100) NOT NULL,
                account_number VARCHAR(100) NOT NULL,
                group_number VARCHAR(100) NOT NULL,
                crop_inspection_date TIMESTAMP,
                crop_name VARCHAR(100) NOT NULL,
                cropt_type VARCHAR(100) NOT NULL,
                area VARCHAR(100) NOT NULL,
                crop_season VARCHAR(100) NOT NULL,
                village INTEGER,
                PRIMARY KEY(id),
                FOREIGN KEY(village) REFERENCES villages(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS status (
                id INTEGER GENERATED ALWAYS AS IDENTITY,
                district INTEGER,
                completed_at TIMESTAMP,
                PRIMARY KEY(id),
                FOREIGN KEY(district) REFERENCES districts(district_id)
            )
            """
        ]
        for i, table in enumerate(tables):
            try:
                self.db_cursor.execute(table)
                self.db_connection.commit()
                print(f"Table {i+1} created/{len(tables)}")
            except Exception as e:
                self.db_connection.rollback()
                print(f"Error occured during creation of tables {e}")



        
    def fill_data(self, table_name, values):
        """
        Insert the values into curresponding tables.
        """
        query = ''
        if table_name == 'divisions':
            query =  f"INSERT INTO divisions(name) VALUES('{values['name']}')"
        if table_name == 'districts':
            query =  f"INSERT INTO districts(district_id, name) VALUES({values['district_id']},'{values['name']}')"
        if table_name == 'talukas':
            query =  f"INSERT INTO talukas( district, name) VALUES({values['district_id']},'{values['name']}')"
        if table_name == 'villages':
            query =  f"INSERT INTO villages(village_id, village_name, taluka, district, taluka_code, division  ) VALUES('{values['village_id']}', '{values['village_name']}',\
                 '{values['taluka']}', {values['district_id']}, {values['taluka_code']}, '{values['division']}')" 
        if table_name == 'account_holders':
            query =  f"INSERT INTO account_holders(name, account_number, group_number, crop_inspection_date, crop_name, cropt_type, area, crop_season, village   ) VALUES\
                ('{values['name']}', '{values['account_number']}', '{values['group_number']}', '{values['crop_inspection_date']}', '{values['crop_name']}', \
                '{values['crop_type']}', '{values['area']}', '{values['season']}', {values['village']})"
        
        try:
            self.db_cursor.execute(query)
            self.db_connection.commit()
            return True
        except Exception as e:
            self.db_connection.rollback()
            print(f"Error occured while inserting into {table_name}. \n Error details: {e}")
            return False

    def fetch_data(self, query):
        """
        Execute query and fetch the data
        """
        try:
            self.db_cursor.execute(query)
            result_set = self.db_cursor.fetchall()
            return result_set
        except Exception as e:
            print(f"There is some error occured. Error: {e}")
            return