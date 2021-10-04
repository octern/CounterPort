import yfinance as yf
import datetime
import time
import requests
import io

def download_prices(start, end, symbol):
	stock_final = pd.DataFrame()
	for i in symbols:
		print( str(symbols.index(i)) + str(' : ') + i, sep=',', end=',', flush=True)

		try:
			# download the stock price
			stock = []
			stock = yf.download(i,start=start, end=end, progress=False)

			# append the individual stock prices
			if len(stock) == 0:
				None
			else:
				stock['Name']=i
				stock_final = stock_final.append(stock,sort=False)
		except Exception:
			None
	return stock_final

def download_one_price(date, symbol):
	start=date
	end=date + datetime.timedelta(days=1)
	try:
		# download the stock price
		price = yf.download(symbol,start=start, end=end, progress=False)["Open"]
	except Exception:
		print("unable to get stock price for {}".format(date))
		price=None
	return price


def download_ubs():
	ubs_url="https://docs.google.com/spreadsheets/d/1pIJUTq1GgGJ7WRHcuaNuUiHdrnNXsArJBt_Cn9Kv4lU/edit?usp=sharing"
	res=requests.get(url=ubs_url)
	open('google.csv', 'wb').write(res.content)

def main(start, end, symbols):
	res=download_prices(start, end, symbols)
	print(res)

if __name__ == "__main__":
	start = datetime.datetime(2020,2,1)
	end = datetime.datetime(2020,2,6)
	symbols = ["AAPL"]
	print(5)
	main(start, end, symbols)
