from flask import Flask
from flask import jsonify, abort
import apimoex
import pandas as pd
import datetime as dt
from datetime import datetime
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_parser_response(tick, time):
    with requests.Session() as session:
        sec = tick
        current_datetime = datetime.now()
        datee = current_datetime
        if time == 'all':
            dateb = current_datetime - dt.timedelta(days=365 * 20)
        elif time == "year":
            dateb = current_datetime - dt.timedelta(days=365)
        elif time == "month":
            dateb = current_datetime - dt.timedelta(days=31)
        elif time == 'week':
            dateb = current_datetime - dt.timedelta(days=7)
        data2 = apimoex.get_board_candles(session=session, security=sec,
                                          interval=24,
                                          start=dateb,
                                          end=datee,
                                          market='shares',
                                          engine='stock',
                                          board='TQBR',
                                          columns='')
        res = pd.DataFrame(data2)
        sdf = list(res.begin)
        f = {}
        rall = [i.split()[0] for i in sdf]
        f['date'] = rall
        f['close'] = list(res.close)
    return f


@app.route('/parse_moex/<sec>/<time>')
def root(sec, time):
    data = get_parser_response(sec, time)
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
