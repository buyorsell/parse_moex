from db_handler import Stock, moex_session
import requests
from fastapi import FastAPI
from datetime import timedelta, date, datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_moex(date2):

	start = 0
	while True:
		url = (
			f'http://iss.moex.com/iss/history/engines/stock/'
			f'markets/shares/boards/TQBR/securities.json?'
			f'date={date2.strftime("%Y-%m-%d")}&start={start}'
		)

		with requests.get(url) as response:

			stock_json = response.json()

			for data in stock_json['history']['data']:

				data_dict = dict(zip(stock_json['history']['columns'], data))

				if data_dict['NUMTRADES'] != 0 and len(data_dict['SECID']) < 7:
					stock = Stock(

						boardid=data_dict['BOARDID'],

						date=date2,

						secid=data_dict['SECID'],

						open=data_dict['OPEN'],
						close=data_dict['CLOSE'],

						low=data_dict['LOW'],
						high=data_dict['HIGH'],

						numtrades=data_dict['NUMTRADES']

					)

					moex_session.add(stock)

			moex_session.commit()

			print(date2, stock_json['history']['data'] != [])

			start += 100

			if stock_json['history.cursor']['data'][0][1] < start:
				break
@app.get("/")
async def getall():
	current_datetime = datetime.now()
	a = (str(current_datetime).split())[0].split('-')
	end_date = date(int(a[0]), int(a[1]), int(a[2]))
	start_date = date(2012, 1, 1)
	def daterange(start_date, end_date):
		for n in range(int((end_date - start_date).days)):
			yield start_date + timedelta(n)
	for single_date in daterange(start_date, end_date):
		date2 = single_date
		parse_moex(date2)

@app.get("/<dateg>")
async def getdate(dateg):
	parse_moex(dateg)
