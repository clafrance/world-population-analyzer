import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect

import os

def load_from_csv_to_sqlite():

    data_files = [
             'data/TOTAL_POPULATION_BOTH_SEXES.csv', 
             'data/TOTAL_POPULATION_FEMALE.csv',
             'data/TOTAL_POPULATION_MALE.csv',
             'data/SEX_RATIO_OF_TOTAL_POPULATION.csv',
             'data/POPULATION_GROWTH_RATE.csv',
             'data/POPULATION_BY_AGE_MALE.csv',
             'data/POPULATION_BY_AGE_FEMALE.csv',
             'data/POPULATION_BY_AGE_BOTH_SEXES.csv']  

    db_files = [
          'db/total_population_both_sexs.sqlite',
          'db/total_population_female.sqlite',
          'db/total_population_male.sqlite',
          'db/sex_ratio_of_total_population.sqlite',
          'db/population_growth_rate.sqlite',
          'db/population_by_age_male.sqlite',
          'db/population_by_age_female.sqlite',
          'db/population_by_age_both_sexes.sqlite']


    db_urls = [
          'sqlite:///./db/total_population_both_sexs.sqlite',
          'sqlite:///./db/total_population_female.sqlite',
          'sqlite:///./db/total_population_male.sqlite',
          'sqlite:///./db/sex_ratio_of_total_population.sqlite',
          'sqlite:///./db/population_growth_rate.sqlite',
          'sqlite:///./db/population_by_age_male.sqlite',
          'sqlite:///./db/population_by_age_female.sqlite',
          'sqlite:///./db/population_by_age_both_sexes.sqlite']

    tables = [
          'total_population_both_sexs',
          'total_population_female',
          'total_population_male',
          'sex_ratio_of_total_population',
          'population_growth_rate',
          'population_by_age_male',
          'population_by_age_female',
          'population_by_age_both_sexes']


    # 1. read the csv files into Panda dataframe
    # 2. Remove the space from the data in dataframes, and convert "…" to "0" if needed
    # 3. then create tables in sqlite from the dataframes

    for i in range(0, len(tables)):
        df = pd.read_csv(data_files[i])

        # Create index, may not need this 
        df.insert(0, 'ID', range(0, len(df)))
        df.set_index('ID', inplace=True)
        
        if i not in [3,4]:
            if i in [0, 1, 2]:
                column_range = range(2, len(df.columns))
            else:
                column_range = range(3, len(df.columns))

            for j in column_range:
                # remove space, replace "…" with "0", then convert to integer
                df.iloc[:, j] = [int(x.replace(" ", "").replace("…", "0")) for x in df.iloc[:, j]]
        
        db_url = db_urls[i]
        table = tables[i]
        db_file = db_files[i]


        # Only create the file if not exist
        if not os.path.exists(db_file):
            engine = create_engine(db_url)
            df.to_sql(table, engine)
            print(f"{db_file}, file is created successfully")
        else:
            print(f"{db_file}, file already exist")

        
        # # if what to drop and recreate, use these code
        # # Remove the files if exist
        # if os.path.exists(db_file):
        #     os.remove(db_file)
        
        # engine = create_engine(db_url)
        # df.to_sql(table, engine)

load_from_csv_to_sqlite()

# # Query the data from sqlite table population_by_age_both_sexes.sqlite
# engine = create_engine("sqlite:///./db/population_by_age_both_sexes.sqlite")
# inspector = inspect(engine)
# inspector.get_table_names()
# inspector.get_columns('population_by_age_both_sexes')
# engine.execute("SELECT * FROM population_by_age_both_sexes").fetchall()