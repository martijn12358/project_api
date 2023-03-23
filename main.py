from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/project-data', methods = ['GET'])
def projectdata():
    date = request.args.get('date')
    if date is None:
        text = "invalid date"
    else:
        text = date
    return jsonify({'message': text})

if __name__ == '__main__':
    app.run(debug=True)

