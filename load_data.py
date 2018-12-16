import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect

import os


data_files = [
         'data/TOTAL_POPULATION_BOTH_SEXES.csv', 
         'data/TOTAL_POPULATION_FEMALE.csv',
         'data/TOTAL_POPULATION_MALE.csv',
         'data/SEX_RATIO_OF_TOTAL_POPULATION.csv',
         'data/POPULATION_GROWTH_RATE.csv',
         'data/POPULATION_BY_AGE_MALE.csv',
         'data/POPULATION_BY_AGE_FEMALE.csv',
         'data/POPULATION_BY_AGE_BOTH_SEXES.csv']  

tables = [
      'total_population_both_sexs',
      'total_population_female',
      'total_population_male',
      'sex_ratio_of_total_population',
      'population_growth_rate',
      'population_by_age_male',
      'population_by_age_female',
      'population_by_age_both_sexes']


db_file = 'db/world_population.sqlite'
db_url = 'sqlite:///./db/world_population.sqlite'

# Remove existing sqlite db file
if not os.path.exists(db_file):
    engine = create_engine(db_url)
    print(f"{db_file}, file is created successfully")
else:
    os.remove(db_file)
    engine = create_engine(db_url)
    print(f"{db_file}, deleted existing file, create a new file")


# 1. read the csv files into Panda dataframe
# 2. Remove the space from the data in dataframes, and convert "…" to "0" if needed
# 3. then create tables in sqlite from the dataframes
for i in range(0, 8):

    # read the csv files into Panda dataframe
    df = pd.read_csv(data_files[i])

    # Create index for the df, may not need this 
    df.insert(0, 'ID', range(0, len(df)))
    df.set_index('ID', inplace=True)
    
    if i not in [3,4]: # data in these two files do not need to be cleaned
        if i in [0, 1, 2]:
            column_range = range(2, len(df.columns)) # Start with 3rd column
        else:
            column_range = range(3, len(df.columns)) # Start with 4th column

        # remove space, replace "…" with "0", then convert to integer
        for j in column_range:
            df.iloc[:, j] = [int(x.replace(" ", "").replace("…", "0")) for x in df.iloc[:, j]]
    
    # Create the table
    table = tables[i]
    try: 
        df.to_sql(table, engine)
        print(f"{table}, has been created successfully")
    except:
        print(f"{table}, can not be created")


# # Query the data from sqlite table population_by_age_both_sexes.sqlite
# engine = create_engine("sqlite:///./db/world_population.sqlite")
# inspector = inspect(engine)
# inspector.get_table_names()
# inspector.get_columns('population_by_age_both_sexes')
# engine.execute("SELECT * FROM population_by_age_both_sexes").fetchall()