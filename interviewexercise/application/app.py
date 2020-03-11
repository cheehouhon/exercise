from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import logging
import json

## MYSQL connection
import mysql.connector as mysql

# Create database
db = mysql.connect(
        host = "tiiv88mn8jz27i.cvjptpuqa6ut.us-east-1.rds.amazonaws.com",
        user = "timesheet",
        password = "timesheet"
    )
dbcur = db.cursor()
dbcur.execute("CREATE DATABASE IF NOT EXISTS timesheet")

## Create Table if it doesnt exist

try: 
    db = mysql.connect(
        host = "tiiv88mn8jz27i.cvjptpuqa6ut.us-east-1.rds.amazonaws.com",
        user = "timesheet",
        password = "timesheet",
        database = "timesheet"
    )
    dbcur = db.cursor()
    dbcur.execute("SHOW TABLES LIKE 'timesheet'")
    output=[]
    for x in dbcur:
        output.append(x)

    if not output:
        logging.warning("Table timesheet not configured: CREATING")
        dbcur.execute("CREATE TABLE timesheet (id INT AUTO_INCREMENT PRIMARY KEY, fname VARCHAR(255) NOT NULL, lname VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, hrsmon VARCHAR(255) NOT NULL, hrstue VARCHAR(255) NOT NULL, hrswed VARCHAR(255) NOT NULL, hrsthu VARCHAR(255) NOT NULL, hrsfri VARCHAR(255) NOT NULL, hrsextra VARCHAR(255) NOT NULL, date DATE NOT NULL)")            
        db.commit()

except Exception as e:
    print("Connection Error: {}".format(e))

app = Flask(__name__)

## Add timesheet to database
def add_timesheet(timesheet):
    db = mysql.connect(
        host = "tiiv88mn8jz27i.cvjptpuqa6ut.us-east-1.rds.amazonaws.com",
        user = "timesheet",
        password = "timesheet",
        database = "timesheet"
    )
    dbcur = db.cursor()
    sql = "INSERT INTO timesheet (email, fname, lname, hrsmon, hrstue, hrswed, hrsthu, hrsfri, hrsextra, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (
        timesheet["email"],
        timesheet["f-name"],
        timesheet["l-name"],
        timesheet["hrs-mon"],
        timesheet["hrs-tue"],
        timesheet["hrs-wed"],
        timesheet["hrs-thu"],
        timesheet["hrs-fri"],
        timesheet["hrs-extra"],
        datetime.strptime(timesheet["date"], '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
    )
    dbcur.execute(sql, val)
    db.commit()

## Get timesheets from database
def list_timesheet():
    db = mysql.connect(
        host = "tiiv88mn8jz27i.cvjptpuqa6ut.us-east-1.rds.amazonaws.com",
        user = "timesheet",
        password = "timesheet",
        database = "timesheet"
    )
    dbcur = db.cursor()
    dbcur.execute("SELECT * FROM timesheet")
    output=[]
    for x in dbcur:
        output.append(x)
    return output


## Routes
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form:
            try:
                add_timesheet(request.form)
            except:
                print(Exception)
            return redirect(url_for('history'))
    else:
        return render_template("index.html")

@app.route("/history", methods=['GET'])
def history():
    return render_template("history.html", timesheets=list_timesheet())

if __name__ == '__main__':

    # Start Flask
    app.run()
    db.close()
