from flask import Flask, jsonify, request
import mysql.connector
import datetime


app = Flask(__name__)

list_datatypes = ["speed", #returns the average speed as listed in the recieved message when only start date given, returns daily average speed if start and end date is given
                  "distance", #returns the total distance (per trip or per day?)
                  "total_trips", #returns the amount of trips made on a day (daily speed data can be sorted by trip)
                  "locations" #returns the locations of the gateways that recieved a message
                  ]
list_aggregation = ["daily",
                    "weekly",
                    "monthly",
                    "yearly"
                    ]

@app.route('/project-data', methods = ['GET'])
def projectdata():
    #retrieve arguments from api request
    startdate = request.args.get('startdate')
    enddate = request.args.get('enddate')
    datatype = request.args.get('datatype')
    aggregation = request.args.get('aggregation')
    trip = request.args.get('trip')

    #check data validity
    #check startdate
    if startdate is None:
        return jsonify({'error': 'no startdate entered'}), 400
    else:
        if not is_date(startdate):
            return jsonify({'error': 'invalid startdate'}),400
    #check datatype
    if datatype is None:
        return jsonify({'error': 'no datatype entered'}),400
    else:
        if datatype not in list_datatypes:
            return jsonify({'error': 'invalid datatype'}), 400
    #check aggregation
    if aggregation is not None:
        if aggregation not in list_aggregation:
            return jsonify({'error': "invalid aggregation type"}), 400
    #check enddate
    if enddate is not None:
        if not is_date(enddate):
            return jsonify({'error': 'invalid enddate'}), 400
        elif startdate == enddate:
            #return jsonify({'error': 'enddate same as startdate'}), 400
            enddate = None
        elif startdate > enddate:
            return jsonify({'error': 'enddate before startdate'}), 400
    if trip is not None:
        if not trip.isdigit():
            return jsonify({'error': 'invalid trip'}), 400

    #check request and return data
    if datatype == "speed":
        if enddate is None:
            if trip is None:
                #database request speed on given day
                return jsonify({
                          "data": [
                            {
                              "speed": 11,
                              "time": "2023-04-05T12:30:00"
                            },
                            {
                              "speed": 6,
                              "time": "2023-04-05T12:31:00"
                            },
                            {
                              "speed": 9,
                              "time": "2023-04-05T12:32:00"
                            }
                          ]
                        }
                        )
            else:
                #database request speed of requested trip on given day
                return jsonify({
                    "data": [
                        {
                            "speed": 11,
                            "time": "2023-04-05T12:30:00",
                            "trip": trip
                        },
                        {
                            "speed": 6,
                            "time": "2023-04-05T12:31:00",
                            "trip": trip
                        },
                        {
                            "speed": 9,
                            "time": "2023-04-05T12:32:00",
                            "trip": trip
                        }
                    ]
                }
                )
        elif aggregation is None:
            return jsonify({'error': 'no given aggregation'}), 400
        else:
            if aggregation == "daily":
                #database request speed daily from given dates
                return jsonify({
                          "data": [
                            {
                              "speed": 10.5,
                              "date": "2023-04-05"
                            },
                            {
                              "speed": 12.3,
                              "date": "2023-04-06"
                            },
                            {
                              "speed": 15.2,
                              "date": "2023-04-07"
                            }
                          ]
                        }
                        )
            elif aggregation == "monthly":
                # database request speed monthly from given dates
                return jsonify({
                      "data": [
                        {
                          "speed": 12.5,
                          "monthly_date": "2023-04"
                        },
                        {
                          "speed": 12.3,
                          "monthly_date": "2023-05"
                        },
                        {
                          "speed": 12.2,
                          "monthly_date": "2023-06"
                        }
                      ]
                    }
                    )
            elif aggregation == "weekly":
                # database request speed weekly from given dates
                return jsonify({
                          "data": [
                            {
                              "speed": 10.5,
                              "weekly_date": "2023-W14"
                            },
                            {
                              "speed": 11.3,
                              "weekly_date": "2023-W15"
                            },
                            {
                              "speed": 11.2,
                              "weekly_date": "2023-W16"
                            }
                          ]
                        })

            elif aggregation == "yearly":
                # database request speed yearly from given dates
                return jsonify({
                    {
                        "data": [
                            {
                                "speed": 12.5,
                                "yearly_date": "2023"
                            },
                            {
                                "speed": 12.3,
                                "yearly_date": "2024"
                            },
                            {
                                "speed": 13.2,
                                "yearly_date": "2025"
                            }
                        ]
                    }

                })
    elif datatype == "distance":
        if enddate is None:
            # database request distance on given date
            return jsonify({"data": [
                        {
                            "distance": 10.5
                        }
            ]})
        elif aggregation is None:
            return jsonify({'error': 'no given aggregation'}), 400
        else:
            if aggregation == "daily":
                # database request distance daily from given dates
                return jsonify({
                    "data": [
                        {
                            "distance": 10.5,
                            "date": "2023-04-05"
                        },
                        {
                            "distance": 12.3,
                            "date": "2023-04-06"
                        },
                        {
                            "distance": 15.2,
                            "date": "2023-04-07"
                        }
                    ]
                }
                )
            elif aggregation == "monthly":
                # database request distance monthly from given dates
                return jsonify({
                    "data": [
                        {
                            "distance": 100.5,
                            "monthly_date": "2023-04"
                        },
                        {
                            "distance": 120.3,
                            "monthly_date": "2023-05"
                        },
                        {
                            "distance": 150.2,
                            "monthly_date": "2023-06"
                        }
                    ]
                }
                )
            elif aggregation == "weekly":
                # database request distance weekly from given dates
                return jsonify({
                          "data": [
                            {
                              "distance": 40.5,
                              "weekly_date": "2023-W14"
                            },
                            {
                              "distance": 22.3,
                              "weekly_date": "2023-W15"
                            },
                            {
                              "distance": 35.2,
                              "weekly_date": "2023-W16"
                            }
                          ]
                        })
            elif aggregation == "yearly":
                # database request distance yearly from given dates
                return jsonify({
                    {
                        "data": [
                            {
                                "distance": 1000.5,
                                "yearly_date": "2023"
                            },
                            {
                                "distance": 1200.3,
                                "yearly_date": "2024"
                            },
                            {
                                "distance": 1500.2,
                                "yearly_date": "2025"
                            }
                        ]
                    }

                })
    elif datatype == "total_trips":
        # database request total trips on given date
        return jsonify({"data" : [{"total trips on " + startdate: "2"}]})
    elif datatype == "locations":
        # database request locations on given date
        return jsonify({
                  "data": [
                    {
                      "name": "test1",
                      "latitude": 52.2215,
                      "longitude": 6.8937
                    },
                    {
                      "name": "test2",
                      "latitude": 52.2225,
                      "longitude": 6.8958
                    },
                    {
                      "name": "test3",
                      "latitude": 52.2245,
                      "longitude": 6.8967
                    }
                  ]
                }
                )

    return jsonify({'error': 'unreachable statement'}),400


def is_date(string):
    try:
        datetime.datetime.strptime(string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    app.run()

