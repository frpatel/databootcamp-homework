import os
import pandas as pd
import requests
import xlrd
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import psycopg2

connection_string = 'postgres:root123@localhost:5432/COVID'
engine = create_engine(f'postgresql://{connection_string}')

"""create table world_daily_data(
	date date,
	total_cases int,
	total_deaths int,
	new_cases int,
	new_deaths int
)"""

# Total Cases Reported by Date in whole world

# Downloading file and saving it into local folder
total_cases = 'https://covid.ourworldindata.org/data/ecdc/total_cases.csv'
total_cases = pd.read_csv(total_cases)
total_cases.to_csv('data/total_cases.csv')
# Reading csv file and fill non na values with 0
df_total_cases = pd.read_csv('data/total_cases.csv')
df_total_cases.fillna(0)
# Filtering date and world data
world_total_cases = df_total_cases[['date', 'World']]
# Renaming World column
world_total_cases = world_total_cases.rename(columns={"World":"total_cases"})

# Total Deaths Reported by Date in whole world
total_deaths = 'https://covid.ourworldindata.org/data/ecdc/total_deaths.csv'
total_deaths = pd.read_csv(total_deaths)
total_deaths.to_csv('data/total_deaths.csv')

df_total_deaths = pd.read_csv('data/total_deaths.csv')
df_total_deaths.fillna(0)

world_death_cases = df_total_deaths[['date', 'World']]
world_death_cases = world_death_cases.rename(columns={"World":"total_deaths"})

world_total_and_death = world_total_cases.merge(world_death_cases, how="inner", on="date")

# Total New Cases Reported by Date in whole world
new_cases = 'https://covid.ourworldindata.org/data/ecdc/new_cases.csv'
new_cases = pd.read_csv(new_cases)
new_cases.to_csv('data/new_cases.csv')

df_new_cases = pd.read_csv('data/new_cases.csv')
df_new_cases.fillna(0)

world_new_cases = df_new_cases[['date', 'World']]
world_new_cases = world_new_cases.rename(columns={"World":"new_cases"})

world_total_and_death_and_new_cases = world_total_and_death.merge(world_new_cases, how="inner", on="date")

# Total New Deaths Reported by Date in whole world
new_deaths = 'https://covid.ourworldindata.org/data/ecdc/new_deaths.csv'
new_deaths = pd.read_csv(new_deaths)
new_deaths.to_csv('data/new_deaths.csv')

df_new_deaths = pd.read_csv('data/new_deaths.csv')
df_new_deaths.fillna(0)

world_new_deaths = df_new_deaths[['date', 'World']]
world_new_deaths = world_new_deaths.rename(columns={"World":"new_deaths"})

world_total_and_death_and_new_cases_new_death_cases = world_total_and_death_and_new_cases.merge(world_new_deaths, how="inner", on="date")
world_total_and_death_and_new_cases_new_death_cases.to_sql(name='world_daily_data', con=engine, if_exists='replace', index=False)
world_total_and_death_and_new_cases_new_death_cases.to_csv('data/world_data.csv', index=False)


full_data = 'https://covid.ourworldindata.org/data/full_data.csv'
full_data = pd.read_csv(full_data)
full_data.fillna(0)
full_data.to_csv('data/full_data.csv')

df_full_data = pd.read_csv('data/full_data.csv')
df_full_data = df_full_data[['date', 'location', 'new_cases', 'new_deaths', 'total_cases', 'total_deaths']]
df_full_data.to_sql(name='full_data', con=engine, if_exists='replace', index=False)


app = Flask(__name__)
conn = psycopg2.connect(user="postgres", password="root123", host="localhost", port="5432", database="COVID")

@app.route("/")
def home():
    """Render Home Page."""
    print('home page')
    return render_template("index.html")

@app.route("/world_data")
def world_data():

    mycursor = conn.cursor()
    mycursor.execute("SELECT date, total_cases, total_deaths, new_cases, new_deaths FROM world_daily_data order by date desc")
    covid_data_by_date = mycursor.fetchall()

    all_data = []
    for row in covid_data_by_date:
        covid_data = {}
        covid_data["Date"] = row[0]
        covid_data["TotalCases"] = row[1]
        covid_data["TotalDeaths"] = row[2]
        covid_data["NewCases"] = row[3]
        covid_data["NewDeaths"] = row[4]
        all_data.append(covid_data)
    mycursor.close()
    return jsonify(all_data)



if __name__ == "__main__":
    app.run(debug=True)