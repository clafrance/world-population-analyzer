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

# Run the load_to_sqlite() function in load_data.py
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
  

db.session.query(Total_Population_Both_Sexes)


@app.route("/")
def index():
    """Return the homepage."""
    
    return render_template("index.html")






@app.route("/country_info/<country>")
def country_info(country):
    """Return the country information for a given country"""


# @app.route("/names")
# def names():
#     """Return a list of sample names."""

#     # Use Pandas to perform the sql query
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Return a list of the column names (sample names)
#     return jsonify(list(df.columns)[2:])


# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""
#     sel = [
#         Samples_Metadata.sample,
#         Samples_Metadata.ETHNICITY,
#         Samples_Metadata.GENDER,
#         Samples_Metadata.AGE,
#         Samples_Metadata.LOCATION,
#         Samples_Metadata.BBTYPE,
#         Samples_Metadata.WFREQ,
#     ]

#     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

#     # Create a dictionary entry for each row of metadata information
#     sample_metadata = {}
#     for result in results:
#         sample_metadata["sample"] = result[0]
#         sample_metadata["ETHNICITY"] = result[1]
#         sample_metadata["GENDER"] = result[2]
#         sample_metadata["AGE"] = result[3]
#         sample_metadata["LOCATION"] = result[4]
#         sample_metadata["BBTYPE"] = result[5]
#         sample_metadata["WFREQ"] = result[6]

#     print(sample_metadata)
#     return jsonify(sample_metadata)


# @app.route("/samples/<sample>")
# def samples(sample):
#     """Return `otu_ids`, `otu_labels`,and `sample_values`."""
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Filter the data based on the sample number and
#     # only keep rows with values above 1
#     sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
#     # Format the data to send as json
#     data = {
#         "otu_ids": sample_data.otu_id.values.tolist(),
#         "sample_values": sample_data[sample].values.tolist(),
#         "otu_labels": sample_data.otu_label.tolist(),
#     }
#     return jsonify(data)


if __name__ == "__main__":
    app.run()
