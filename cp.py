import pandas as pd
import yfinance as yf
import download_prices as dp
import datetime
import time
import requests
import io
import sys
import pdb

def udate(datestr):
	return datetime.datetime.strptime(datestr, "%Y-%m-%d").date()

def read_transactions(transactions):
	for index, row in transactions.iterrows():
		ts = udate(row.Date)
		val = row.total_value
		if ts in operations.keys():
			operations[ts] = operations[ts]+val
		else:
			operations[ts] = val
		operations[datetime.datetime.now().date() - datetime.timedelta(days=3)] = 0
	return operations


#symbols = [sys.argv[0]]

symbols = ["AAPL"]

#pdb.set_trace()
operations = {}
transactions = pd.read_csv("ubs_transactions.csv")
operations = read_transactions(transactions)
dateList = []
for d in sorted(operations.keys())[0:5]:
	dateList.append(d)

prices = {}
for date in dateList:
	prices[date] = dp.download_one_price(date=date, symbol=symbols[0])[0]
	print(prices[date])

cpValues = {}
cpValues[dateList[0]] = operations[dateList[0]]
for i in range(1,len(dateList)):
	oldDate = dateList[i-1]
	newDate = dateList[i]
	oldValue = cpValues[oldDate]
	priceChange = prices[newDate] / prices[oldDate]
	valueBeforeTransaction = cpValues[oldDate] * priceChange
	valueAfterTransaction = valueBeforeTransaction + operations[newDate]
	cpValues[newDate] = valueAfterTransaction
	review = {"oldDate":oldDate, "newDate":newDate, "oldValue":oldValue, "oldPrice":prices[oldDate], "newPrice":prices[newDate], "transaction":operations[newDate], "valueBeforeTransaction":valueBeforeTransaction, "valueAfterTransaction":valueAfterTransaction}
	for k in sorted(review.keys()):
		print("{}: {}".format(k, review[k]))
	print("---")
	pdb.set_trace()
