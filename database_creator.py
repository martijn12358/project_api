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
  mycursor.execute("CREATE TABLE IF NOT EXISTS data (speed DOUBLE, distance DOUBLE, time DATETIME, longitude DOUBLE, latitude DOUBLE, trip INT)")

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
  mycursor.execute("CREATE TABLE IF NOT EXISTS data (speed DOUBLE, distance DOUBLE, time DATETIME, longitude DOUBLE, latitude DOUBLE, trip INT)")

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
  end_date = datetime(2023, 4, 28)

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

      # Insert the entry into the "data" table
      sql = "INSERT INTO data (speed, distance, time, longitude, latitude, trip) VALUES (%s, %s, %s, %s, %s, %s)"
      val = (speed, distance, time, longitude, latitude, trip)
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
      else:
        #trip average speed
    else:
      if aggregation == "daily":
        #daily average speed from start to end date
      elif aggregation == "weekly":
        #weekly average speed from start to end date
      elif aggregation == "monthly":
        #monthly average speed from start to end date
      else
        #yearly average speed from start to end date
  elif datatype == "distance":
    if enddate is None:
      if trip is None:
        #total distance of day
      else:
        #total distance of trip
    else:
      if aggregation == "daily":
        # daily average speed from start to end date
      elif aggregation == "weekly":
        # weekly average speed from start to end date
      elif aggregation == "monthly":
        # monthly average speed from start to end date
      else
        # yearly average speed from start to end date


  results =0
  con.close()

  return results

create_database()
data = retrieve_data("speed", "weekly", "2023-04-21", "2023-04-28", 1)
print(data)