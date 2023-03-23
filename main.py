from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/project-data', methods = ['GET'])
def projectdata():
    startdate = request.args.get('startdate')
    enddate = request.args.get('enddate')
    if startdate is None:
        text = "invalid date"
    else:
        text = startdate
    return jsonify({'data': [{'date': startdate, 'KM/H': '13'}, {'date': startdate, 'KM/H': '12'}]})

if __name__ == '__main__':
    app.run(debug=True)

