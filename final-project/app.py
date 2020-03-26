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

x_axis = world_total_and_death_and_new_cases_new_death_cases['date'].to_numpy()
y_axis = world_total_and_death_and_new_cases_new_death_cases['total_cases'].to_numpy()
plt.figure(figsize=(15,8))
plt.plot(x_axis, y_axis, marker='o')
plt.xticks(rotation=90, horizontalalignment='center', fontweight='light', fontsize='large')
plt.title('Total COVID-19 Cases per Day', fontweight='bold', fontsize='x-large')
plt.ylabel('Total Cases', fontweight='bold', fontsize='x-large')
plt.savefig('static/images/total-cases-covid-19.png')

x_axis = world_total_and_death_and_new_cases_new_death_cases['date'].to_numpy()
y_axis = world_total_and_death_and_new_cases_new_death_cases['total_deaths'].to_numpy()
plt.figure(figsize=(15,8))
plt.bar(x_axis, y_axis, alpha= 0.25)
plt.xticks(rotation=90, horizontalalignment='center', fontweight='light', fontsize='large')
plt.title('Total Deaths COVID-19 Cases per Day', fontweight='bold', fontsize='x-large')
plt.ylabel('Total Deaths', fontweight='bold', fontsize='x-large')
plt.savefig('static/images/total-deaths-covid-19.png')

x_axis = world_total_and_death_and_new_cases_new_death_cases['date'].to_numpy()
y_axis = world_total_and_death_and_new_cases_new_death_cases['new_cases'].to_numpy()
plt.figure(figsize=(15,8))
plt.plot(x_axis, y_axis, marker='o')
plt.xticks(rotation=90, horizontalalignment='center', fontweight='light', fontsize='large')
plt.title('New Cases COVID-19 Cases per Day', fontweight='bold', fontsize='x-large')
plt.ylabel('New Cases', fontweight='bold', fontsize='x-large')
plt.savefig('static/images/new-cases-covid-19.png')

x_axis = world_total_and_death_and_new_cases_new_death_cases['date'].to_numpy()
y_axis = world_total_and_death_and_new_cases_new_death_cases['new_deaths'].to_numpy()
plt.figure(figsize=(15,8))
plt.plot(x_axis, y_axis, marker='o')
plt.xticks(rotation=90, horizontalalignment='center', fontweight='light', fontsize='large')
plt.title('New Deaths COVID-19 Cases per Day', fontweight='bold', fontsize='x-large')
plt.ylabel('New Deaths', fontweight='bold', fontsize='x-large')
plt.savefig('static/images/new-deaths-covid-19.png')

full_data = 'https://covid.ourworldindata.org/data/full_data.csv'
full_data = pd.read_csv(full_data)
full_data.fillna(0)
full_data.to_csv('data/full_data.csv')

df_full_data = pd.read_csv('data/full_data.csv')
df_full_data = df_full_data[['date', 'location', 'new_cases', 'new_deaths', 'total_cases', 'total_deaths']]
df_full_data.to_sql(name='full_data', con=engine, if_exists='replace', index=False)

tsx = pd.read_csv('data/GSPTSE.csv')
dji = pd.read_csv('data/DJI.csv')

tsx = tsx[['Date', 'Close']]
tsx = tsx.rename(columns={"Close":"tsx_Closing"})

dji = dji[['Date', 'Close']]
dji = dji.rename(columns={"Close":"dji_Closing"})

merge_close = tsx.merge(dji, how="inner", on="Date")

x_axis = merge_close['Date'].to_numpy()
tsx_closing = merge_close['tsx_Closing'].to_numpy()
dji_closing = merge_close['dji_Closing'].to_numpy()
plt.figure(figsize=(15,8))
plt.xticks(rotation=90, horizontalalignment='center', fontweight='light', fontsize='large')
plt.title('DJI and TSX Closing after COVID pendemic', fontweight='bold', fontsize='x-large')
tsx_handle, = plt.plot(x_axis, tsx_closing, marker='o', color='blue', label='TSX')
dji_handle, = plt.plot(x_axis, dji_closing, marker='o', color='red', label='DJI')
plt.savefig('static/images/tsx-dji-closing.png')
# current_date = date.today()
# formatted_date = current_date.strftime("%Y-%m-%d")
# covid_data_url = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-"+formatted_date+".xlsx"

# df_xls_data = pd.read_excel(covid_data_url)
# df_xls_data.to_excel('data/COVID-19-geographic-disbtribution-worldwide.xlsx', index=False)

# xls_to_csv = df_xls_data[['DateRep', 'Countries and territories', 'Cases', 'Deaths']]
# xls_to_csv.to_csv('data/country_wide_data.csv', index=False)
# world_data_by_country = pd.read_csv('data/country_wide_data.csv')

# total_cases_by_country = world_data_by_country[['Countries and territories','Cases']].groupby('Countries and territories').sum()

# total_case_chart = total_cases_by_country.sort_values(by='Cases', ascending=False).head(10).plot(kind='bar', alpha=0.25)
# total_case_chart.set_xlabel("Country", fontweight='bold', fontsize='x-large')
# total_case_chart.set_ylabel("Total # of Cases", fontweight='bold', fontsize='x-large')

# plt.title('Top 10 Countries with Total COVID-19 Cases', fontweight='bold', fontsize='x-large')
# plt.show()
# plt.tight_layout()
# plt.savefig('static/images/top10-countries-covid-19-cases.png')

# total_deaths_by_country = world_data_by_country[['Countries and territories','Deaths']].groupby('Countries and territories').sum()

# total_death_chart = total_deaths_by_country.sort_values(by='Deaths', ascending=False).head(10).plot(kind='bar', alpha=0.25)
# total_death_chart.set_xlabel("Country", fontweight='bold', fontsize='x-large')
# total_death_chart.set_ylabel("Total # of Deaths", fontweight='bold', fontsize='x-large')

# plt.title('Top 10 Countries with Total COVID-19 Deaths', fontweight='bold', fontsize='x-large')
# plt.show()
# plt.tight_layout()
# plt.savefig('static/images/top10-countries-covid-19-deaths.png')

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
    app.run()