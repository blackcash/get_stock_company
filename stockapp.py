#!/usr/bin/python

import time
from bs4 import BeautifulSoup
import requests
import pandas
from openpyxl import load_workbook
import numpy as np
import json
from pandas import Series, DataFrame 

class StockApp:

	def func_dog_data(stockNum,years,seansons,yeare,seansone):
		res = requests.get('https://statementdog.com/api/v1/fundamentals/' + stockNum + '/'+ years +'/' + seansons + '/'+ yeare +'/' + seansone + '/cf?queried_by_user=true&_=1508471446198')
		encodedjson =  json.loads(res.text)
		print (encodedjson['1']['data']['ticker_name'])
		data = {}
		years =[]
		for year in encodedjson['59']['data']:
			years.append(year[2])
		print (years)
		for index in range(102,58,-1):			
			years_data = []
			for y in range(0,len(years)):
				print (years[y],encodedjson[str(index)]['label'],":",encodedjson[str(index)]['data'][y][1])
				years_data.append(encodedjson[str(index)]['data'][y][1])
			data[encodedjson[str(index)]['label']] = years_data
		dfs = DataFrame(data) 
		idx = 0
		dfs.insert(loc = idx, column = u'項次', value = years)
		return dfs

	def func_finddate():
		isOK = 0
		err_cou = 0
		while isOK == 0:
			try:
				head ={
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'Connection':'keep-alive',
				'Host':'www.tdcc.com.tw',
				'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
				}
				rs = requests.session()
				res = rs.get('https://www.tdcc.com.tw/smWeb/QryStock.jsp',headers = head)
				bs = BeautifulSoup(res.text,'lxml')
				date = bs.select("select option")[0].text
				isOK = 1
			except:
				err_cou = err_cou + 1
				print ('except finddate')
				if (err_cou > 5):
					print ('err too much')
					isOK = 1
		return date
	
	def func_ConnectToStoresSite(date,stockNum):
		isOK = 0
		err_cou = 0
		while isOK == 0:
			try:
				dfs = pandas.read_html('https://www.tdcc.com.tw/smWeb/QryStock.jsp?SCA_DATE=' + date + '&SqlMethod=StockNo&StockNo=' + stockNum + '&StockName=&sub=%ACd%B8%DF')
				isOK = 1
			except:
				err_cou = err_cou + 1 
				print ('except func_ConnectToStoresSite')
				if (err_cou > 5):
					print ('err too much')
					isOK = 1
		return dfs

	def func_ConnectToKimoGiven(stockNum):
		isOK = 0
		err_cou = 0
		while isOK == 0:
			try:
				dfs = pandas.read_html('https://tw.stock.yahoo.com/d/s/dividend_' + stockNum + '.html')
				isOK = 1
			except:
				err_cou = err_cou + 1 
				print ('except func_ConnectToKimoGiven')
				if (err_cou > 5):
					print ('err too much')
					isOK = 1
		return dfs


	def func_stockName(dfs):
		df = dfs[5]
		df = df.ix[:,0:0]
		title = str(df.values.tolist()[0])
		num = title.rfind('：')
		stockName = title[(num + 1):(len(title)- 2)]
		print (stockName)
		return stockName


	def func_stockStores(filename , dfss , dfskg , dfscd, sdd):
		ss = dfss[6]
		skg = dfskg[9]
		scd = dfscd[9]
		scd = scd.replace(np.nan, '', regex=True)

		path = filename + time.strftime("%Y%m%d") +'.xlsx'
		writer = pandas.ExcelWriter(path, engine='xlsxwriter')
		scd.to_excel(writer,sheet_name =  filename +'公司資料' ,index=False)
		writer.save()
		writer.close()

		book = load_workbook(path)
		writer = pandas.ExcelWriter(path, engine = 'openpyxl')
		writer.book = book
		sdd.to_excel(writer,sheet_name = filename +'財報狗資料',index=False)
		skg.to_excel(writer,sheet_name =  filename +'配息' ,index=False)
		ss.to_excel(writer,sheet_name = filename +'股權',index=False)
		writer.save()
		writer.close()
		
	def func_stockCompanydataStores(stockNum):
		dfs = pandas.read_html('https://tw.stock.yahoo.com/d/s/company_' + stockNum + '.html')
		return dfs

	def func_search_stockvalue(stockNum):
		try:
			res = requests.get('https://tw.stock.yahoo.com/q/q?s=' + stockNum)
			bs = BeautifulSoup(res.text,'lxml')
			tables = bs.select('table')
			trs = tables[6].select('tr')
			tds = trs[1].select('td')
			print (tds[0].text[0:len(tds[0].text)-6],tds[2].text)
		except:
			print ("請確定網路或股號是否正確!!")
			