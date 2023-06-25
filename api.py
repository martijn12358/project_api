from flask import Flask, jsonify, request
import datetime


class Api(Flask):
    def __init__(self, database):
        super().__init__(__name__)
        self.route('/project-data')(self.projectdata)
        self.list_datatypes = ["speed",
                               # returns the average speed as listed in the recieved message when only start date given, returns daily average speed if start and end date is given
                               "distance",  # returns the total distance (per trip or per day?)
                               "total_trips",
                               # returns the amount of trips made on a day (daily speed data can be sorted by trip)
                               "locations",  # returns the locations of the gateways that received a message
                               "battery",  # returns battery percentage
                               ]
        self.list_aggregation = ["daily",
                                 "weekly",
                                 "monthly",
                                 "yearly"
                                 ]
        self.database = database

    def projectdata(self):
        # retrieve arguments from api request
        startdate = request.args.get('startdate')
        enddate = request.args.get('enddate')
        datatype = request.args.get('datatype')
        aggregation = request.args.get('aggregation')
        trip = request.args.get('trip')
        circumference = request.args.get('circumference')

        # check data validity
        # check startdate
        if circumference is not None:
            if circumference.isdigit():
                self.database.enter_bike_circumference(circumference)
                return jsonify({'info': 'successfully saved bike info'})
            else:
                return jsonify({'error': 'not a number'})
        if startdate is None:
            return jsonify({'error': 'no startdate entered'}), 400
        else:
            if not self._is_date(startdate):
                return jsonify({'error': 'invalid startdate'}), 400
        # check datatype
        if datatype is None:
            return jsonify({'error': 'no datatype entered'}), 400
        else:
            if datatype not in self.list_datatypes:
                return jsonify({'error': 'invalid datatype'}), 400
        # check aggregation
        if aggregation is not None:
            if aggregation not in self.list_aggregation:
                return jsonify({'error': "invalid aggregation type"}), 400
        # check enddate
        if enddate is not None:
            if not self._is_date(enddate):
                return jsonify({'error': 'invalid enddate'}), 400
            elif startdate == enddate:
                # return jsonify({'error': 'enddate same as startdate'}), 400
                enddate = None
            elif startdate > enddate:
                return jsonify({'error': 'enddate before startdate'}), 400
        if trip is not None:
            if not trip.isdigit():
                return jsonify({'error': 'invalid trip'}), 400

        # check request and return data
        if datatype == "speed":
            if enddate is None:
                # if trip is None:
                # database request speed on given day
                # data = database_functions.retrieve_data(datatype, aggregation, startdate, enddate, trip)
                # return jsonify({"data": data})
                # else:
                # database request speed of requested trip on given day
                data = self.database.retrieve_data(datatype, aggregation, startdate, enddate, trip)
                return jsonify({"data": data})
            elif aggregation is None:
                return jsonify({'error': 'no given aggregation'}), 400
            else:
                data = self.database.retrieve_data(datatype, aggregation, startdate, enddate, trip)
                return jsonify({"data": data})
        elif datatype == "distance":
            if enddate is None:
                # database request distance on given date
                data = self.database.retrieve_data(datatype, aggregation, startdate, enddate, trip)
                return jsonify({"data": data})
            elif aggregation is None:
                return jsonify({'error': 'no given aggregation'}), 400
            else:
                data = self.database.retrieve_data(datatype, aggregation, startdate, enddate, trip)
                return jsonify({"data": data})
        elif datatype == "total_trips":
            # database request total trips on given date
            data = self.database.retrieve_data(datatype, aggregation, startdate, enddate, trip)
            return jsonify({"data": data})
        elif datatype == "locations":
            # database request locations on given date
            data = self.database.retrieve_data(datatype, aggregation, startdate, enddate, trip)
            return jsonify({"data": data})

        return jsonify({'error': 'unreachable statement'}), 400

    def _is_date(self, string):
        try:
            datetime.datetime.strptime(string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
