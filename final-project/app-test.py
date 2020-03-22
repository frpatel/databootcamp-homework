import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, render_template, url_for, json, jsonify
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import pandas as pd
import numpy as np
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#CONNECT TO ENGINE  UNCOMENT THESE LATER
#engine=create_engine('mysql://root:root1234@localhost/NewNBAProject')
#Base=automap_base()
#Base.prepare(engine, reflect=True)
#updatedmastertable=Base.classes.df_final_df_cleaning
#session=Session(engine)
#STOP UNCOMMENTING

#Base2=automap_base()
#teamstats=Base.classes.updatedmastertable


import mysql.connector
   
@app.route("/")
def home():
    """Render Home Page."""
    print('home page')
    return render_template("index.html")

@app.route("/stats/<team>")
def plotstat(team):
    
   #  import mysql.connector

	mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="root123",
	database="NewNBAProject"
	)
	mycursor = mydb.cursor()

	mycursor.execute(f"SELECT Name, Pos, Weight, Year, Points_season, PER, Height FROM df_final_df_cleaning where Team='{team}' and Year='2019'")

	myresult = mycursor.fetchall()

	allplayers = []
	for result in myresult:
		players = {}
		players["Name"] = result[0]
		players["Pos"] = result[1]
		players["Weight"] = result[2]
		players["Year"] = result[3]      
		players["Points"]= result[4]
		players["PER"] = result[5]
		players["Height"] = result[6]
		allplayers.append(players)
	return jsonify(allplayers)

@app.route("/home")
def Main():
    """Render Home Page."""
    print('home page')
    return render_template("home.html")

# @app.route("/teamstats")
# def teamstats():
#     sel=[teamstats.Team,
   #    teamstats.Win-Loss-Percentage,
   #    teamstats.ESPN-BPI, 
   #    teamstats.Points-Per-Game,
   #    teamstats.Field-Goal-Percentage]
# results

   #  data_team_all=[]
   # for item in results:
   #    data={}
   #    data['Team']=item[0]
   #    data['Win-Loss-Percentage']=item[1]
   #    data['ESPN-BPI']=item[2]
   #    data['Points-Per-Game']=item[3]
   #    data['Field-Goal-Percentage']=item[4]
   #    data_all.append(data)

# 





# @app.route("/api/get_team")
def get_team():
   sel=[updatedmastertable.Name,
      updatedmastertable.Pos,
      updatedmastertable.Height,
      updatedmastertable.Weight, 
      updatedmastertable.Year,
      updatedmastertable.Team,
      updatedmastertable.Points_season,updatedmastertable.PER]
   results=session.query(*sel).filter(updatedmastertable.Year==2019).distinct()

   data_all=[]
   for item in results:
      data={}
      data['Name']=item[0]
      data['Pos']=item[1]
      data['Height']=item[2]
      data['Weight']=item[3]
      data['Year']=item[4]
      data['Team']=item[5]
      data['pointsSeason']=item[6]
      data['PER']=item[7]
      data_all.append(data)
      
   data_df=pd.DataFrame(data_all)  
   all_teams=data_df['Team'].unique()
   all_data_dict={}
   for team in all_teams:
      exec("df_{0} = data_df[data_df['Team']=='{1}']".format(team, team))
      exec("dict_{0}=df_{0}.to_dict(orient='list')".format(team, team))
      exec("all_data_dict['{0}']=dict_{0}".format(team, team))
   return jsonify (all_data_dict)


if __name__ == "__main__":
    app.run(debug=True, port=4999)

