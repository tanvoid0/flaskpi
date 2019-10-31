import json
from flask import Flask, request, jsonify, Response, render_template
import pandas as pd
import requests
import numpy as np

app = Flask(__name__)

def soilTest(value):
    if value == 0:
        return 'Dry'
    elif value == 1:
        return 'Wet'
    elif value == 2:
        return 'Very Wet'
    else:
        return ''

@app.route('/')
def home():
    return "<h1>Welcome to our server !!</h1>"

@app.route('/api')
def datamine():
    # url = "http://djangpi.herokuapp.com/api/datalogs/"
    url = request.args.get('url')

    datalogs = requests.get(url=url).json()
    # return render_template("index.html", data=datalogs)
    data_frame = pd.DataFrame(datalogs, columns=['id', 'light', 'temperature', 'humidity', 'soil', 'moisture', 'alive'])
    # return render_template("index.html", data=data_frame)
    data_frame_filter = data_frame.query('alive!=0')
    data_frame_filter['soil'] = np.where(data_frame_filter['soil'] == 'Dry', 0, data_frame_filter['soil'])
    data_frame_filter['soil'] = np.where(data_frame_filter['soil'] == 'Wet', 1, data_frame_filter['soil'])
    data_frame_filter['soil'] = np.where(data_frame_filter['soil'] == 'Very Wet', 2, data_frame_filter['soil'])

    # return render_template("index.html", data=data_frame_filter)

    data = {
        'light': [
            data_frame_filter['light'].min(),
            data_frame_filter['light'].max()
        ],
        'temperature': [
            data_frame_filter['temperature'].min(),
            data_frame_filter['temperature'].max()
        ],
        'humidity': [
            data_frame_filter['humidity'].min(),
            data_frame_filter['humidity'].max()
        ],
        'soil': [
            soilTest(data_frame_filter['soil'].min())
            ,
            soilTest(data_frame_filter['soil'].max())
        ],
        'moisture': [
            data_frame_filter['moisture'].min(),
            data_frame_filter['moisture'].max()
        ]
    }
    return Response(json.dumps(data))


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
