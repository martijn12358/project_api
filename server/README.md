# project_api

the url that is used for the api is: https://api.martijn12358.nl/project-data

the api takes 6 arguments 
the parameters are:  
datatype, to select the type of data (e.g. distance, average speed) (required)  
startdate, to select the date of which data must be collected (required)  
enddate, to select the end date where date must be collected  
aggregation, to select how data is aggregated (e.g. weekly, daily)
trip, to select from which trip data must be collected
circumference, to set the circumference of the wheel that needs to be used to calculate the distance and speet

# datatype can be any of the types below  
"speed", returns the average speed as listed in the recieved message when only start date given, returns daily average speed if start and end date is given  
"distance" returns the total distance (per trip or per day?)  
"total_trips" returns the amount of trips made on a day (daily speed data can be sorted by trip)  
"locations" returns the locations of the gateways that recieved a message  
"battery" returns the battery percentage of the device
"circumference" returns the circumference that is stored in the database

# aggregation can be any of the types below
"daily"  
"weekly"  
"monthly"  
"yearly"  

# examples
retrieve the average speed for a day
```
https://api.martijn12358.nl/project-data?startdate=2023-2-2&datatype=speed
```
request the distance for a date range
```
https://api.martijn12358.nl/project-data?startdate=2023-2-2&datatype=distance&enddate=2023-2-5&aggregation=daily
```
