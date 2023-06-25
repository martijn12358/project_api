import json

import mysql.connector
from random import uniform, randint
from datetime import datetime, timedelta


class Database:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def connect_database(self):
        mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        # Check if the connection is successful
        if mydb.is_connected():
            print("Connected to the MySQL server")
        else:
            print("Failed to connect to the MySQL server")
        return mydb

    def create_database(self):
        mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        # Create a cursor object
        mycursor = mydb.cursor()

        # Create the database if it does not exist
        mycursor.execute("CREATE DATABASE IF NOT EXISTS data")

        # Use the "data" database
        mycursor.execute("USE data")

        # Create the "data" table with the specified fields
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS data (speed DOUBLE, distance DOUBLE, dtime DATETIME, longitude DOUBLE, latitude DOUBLE, trip INT)")
        mycursor.execute("CREATE TABLE IF NOT EXISTS bike (id INT, circumference Double, battery Double)")

        # Commit the changes
        mydb.commit()

        sql = "INSERT INTO bike(id, circumference) VALUES (1, 2)"
        mycursor.execute(sql)
        mydb.commit()

        print("Database created successfully")

    def reset_database(self):
        # Connect to the MySQL server
        mydb = self.connect_database()

        # Create a cursor object
        mycursor = mydb.cursor()

        # Drop the "data" table if it exists
        mycursor.execute("DROP TABLE IF EXISTS data")
        mycursor.execute("DROP TABLE IF EXISTS bike")

        # Create the "data" table with the specified fields
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS data (speed DOUBLE, distance DOUBLE, dtime DATETIME, longitude DOUBLE, latitude DOUBLE, layer TEXT, name TEXT, trip INT)")
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS bike (id INT, circumference DOUBLE, battery DOUBLE)")

        # Commit the changes
        mydb.commit()

        sql = "INSERT INTO bike(id, circumference) VALUES (1, 2)"
        mycursor.execute(sql)
        mydb.commit()

        print("Database reset successfully")

    def database_checker(self):
        mydb = self.connect_database()
        mycursor = mydb.cursor()
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS data (speed DOUBLE, distance DOUBLE, dtime DATETIME, longitude DOUBLE, latitude DOUBLE, layer TEXT, name TEXT, trip INT)")
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS bike (id INT, circumference DOUBLE, battery DOUBLE)")
        mydb.commit()
        print("tables made if not present previously")

    def enter_message(self, speed, distance, dtime, longitude, latitude, layer, name, trip):
        mydb = self.connect_database()
        mycursor = mydb.cursor()
        sql = "INSERT INTO data (speed, distance, dtime, longitude, latitude, layer, name, trip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (speed, distance, dtime, longitude, latitude, layer, name, trip)
        try:
            # Execute the SQL query with the provided values
            mycursor.execute(sql, values)

            # Commit the changes to the database
            mydb.commit()

            print("Data inserted successfully!")
        except Exception as e:
            print(f"Error inserting data: {e}")
        mycursor.close()
        mydb.close()

    def enter_bike_circumference(self, circumference):
        mydb = self.connect_database()
        mycursor = mydb.cursor()
        sql = "INSERT INTO bike (circumference) VALUES (%s) WHERE id = 1"
        values = circumference
        try:
            # Execute the SQL query with the provided values
            mycursor.execute(sql, (values,))

            # Commit the changes to the database
            mydb.commit()

            print("Data inserted successfully!")
        except Exception as e:
            print(f"Error inserting data: {e}")
        mycursor.close()
        mydb.close()

    def enter_bike_battery(self, battery):
            mydb = self.connect_database()
            mycursor = mydb.cursor()
            sql = "INSERT INTO bike (circumference) VALUES (%s) WHERE id = 1"
            values = battery
            try:
                # Execute the SQL query with the provided values
                mycursor.execute(sql, (values,))

                # Commit the changes to the database
                mydb.commit()

                print("Data inserted successfully!")
            except Exception as e:
                print(f"Error inserting data: {e}")
            mycursor.close()
            mydb.close()

    def fill_database(self):
        # Connect to the MySQL server and select the "data" database
        mydb = self.connect_database()

        # Create a cursor object
        mycursor = mydb.cursor()

        # Define the date range
        start_date = datetime(2023, 4, 21)
        end_date = datetime(2023, 6, 15)

        enschede_latitude = 52.219373
        enschede_longitude = 6.895129

        # Loop through each date in the range
        current_date = start_date
        while current_date <= end_date:
            # Generate 100 random entries for the current date
            for i in range(100):
                speed = randint(4, 8)
                distance = randint(240, 480)
                time = current_date + timedelta(minutes=i)
                longitude = round(enschede_longitude + uniform(-0.01, 0.01), 6)
                latitude = round(enschede_latitude + uniform(-0.01, 0.01), 6)
                trip = 0
                layer = "markers"
                name = "test" + str(randint(0, 10000))

                # Insert the entry into the "data" table
                sql = "INSERT INTO data (speed, distance, dtime, longitude, latitude,layer, name, trip) VALUES (%s, %s, %s, %s, %s,%s, %s, %s)"
                val = (speed, distance, time, longitude, latitude, layer, name, trip)
                mycursor.execute(sql, val)

                # Increment the current date by one day
            current_date += timedelta(days=1)

        # Commit the changes
        mydb.commit()

        print("Database filled with test data")

    def retrieve_data(self, datatype, aggregation, startdate, enddate=None, trip=None):
        con = self.connect_database()
        if datatype == "speed":
            if enddate is None:
                if trip is None:
                    # average speed of day
                    sql = f"SELECT DATE_FORMAT(d.dtime, '%H:%i') AS date, round(AVG((b.circumference / d.speed)*3.6),2) AS speed FROM data d CROSS JOIN bike b WHERE DATE(d.dtime) = '{startdate}' GROUP BY date;"
                else:
                    # trip average speed
                    sql = f"SELECT DATE_FORMAT(d.dtime, '%H:%i') AS date, round(AVG((b.circumference / d.speed)*3.6),2) AS speed FROM data d CROSS JOIN bike b WHERE DATE(d.dtime) BETWEEN = '{startdate}' AND trip = {trip} GROUP BY date;"
            else:
                if aggregation == "daily":
                    # daily average speed from start to end date
                    sql = f"SELECT DATE_FORMAT(d.dtime, '%Y-%m-%d') AS date, round(AVG((b.circumference / d.speed)*3.6),2) AS speed FROM data d CROSS JOIN bike b WHERE DATE(d.dtime) BETWEEN '{startdate}' AND '{enddate}'GROUP BY date;"
                elif aggregation == "weekly":
                    # weekly average speed from start to end date
                    sql = f"SELECT DATE_FORMAT(d.dtime, '%Y-W%v') AS weekly_date, round(AVG((b.circumference / d.speed)*3.6),2) AS speed FROM data d CROSS JOIN bike b WHERE DATE(d.dtime) BETWEEN '{startdate}' AND '{enddate}'GROUP BY weekly_date;"
                elif aggregation == "monthly":
                    # monthly average speed from start to end date
                    sql = f"SELECT DATE_FORMAT(d.dtime, '%Y-%m') AS monthly_date, round(AVG((b.circumference / d.speed)*3.6),2) AS speed FROM data d CROSS JOIN bike b WHERE DATE(d.dtime) BETWEEN '{startdate}' AND '{enddate}'GROUP BY monthly_date;"
                else:
                    # yearly average speed from start to end date
                    sql = f"SELECT DATE_FORMAT(d.dtime, '%Y') AS yearly_date, AVG((b.circumference / d.speed)*3.6) AS speed FROM data d CROSS JOIN bike b WHERE DATE(d.dtime) BETWEEN '{startdate}' AND '{enddate}'GROUP BY yearly_date;"
        elif datatype == "distance":
            if enddate is None:
                if trip is None:
                    # total distance of day
                    sql = f"SELECT round(SUM((distance * b.circumference)/1000), 2) as distance from data d CROSS JOIN bike b WHERE DATE(dtime) = '{startdate}'"
                else:
                    # total distance of trip
                    sql = f"SELECT round(SUM((distance * b.circumference)/1000), 2) as distance from data d CROSS JOIN bike b WHERE DATE(dtime) = '{startdate}' and trip = {trip}"
            else:
                if aggregation == "daily":
                    # daily average speed from start to end date
                    sql = f"SELECT DATE_FORMAT(d.dtime, '%Y-%m-%d') AS date, round(SUM((distance * b.circumference)/1000), 2) AS distance FROM data d CROSS JOIN bike b WHERE DATE(d.dtime) BETWEEN '{startdate}' AND '{enddate}'GROUP BY date;"
                elif aggregation == "weekly":
                    # weekly average speed from start to end date
                    sql = f"SELECT DATE_FORMAT(d.dtime, '%Y-W%v') AS weekly_date, round(SUM((distance * b.circumference)/1000), 2) AS distance FROM data d CROSS JOIN bike b WHERE DATE(d.dtime) BETWEEN '{startdate}' AND '{enddate}'GROUP BY weekly_date;"
                elif aggregation == "monthly":
                    # monthly average speed from start to end date
                    sql = f"SELECT DATE_FORMAT(d.dtime, '%Y-%m') AS monthly_date, round(SUM((distance * b.circumference)/1000), 2) AS distance FROM data d CROSS JOIN bike b WHERE DATE(d.dtime) BETWEEN '{startdate}' AND '{enddate}'GROUP BY monthly_date;"
                else:
                    # yearly average speed from start to end date
                    sql = f"SELECT DATE_FORMAT(d.dtime, '%Y') AS yearly_date, round(SUM((distance * b.circumference)/1000), 2) AS distance FROM data d CROSS JOIN bike b WHERE DATE(d.dtime) BETWEEN '{startdate}' AND '{enddate}'GROUP BY yearly_date;"
        elif datatype == "total_trips":
            sql = f"select count(distinct trip) as trips from data where Date(dtime) = '{startdate}'"
        elif datatype == "locations":
            if enddate is None:
                sql = f"select layer, name, latitude, longitude from data where Date(dtime) = '{startdate}'"
            else:
                sql = f"select layer, name, latitude, longitude from data where Date(dtime) BETWEEN '{startdate}' AND {enddate}"
        with con.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

        con.close()
        # results = json.dumps(results)

        return results
