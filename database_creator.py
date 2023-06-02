import json

import mysql.connector
from random import uniform, randint
from datetime import datetime, timedelta
def connect_database():
  mydb = mysql.connector.connect(
    host="localhost",
    user="project_dev",
    password="project_password",
    database="data"
  )

# Check if the connection is successful
  if mydb.is_connected():
    print("Connected to the MySQL server")
  else:
    print("Failed to connect to the MySQL server")
  return mydb

def create_database():
  mydb = mysql.connector.connect(
    host="localhost",
    user="project_dev",
    password="project_password"
  )
  # Create a cursor object
  mycursor = mydb.cursor()

  # Create the database if it does not exist
  mycursor.execute("CREATE DATABASE IF NOT EXISTS data")

  # Use the "data" database
  mycursor.execute("USE data")

  # Create the "data" table with the specified fields
  mycursor.execute("CREATE TABLE IF NOT EXISTS data (speed DOUBLE, distance DOUBLE, dtime DATETIME, longitude DOUBLE, latitude DOUBLE, trip INT)")

  # Commit the changes
  mydb.commit()

  print("Database created successfully")

def reset_database():
  # Connect to the MySQL server
  mydb = connect_database()

  # Create a cursor object
  mycursor = mydb.cursor()

  # Drop the "data" table if it exists
  mycursor.execute("DROP TABLE IF EXISTS data")

  # Create the "data" table with the specified fields
  mycursor.execute("CREATE TABLE IF NOT EXISTS data (speed DOUBLE, distance DOUBLE, dtime DATETIME, longitude DOUBLE, latitude DOUBLE, layer TEXT, name TEXT, trip INT)")

  # Commit the changes
  mydb.commit()

  print("Database reset successfully")

def fill_database():
  # Connect to the MySQL server and select the "data" database
  mydb = connect_database()

  # Create a cursor object
  mycursor = mydb.cursor()

  # Define the date range
  start_date = datetime(2023, 4, 21)
  end_date = datetime(2023, 6, 1)

  enschede_latitude = 52.219373
  enschede_longitude = 6.895129

  # Loop through each date in the range
  current_date = start_date
  while current_date <= end_date:
    # Generate 100 random entries for the current date
    for i in range(100):
      speed = randint(0, 30)
      distance = round(uniform(0, 100)+100*i, 2)
      time = current_date + timedelta(minutes=randint(0, 1439))
      longitude = round(enschede_longitude + uniform(-0.01, 0.01), 6)
      latitude = round(enschede_latitude + uniform(-0.01, 0.01), 6)
      trip = 0
      layer = "markers"
      name = "test"+ str(randint(0,10000))

      # Insert the entry into the "data" table
      sql = "INSERT INTO data (speed, distance, dtime, longitude, latitude,layer, name, trip) VALUES (%s, %s, %s, %s, %s,%s, %s, %s)"
      val = (speed, distance, time, longitude, latitude, layer, name, trip)
      mycursor.execute(sql, val)

    # Increment the current date by one day
    current_date += timedelta(days=1)

  # Commit the changes
  mydb.commit()

  print("Database filled with test data")


def retrieve_data(datatype, aggregation, startdate, enddate=None, trip=None):
  con = connect_database()
  if datatype == "speed":
    if enddate is None:
      if trip is None:
        #average speed of day
        sql = f"SELECT speed as speed, dtime as date from data WHERE DATE(dtime) = '{startdate}'"
        sql = f"SELECT date, speed as speed FROM ( SELECT DATE_FORMAT(dtime, '%H:%i') AS date, speed FROM data WHERE DATE(dtime) = '{startdate}' ) AS subquery GROUP BY date"
      else:
          #trip average speed
          sql = f"SELECT speed from data WHERE DATE(dtime) = '{startdate}' and trip = {trip}"
    else:
        if aggregation == "daily":
          #daily average speed from start to end date
          sql = f"SELECT date, avg(speed) as speed FROM ( SELECT DATE_FORMAT(dtime, '%Y-%m-%d') AS date, speed FROM data WHERE DATE(dtime) BETWEEN '{startdate}' AND '{enddate}') AS subquery GROUP BY date"
        elif aggregation == "weekly":
          #weekly average speed from start to end date
          sql = f"SELECT weekly_date, avg(speed) as speed FROM ( SELECT DATE_FORMAT(dtime, '%Y-W%v') AS weekly_date, speed FROM data WHERE DATE(dtime) BETWEEN '{startdate}' AND '{enddate}') AS subquery GROUP BY weekly_date"
        elif aggregation == "monthly":
          #monthly average speed from start to end date
          sql = f"SELECT monthly_date, avg(speed) as speed FROM ( SELECT DATE_FORMAT(dtime, '%Y-%m') AS monthly_date, speed FROM data WHERE DATE(dtime) BETWEEN '{startdate}' AND '{enddate}') AS subquery GROUP BY monthly_date"
        else:
          #yearly average speed from start to end date
          sql = f"SELECT yearly_date, avg(speed) as speed FROM ( SELECT DATE_FORMAT(dtime, '%Y') AS yearly_date, speed FROM data WHERE DATE(dtime) BETWEEN '{startdate}' AND '{enddate}') AS subquery GROUP BY yearly_date"
  elif datatype == "distance":
    if enddate is None:
        if trip is None:
          #total distance of day
          sql = f"SELECT SUM(distance) as distance, date(dtime) as date from data WHERE DATE(dtime) = '{startdate}'"
        else:
          #total distance of trip
          sql = f"SELECT distance from data WHERE DATE(dtime) = '{startdate}' and trip = {trip}"
    else:
      if aggregation == "daily":
        # daily average speed from start to end date
        sql = f"SELECT date, sum(distance) as distance FROM ( SELECT DATE_FORMAT(dtime, '%Y-%m-%d') AS date, distance FROM data WHERE DATE(dtime) BETWEEN '{startdate}' AND '{enddate}') AS subquery GROUP BY date"
      elif aggregation == "weekly":
        # weekly average speed from start to end date
        sql = f"SELECT weekly_date, sum(distance) as distance FROM ( SELECT DATE_FORMAT(dtime, '%Y-W%v') AS weekly_date, distance FROM data WHERE DATE(dtime) BETWEEN '{startdate}' AND '{enddate}') AS subquery GROUP BY weekly_date"
      elif aggregation == "monthly":
        # monthly average speed from start to end date
        sql = f"SELECT monthly_date, sum(distance) as distance FROM ( SELECT DATE_FORMAT(dtime, '%Y-%m') AS monthly_date, distance FROM data WHERE DATE(dtime) BETWEEN '{startdate}' AND '{enddate}') AS subquery GROUP BY monthly_date"
      else:
        # yearly average speed from start to end date
        sql = f"SELECT yearly_date, sum(distance) as distance FROM ( SELECT DATE_FORMAT(dtime, '%Y') AS yearly_date, distance FROM data WHERE DATE(dtime) BETWEEN '{startdate}' AND '{enddate}') AS subquery GROUP BY yearly_date"
  elif datatype == "total_trips":
    sql = f"select count(distinct trip) as trips from data where Date(dtime) = '{startdate}'"
  elif datatype == "locations":
      sql = f"select layer, name, latitude, longitude from data where Date(dtime) = '{startdate}'"

  with con.cursor(dictionary=True) as cursor:
    cursor.execute(sql)
    results = cursor.fetchall()

  con.close()
  #results = json.dumps(results)

  return results

