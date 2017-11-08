#!/usr/bin/python

import stockapp

cmd = '' 
while(cmd != 'X') and (cmd != 'x'):
	cmd = input("請輸入要使用的功能(x:離開/1:產生股票資料/2:查詢股票股價):")
	tag = ''
	if (cmd == '1'):
		while(tag != 'X') and (tag != 'x'):
			tag = input("請輸入要產生的股票資料(x:離開):")
			tag = tag.strip()
			if (tag == 'X') or (tag == 'x'):
				break
			else:
				date = stockapp.StockApp.func_finddate()
				print (u"日期:",date)
				dfss = stockapp.StockApp.func_ConnectToStoresSite(date,tag)
				print (u'股權資料取得完成!')
				filename = stockapp.StockApp.func_stockName(dfss)
				dfskg = stockapp.StockApp.func_ConnectToKimoGiven(tag)
				print (u'公司配息資料取得完成!')
				dfscd = stockapp.StockApp.func_stockCompanydataStores(tag)
				print (u'公司基本資料取得完成!')
				years = input("請輸入開始年:")
				seansons = input("請輸入開始季:")
				yeare = input("請輸入結束年:")
				seansone = input("請輸入結束季:")
				sdd = stockapp.StockApp.func_dog_data(tag,years,seansons,yeare,seansone)
				print (u'財報狗資料取得完成!')
				stockapp.StockApp.func_stockStores(filename+ '(' + tag +')',dfss,dfskg,dfscd,sdd)
				print (u'存取到' + filename+ '(' + tag +')' + '完成')


	elif (cmd == '2'):
		while(tag != 'X') and (tag != 'x'):
			tag = input("請輸入要查詢的股票(x:離開):")
			tag = tag.strip()
			if (tag == 'X') or (tag == 'x'):
				break
			else:
				stockapp.StockApp.func_search_stockvalue(tag)
	elif (cmd == 'x') or (cmd == 'X'):
		print("exit programming!!")
		break


