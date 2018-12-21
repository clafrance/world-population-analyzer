import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

import load_data



app = Flask(__name__)

# # Run the load_to_sqlite() function in load_data.py
load_data.load_to_sqlite()



# Database Setup

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/world_population.sqlite"
db = SQLAlchemy(app)


# reflect an the world+population database into a model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)


# Create a object for each table
Total_Population_Both_Sexes = Base.classes.total_population_both_sexes
Total_Population_Female = Base.classes.total_population_female
Total_Population_Male = Base.classes.total_population_male
Sex_Ratio_Of_Total_Population = Base.classes.sex_ratio_of_total_population
Population_Growth_Rate = Base.classes.population_growth_rate
Population_By_Age_Male = Base.classes.population_by_age_male
Population_By_Age_Female = Base.classes.population_by_age_female
Population_By_Age_Both_Sexes = Base.classes.population_by_age_both_sexes
Country_Continent = Base.classes.country_continent
  

# db.session.query(Total_Population_Both_Sexes)


@app.route("/")
def index():
    """Return the homepage."""

    return render_template("index.html")



@app.route("/countries_old")
def countries_old():
    """Return a list of countries."""

    stmt = db.session.query(Country_Continent).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    country_list = list(df.iloc[:, 1])

    country_list.insert(0, "WORLD")

    return jsonify(country_list)

@app.route("/countries")
def countries():
    """Return a list of countries."""

    stmt = db.session.query(Country_Continent).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    country_list = list(df.iloc[:, 1])

    country_list.insert(0, "WORLD")
    years_bin = list(range(1950,2020,5))

    dictA= {'countries':country_list,
            
             'years_bin' :years_bin
    }
    return jsonify(dictA)



@app.route("/years_list")
def years_list():
    """Return a list of Years."""

    stmt = db.session.query(Total_Population_Both_Sexes).statement
    df_all = pd.read_sql_query(stmt, db.session.bind)
    return jsonify(list(df_all.columns[3:]))

@app.route("/populations_all_world")
def populations():
    """Return population for both  sex for given  region selection."""
    stmt = db.session.query(Total_Population_Both_Sexes).filter(Total_Population_Both_Sexes.region_subregion_country_area == "WORLD").statement
    df_all = pd.read_sql_query(stmt, db.session.bind)
    df_all.drop(columns = ["region_subregion_country_area",'ID','country_code'],inplace=True)
    df_new = df_all.transpose()
    df_new.reset_index(level=0, inplace=True)
    df_new.columns = ["Year","Population"]
    return jsonify(df_new.to_dict(orient="records"))    

@app.route("/population_all/<country>")
def population_all(country):
    """Return population for both  sex for given  region selection."""
    #All Population
    stmt = db.session.query(Total_Population_Both_Sexes).filter(Total_Population_Both_Sexes.region_subregion_country_area == country).statement
    df_a = pd.read_sql_query(stmt, db.session.bind)
    df_a.drop(columns = ["region_subregion_country_area",'ID','country_code'],inplace=True)
    df_all= df_a.transpose()
    df_all.reset_index(level=0, inplace=True)
    df_all.columns = ["Year","A_Population"]
    
    #Female Population
    stmt = db.session.query(Total_Population_Female).filter(Total_Population_Female.region_subregion_country_area == country).statement
    df_f = pd.read_sql_query(stmt, db.session.bind)
    df_f.drop(columns = ["region_subregion_country_area",'ID','country_code'],inplace=True)
    df_f2 =df_f.transpose()
    df_f2.reset_index(level=0, inplace=True)
    df_f2.columns = ["Year","f_Population"]
    
    #male Population
    stmt = db.session.query(Total_Population_Male).filter(Total_Population_Male.region_subregion_country_area == country).statement
    df_m = pd.read_sql_query(stmt, db.session.bind)
    df_m.drop(columns = ["region_subregion_country_area",'ID','country_code'],inplace=True)
    df_m2 =df_m.transpose()
    df_m2.reset_index(level=0, inplace=True)
    df_m2.columns = ["Year","m_Population"]
    
    #merge together

    df_all =df_all.merge(df_m2, on='Year')
    df_all =df_all.merge(df_f2, on='Year')

    return jsonify(df_all.to_dict(orient="records"))

@app.route("/age_group/<country>/<year>")
def age_group(country,year):
    """Return population for both  sex for given  region selection."""
    #All Population
    stmt = db.session.query(Population_By_Age_Both_Sexes).filter(Population_By_Age_Both_Sexes.reference_date == year)\
        .filter(Population_By_Age_Both_Sexes.region_subregion_country_area == country).statement
    df_a = pd.read_sql_query(stmt, db.session.bind)
    df_a.drop(columns = ["region_subregion_country_area",'ID','country_code','reference_date'],inplace=True)
    df_a2 =df_a.transpose()
    df_a2.reset_index(level=0, inplace=True)
    df_a2.columns = ["Age_Group","A_Population"]
    
    
    #Female Population
    stmt = db.session.query(Population_By_Age_Female).filter(Population_By_Age_Female.reference_date == year)\
        .filter(Population_By_Age_Female.region_subregion_country_area == country).statement
    df_f = pd.read_sql_query(stmt, db.session.bind)
    df_f.drop(columns = ["region_subregion_country_area",'ID','country_code','reference_date'],inplace=True)
    df_f2 =df_f.transpose()
    df_f2.reset_index(level=0, inplace=True)
    df_f2.columns = ["Age_Group","F_Population"]
    
    #male Population
    stmt = db.session.query(Population_By_Age_Male).filter(Population_By_Age_Male.reference_date == year)\
        .filter(Population_By_Age_Male.region_subregion_country_area == country).statement
    df_m = pd.read_sql_query(stmt, db.session.bind)
    df_m.drop(columns = ["region_subregion_country_area",'ID','country_code','reference_date'],inplace=True)
    df_m2 =df_m.transpose()
    df_m2.reset_index(level=0, inplace=True)
    df_m2.columns = ["Age_Group","M_Population"]
    
    #merge together

    df_bin =df_a2.merge(df_m2, on='Age_Group')
    df_bin =df_bin.merge(df_f2, on='Age_Group')
   
    return jsonify(df_bin.to_dict(orient="records"))  
    
@app.route("/country_info/<country>")
def country_info(country):
    """Return the country information for a given country"""

    sel = [
        Country_Continent.country,
        Country_Continent.code,
        Country_Continent.country_code,
        Country_Continent.capital,
        Country_Continent.latitude,
        Country_Continent.longitude,
        Country_Continent.continent
    ]

    results = db.session.query(*sel).filter(Country_Continent.country == country).first()

    country_info = {}
    for result in results:
        country_info["Code"] = results[1]
        country_info["Capital"] = results[3]
        country_info["Latitude"] = results[4]
        country_info["Longitude"] = results[5]
        country_info["Continent"] = results[6]

    # print(results)
    return jsonify(country_info)


if __name__ == "__main__":
    app.run()
