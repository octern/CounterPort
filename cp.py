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
	daysback = 3
	if datetime.datetime.now().date().weekday() in [1,2]:
		daysback = 5
#	lastday = datetime.datetime.now().date() - datetime.timedelta(days=daysback)
	lastday = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
	operations[lastday] = 0
	return operations

debug = 0

#symbol = "VNQ"
symbol = sys.argv[1]
end_date = sys.argv[2]


#pdb.set_trace()
operations = {}
transactions = pd.read_csv("ubs_transactions.csv")
operations = read_transactions(transactions)
dateList = []
for d in sorted(operations.keys()):
	dateList.append(d)

prices = {}
for date in dateList:
#	if date==dateList[-1]: pdb.set_trace()
	prices[date] = dp.download_one_price(date=date, symbol=symbol)[0]
#	print("{}: {}, {}".format(date.strftime("%Y-%m-%d"), round(prices[date], 2), round(operations[date])))

cpValues = {}
cpValues[dateList[0]] = round(operations[dateList[0]])
for i in range(1,len(dateList)):
	oldDate = dateList[i-1]
	newDate = dateList[i]
	oldValue = cpValues[oldDate]
	priceChange = prices[newDate] / prices[oldDate]
	valueBeforeTransaction = cpValues[oldDate] * priceChange
	valueAfterTransaction = valueBeforeTransaction + operations[newDate]
	cpValues[newDate] = round(valueAfterTransaction)
	review = {"oldDate":oldDate, "newDate":newDate, "oldValue":oldValue, "oldPrice":prices[oldDate], "newPrice":prices[newDate], "transaction":operations[newDate], "valueBeforeTransaction":valueBeforeTransaction, "valueAfterTransaction":valueAfterTransaction}
	if debug:
		for k in sorted(review.keys()):
			print("{}: {}".format(k, review[k]))
		print("---")
#		pdb.set_trace()

startValue = cpValues[dateList[0]]
endValue = cpValues[dateList[-1]]
growth = round(endValue - startValue)
growthProp = round(endValue / startValue, 2)
ops = sum(operations.values()) - operations[dateList[0]]
print("counterfactual portfolio: {}".format(symbol))
print("start value {}: {:,}".format(dateList[0].strftime("%Y-%m-%d"), startValue))
print("final value {}: {:,}".format(dateList[-1].strftime("%Y-%m-%d"), endValue))
print("growth factor: {:.0%}".format(growthProp))
print("inputs/outputs: {:,} ({:.0%} of total growth)".format(round(ops), round(ops/growth, 2)))
