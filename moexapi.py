from flask import Flask
from flask import jsonify, abort
import apimoex
import pandas as pd
from datetime import datetime
import requests

app = Flask(__name__)


def get_parser_response(tick, dateb, datee):
    engine = 'stock'
    market = 'shares'
    board = 'TQBR'
    request_url = ('https://iss.moex.com/iss/engines/{}/'
                   'markets/{}/boards/{}/securities.json'.format(engine, market, board))

    arguments = {
    }
    z = 0
    res = {}

    with requests.Session() as session:
        iss = apimoex.ISSClient(session, request_url, arguments)
        data = iss.get()
        df_meta = pd.DataFrame(data['securities'])
        sec = tick
        data = apimoex.get_board_history(session, sec, board=board)
        z += 1

        if data != []:

            data2 = apimoex.get_board_candles(session=session, security=sec,
                                              interval=24,
                                              start=dateb,
                                              end=datee,
                                              market='shares',
                                              engine='stock',
                                              board='TQBR',
                                              columns='')

            print(sec)
            res = data2
    return res


@app.route('/parse_moex/<sec>/<str_date_b>/<str_date_e>')
def root(sec, str_date_b, str_date_e):
        dateb = datetime.strptime(str_date_b, '%Y-%m-%d')
        datee = datetime.strptime(str_date_e, '%Y-%m-%d')
        data = get_parser_response(sec, dateb, datee)
        print(data)
        return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
