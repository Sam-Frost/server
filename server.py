'''

1. Single fuction to get attendace and timetable, both within a single login session


How to run : 
python -u server.py

How to use :

send POST request to /attendace or /timetable with request body(json):
{
    "username" : "20CSU093",
    "password" : "QRjFyqJp"
}

eg: http://127.0.0.1:5000/attendace


'''
from academics import get_attendance, get_timetable
from flask import Flask, request

app = Flask(__name__)

@app.route('/attendance', methods=['POST'])
def attendance():
    data = request.get_json()
    return get_attendance(data['username'], data['password'])

@app.route('/timetable', methods=['POST'])
def timetable():
    data = request.get_json()
    return get_timetable(data['username'], data['password'])

if __name__ == '__main__':
    app.run(debug=True)
