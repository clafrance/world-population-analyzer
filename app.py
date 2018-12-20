import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


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



@app.route("/countries")
def countries():
    """Return a list of countries."""

    stmt = db.session.query(Country_Continent).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    country_list = list(df.iloc[:, 1])

    country_list.insert(0, "WORLD")

    return jsonify(country_list)


@app.route("/years_list")
def years_list():
    """Return a list of Years."""

    stmt = db.session.query(Total_Population_Both_Sexes).statement
    df_all = pd.read_sql_query(stmt, db.session.bind)
    return jsonify(list(df_all.columns[3:]))

@app.route("/population_all/<region>")
def population_all(region):
    """Return population for both  sex for given  region selection."""
    stmt = db.session.query(Total_Population_Both_Sexes).filter(Total_Population_Both_Sexes.region_subregion_country_area == region).statement
    df_all = pd.read_sql_query(stmt, db.session.bind)
    df_all = df_all.set_index("region_subregion_country_area", drop = True)
    df_all.drop(columns = ['ID','country_code'],inplace=True)

    return jsonify(df_all.T.to_dict('list'))

@app.route("/population_male/<region>")
def population_male(region):
    """Return population for both  sex for given  region selection."""
    stmt = db.session.query(Total_Population_Male).filter(Total_Population_Male.region_subregion_country_area == region).statement
    df_all = pd.read_sql_query(stmt, db.session.bind)
    df_all = df_all.set_index("region_subregion_country_area", drop = True)
    df_all.drop(columns = ['ID','country_code'],inplace=True)

    return jsonify(df_all.T.to_dict('list')) 

@app.route("/population_female/<region>")
def population_female(region):
    """Return population for both  sex for given  region selection."""
    stmt = db.session.query(Total_Population_Female).filter(Total_Population_Female.region_subregion_country_area == region).statement
    df_all = pd.read_sql_query(stmt, db.session.bind)
    df_all = df_all.set_index("region_subregion_country_area", drop = True)
    df_all.drop(columns = ['ID','country_code'],inplace=True)

    return jsonify(df_all.T.to_dict('list'))       

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
