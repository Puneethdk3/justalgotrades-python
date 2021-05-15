#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 21:14:47 2021

@author: pkaribasappa
"""


import json, time
from flask import Flask, request, jsonify
import sys

import requests
from alice_blue import *
import os
import datetime
import pytz
from flask_cors import CORS, cross_origin
from pytz import timezone
import threading
import random
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
import logging


from os.path import isfile, join
from os import listdir


logging.basicConfig(level=logging.INFO)

isFirstTime = False

#websocket var
exitWS1 = False
exitWS2 = False

#candleData
isCandle3MinDataGot = False
isCandle5MinDataGot = False
isCandle15MinDataGot = False
isCandle60MinDataGot = False

#Upstox
upstoxApiKey = 'dPMbue9lq7abjTPCeuJ0Y8tYNEXdwKDd3OQiashl'
upstoxAccessToken = '1a0a8288920d43cf17d05d6ebab8e09898422065'
#Upstox

allData=[]
access_token=None
api_secret = ''
clientId = 'AB203323'
password = 'DKP@v@5'
answer = 'no'
socket_opened = False
path = "/Users/pkaribasappa/Desktop/Share/UpstoxAlgo/Websocket/"
websocketBroker = "aliceblue"
    
livePath=""
livePathExit="" 
candle3minPath=""
candle5minPath=""
candle15minPath=""
candle60minPath=""

current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'aliceblue')
livePath = os.path.join(final_directory, r'live')
candle3minPath = os.path.join(final_directory, r'candle3min')
candle5minPath = os.path.join(final_directory, r'candle5min')
candle15minPath = os.path.join(final_directory, r'candle15min')
candle60minPath = os.path.join(final_directory, r'candle60min')

   
   
def socket_example(intradaySymbols, purpose, access_token):
    print("socket")
    global allData
    
    alice = AliceBlue(username=clientId, password=password, access_token=access_token, master_contracts_to_download=['NSE'])
    
    print(alice.get_balance())
    alice.start_websocket(subscribe_callback=event_handler_quote_update,
                      socket_open_callback=open_callback,
                      run_in_background=True)
    while(socket_opened==False):
        pass
    
    subscribeArray = []
    
    incr=0
    for name in intradaySymbols:
        
        obj = alice.get_instrument_by_symbol('NSE', name)
        if (obj!=None):
            subscribeArray.append(obj)
        incr+=1
           
            
    
    alice.subscribe(subscribeArray, LiveFeedType.MARKET_DATA)
    
def socket_example_exit(intradaySymbols, purpose, access_token):
    print("socket")
    global allData
    
    alice = AliceBlue(username=clientId, password=password, access_token=access_token, master_contracts_to_download=['NSE'])
    
    print(alice.get_balance())
    alice.start_websocket(subscribe_callback=event_handler_quote_update_exit,
                      socket_open_callback=open_callback,
                      run_in_background=True)
    while(socket_opened==False):
        pass
    
    subscribeArray = []
    
    incr=0
    for name in intradaySymbols:
        
        obj = alice.get_instrument_by_symbol('NSE', name)
        if (obj!=None):
            subscribeArray.append(obj)
        incr+=1
           
            
    
    alice.subscribe(subscribeArray, LiveFeedType.SNAPQUOTE)
    
def open_callback():
    global socket_opened
    socket_opened = True
    

def getCandleData(symbol, whichCandle, date, apikey, accessToken):
    try:
        headers = {
                    'Authorization': 'Bearer '+accessToken,
                    'x-api-key': apikey
                  }
        url = "https://api.upstox.com/historical/nse_eq/"+symbol+"/"+whichCandle+"?format=json&start_date="+date+"&end_date="+date+"";
        res = requests.get(url, headers=headers)
        
        data = res.json()["data"];
        return data
    except Exception as e:
        data = []
        return data

@app.route('/api/live', methods=['GET'])
@cross_origin(origin='*')
def getLive():
    data = ""
    global livePath
    try:        
        path = livePath+'/'
        token = request.args["instrumenttoken"]
        fullPath = path + token+".json"
        data=""
        
        with open(fullPath,'r') as f:
            s = f.read()
            s = s.replace('\t','')
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            s = s.replace("'", '"')
            data = json.loads(s)
            f.close()
    except Exception as e:
        data = {}
    return data

@app.route('/api/live/exit', methods=['GET'])
@cross_origin(origin='*')
def getLiveExit():
    data = ""
    global livePathExit
    try:        
        path = livePathExit+'/'
        token = request.args["instrumenttoken"]
        fullPath = path + token+".json"
        data=""
        
        with open(fullPath,'r') as f:
            s = f.read()
            s = s.replace('\t','')
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            s = s.replace("'", '"')
            data = json.loads(s)
            f.close()
    except Exception as e:
        data = {}
    return data

@app.route('/api/candle/3M', methods=['GET'])
@cross_origin(origin='*')
def getCandle3Min():
    global candle3minPath
    data = ""
    try:
        path = candle3minPath+'/'
        token = request.args["instrumenttoken"]
        fullPath = path + token+".json"
        data=""
        
        with open(fullPath,'r') as f:
            s = f.read()
            s = s.replace('\t','')
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            s = s.replace("'", '"')
            data = json.loads(s)
            f.close()
    except Exception as e:
        data = {}
    return data

@app.route('/api/candle/5M', methods=['GET'])
@cross_origin(origin='*')
def getCandle5Min():
    global candle5minPath
    data = ""
    try:
        path = candle5minPath+'/'
        token = request.args["instrumenttoken"]
        fullPath = path + token+".json"
        data=""
        
        with open(fullPath,'r') as f:
            s = f.read()
            s = s.replace('\t','')
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            s = s.replace("'", '"')
            data = json.loads(s)
            f.close()
    except Exception as e:
        data = {}
    return data

@app.route('/api/candle/15M', methods=['GET'])
@cross_origin(origin='*')
def getCandle15Min():
    global candle15minPath
    data = ""
    try:
        path = candle15minPath+'/'
        token = request.args["instrumenttoken"]
        fullPath = path + token+".json"
        data=""
        
        with open(fullPath,'r') as f:
            s = f.read()
            s = s.replace('\t','')
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            s = s.replace("'", '"')
            data = json.loads(s)
            f.close()
    except Exception as e:
        data = {}
    return data

@app.route('/api/candle/60M', methods=['GET'])
@cross_origin(origin='*')
def getCandle60Min():
    global candle60minPath
    data = ""
    try:
        path = candle60minPath+'/'
        token = request.args["instrumenttoken"]
        fullPath = path + token+".json"
        data=""
        
        with open(fullPath,'r') as f:
            s = f.read()
            s = s.replace('\t','')
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            s = s.replace("'", '"')
            data = json.loads(s)
            f.close()
    except Exception as e:
        data = {}
    return data
    
def writeToFile(fullPath, content):
    print(fullPath)
    f = open(fullPath, "w")
    f.write(str(content))
    f.close()
    
    
def event_handler_quote_update_exit(message):
    #print(message)
    global livePathExit,  exitWS1, exitWS2
    if(exitWS2 == True):
        sys.exit('Exiting')
        
    symbol = str(str(str(message["instrument"]).split(",")[2]).split("=")[1])
    symbol = symbol.replace("'","")
    bid_prices = message["bid_prices"]
    ask_prices = message["ask_prices"]
    exchange_time_stamp = str(message["exchange_time_stamp"])
    buyers = message["buyers"]
    bid_quantities = message["bid_quantities"]
    sellers = message["sellers"]
    ask_quantities = message["ask_quantities"]
    
    x = {
        "symbol": symbol,
        "bid_prices": bid_prices,
        "buyers": buyers,
        "bid_quantities": bid_quantities,
        "ask_prices": ask_prices,
        "sellers": sellers,
        "ask_quantities": ask_quantities,
        "exchange_time_stamp": exchange_time_stamp
    }
    fullPath = livePathExit + '/' + str(message["token"])+".json"
    writeToFile(fullPath, x)
    
def isGotFirstCandleData(date, whichCandle):
    res = getCandleData('SBIN', str(whichCandle), date, upstoxApiKey, upstoxAccessToken)
    if (len(res) ==0):
        res = getCandleData('TCS', str(whichCandle), date, upstoxApiKey, upstoxAccessToken)
        if (len(res) ==0):
            res = getCandleData('INFY', str(whichCandle), date, upstoxApiKey, upstoxAccessToken)
            if (len(res) ==0):
                return False
            else:
                return True
        else: 
            return True
    else:
        return True
        
def fetchCandleDataFromUpstox(date, whichCandle, candlePath):
    global livePath, exitWS1, exitWS2, isCandle3MinDataGot, isCandle5MinDataGot
    global isCandle15MinDataGot, isCandle60MinDataGot
    tradesWithToken = []
    tradesWithToken = getTodaysTradesWithToken()
    if (len(tradesWithToken) ==0):
        tradesWithToken = getTodaysTradesWithToken()
        if (len(tradesWithToken) ==0):
            tradesWithToken = getTodaysTradesWithToken()
            if (len(tradesWithToken) ==0):
                tradesWithToken = getTodaysTradesWithToken()
            
    isGot = False
    while(isGot==False):
        isGot = isGotFirstCandleData(date, whichCandle)
    start = time.time()
    for t in tradesWithToken:
        try:
            token = str(t["instrumenttoken"])
            symbol = str(t["symbol"])
            fullPath = candlePath + '/' + token+".json"
            if(os.path.exists(fullPath) == False):
                print("Fetching 3min candle data")
                res = getCandleData(symbol, str(whichCandle), date, upstoxApiKey, upstoxAccessToken)
                if(len(res) > 0):
                    candleData = {
                        "symbol": symbol,
                        "high": res[0]["high"],
                        "low": res[0]["low"],
                        "exchange_time_stamp": res[0]["timestamp"]
                    }
                    writeToFile(fullPath, candleData)
                    if (int(whichCandle) == 3):
                        isCandle3MinDataGot = True
                    if (int(whichCandle) == 5):
                        isCandle5MinDataGot = True
                    if (int(whichCandle) == 15):
                        isCandle15MinDataGot = True
                    if (int(whichCandle) == 60):
                        isCandle60MinDataGot = True
        except Exception as e:
            print(str(e))
        
    print(f'Time taken to fetch all candles data : {time.time() - start}')
    
        
    
def event_handler_quote_update(message):
    #print(message)
    
    global livePath, candle3minPath, candle5minPath, candle15minPath, candle60minPath, exitWS1, exitWS2, isCandle3MinDataGot, isCandle5MinDataGot, isCandle15MinDataGot, isCandle60MinDataGot
    
    if(exitWS1 == True):
        sys.exit('Exiting')
        
    symbol = str(str(str(message["instrument"]).split(",")[2]).split("=")[1])
    symbol = symbol.replace("'","")
    open = str(message["open"])
    high = str(message["high"])
    low = str(message["low"])
    close = str(message["close"])
    atp = str(message["ltp"])
    total_buy_quantity = str(message["total_buy_quantity"])
    total_sell_quantity = str(message["total_sell_quantity"])
    bid_price = str(message["best_bid_price"])
    ask_price = str(message["best_ask_price"])
    bid_quantities = str(message["best_bid_quantity"])
    ask_quantities = str(message["best_ask_quantity"])
    volume = str(message["volume"])
    exchange_time_stamp = str(message["exchange_time_stamp"])
    
    
    
    x = {
        "symbol": symbol,
        "token": str(message["token"]),
    	"open": open,
        "high": high,
        "low": low,
        "close": close,
        "ltp": atp,
        "total_buy_quantity": total_buy_quantity,
        "total_sell_quantity": total_sell_quantity,
        "bid_price": bid_price,
        "ask_price": ask_price,
        "bid_qty": bid_quantities,
        "ask_qty": ask_quantities,
        "volume": volume,
        "exchange_time_stamp": exchange_time_stamp
    }
    
    exchangeTime = datetime.datetime.fromtimestamp(int(exchange_time_stamp), timezone('Asia/Kolkata'))
    eHour = exchangeTime.hour
    eMin = exchangeTime.minute
    eSec = exchangeTime.second
    token = str(message["token"])
    fullPath = livePath + '/' + token+".json"
    writeToFile(fullPath, x)
    
    date = str(exchangeTime.day).zfill(2) +"-"+ str(exchangeTime.month).zfill(2) +"-"+ str(exchangeTime.year).zfill(2)
    print(date +" "+str(eHour)+":"+str(eMin)+":"+str(eSec))
    
    
    if(eHour==9 and eMin==18 and eMin <=19 and (eSec>=30)):
        fullPath = candle3minPath + '/' + token+".json"
        if(os.path.exists(fullPath) == False):
            candleData = {
                    "symbol": symbol,
                    "high": high,
                    "low": low,
                    "exchange_time_stamp": exchange_time_stamp
                }
            writeToFile(fullPath, candleData)
            
        
    if(eHour==9 and eMin==20 and eMin<=21 and (eSec>=30)):
        fullPath = candle5minPath + '/' + token+".json"
        if(os.path.exists(fullPath) == False):
            candleData = {
                    "symbol": symbol,
                    "high": high,
                    "low": low,
                    "exchange_time_stamp": exchange_time_stamp
                }
            writeToFile(fullPath, candleData)
    if(eHour==9 and eMin==30 and eMin<=21 and (eSec>=30)):
        fullPath = candle15minPath + '/' + token+".json"
        if(os.path.exists(fullPath) == False):
            candleData = {
                    "symbol": symbol,
                    "high": high,
                    "low": low,
                    "exchange_time_stamp": exchange_time_stamp
                }
            writeToFile(fullPath, candleData)
    if(eHour==10 and eMin==15 and eMin<=21 and (eSec>=30)):
        fullPath = candle60minPath + '/' + token+".json"
        if(os.path.exists(fullPath) == False):
            candleData = {
                    "symbol": symbol,
                    "high": high,
                    "low": low,
                    "exchange_time_stamp": exchange_time_stamp
                }
            writeToFile(fullPath, candleData)
# =============================================================================
#         if (isCandle5MinDataGot == False):
#             print("getting ready for candle data fetch for 5 min")
#             fetchCandleDataFromUpstox(date, '5', candle5minPath)
#             if (isCandle5MinDataGot == False):
#                 print("nomore candle data found, something is wrong with 5 min candle from upstox--Error")
#                 fullPath = candle5minPath + '/' + token+".json"
#                 if(os.path.exists(fullPath) == False):
#                     candleData = {
#                             "symbol": symbol,
#                             "high": high,
#                             "low": low,
#                             "exchange_time_stamp": exchange_time_stamp
#                         }
#                     writeToFile(fullPath, candleData)
#         if (isCandle5MinDataGot == True):
#             fullPath = candle5minPath + '/' + token+".json"
#             if(os.path.exists(fullPath) == False):
#                 candleData = {
#                         "symbol": symbol,
#                         "high": high,
#                         "low": low,
#                         "exchange_time_stamp": exchange_time_stamp
#                     }
#                 writeToFile(fullPath, candleData)
# =============================================================================

    
def getIntradaySymbols():
    url = "http://pro.justalgotrades.com/api/trades/today"
    headers = {'Content-Type': 'application/json'}
    res = requests.get(url, headers=headers)

    print(res)
    data = res.json()["data"]
    return data

def getExistingAccessToken():
    url = "https://pro.justalgotrades.com/api/client/eligible"
    headers = {'Content-Type': 'application/json'}
    res = requests.get(url, headers=headers)

    print(res)
    data = res.json()["data"]
    return random.choice(data)["accesstoken"]

def getRandomClientId():
    url = "https://pro.justalgotrades.com/api/client/eligible"
    headers = {'Content-Type': 'application/json'}
    res = requests.get(url, headers=headers)

    print(res)
    data = res.json()["data"]
    return random.choice(data)["clientid"]


def getTodaysTradesWithToken():
    
    data = []
    try:
        clientId = getRandomClientId()
        url = "https://pro.justalgotrades.com/api/trades/clients/"+str(clientId)
        headers = {'Content-Type': 'application/json'}
        res = requests.get(url, headers=headers)
    
        print("CandleFetch=======================fetching trades for clientid="+str(clientId))
        data  = res.json()["data"]
    except Exception as e:
        print(str(e))
    return data

        
def startUpdate():
    global access_token
    
        
    data=""
    try:
        data = getIntradaySymbols()
    except Exception as e:
        print(str(e))
        data = getIntradaySymbols()
    
    print("got intraday symbols")
    allSymbols=[]
    access_token = getExistingAccessToken()
    print(access_token)
    for name in data:
        allSymbols.append(name)
        
    #print("Aliceblue access token = "+access_token)
    socket_example(allSymbols,"update", access_token)
    
def startUpdateExit():
    global access_token
    
        
    data=""
    try:
        data = getIntradaySymbols()
    except Exception as e:
        print(str(e))
        data = getIntradaySymbols()
    
    print("got intraday symbols")
    allSymbols=[]
    access_token = getExistingAccessToken()
    print(access_token)
    for name in data:
        allSymbols.append(name)
        
    #print("Aliceblue access token = "+access_token)
    socket_example_exit(allSymbols,"update", access_token)
    


@app.route('/api/candle/update/3M', methods=['POST'])
@cross_origin(origin='*')
def updateCandle3Min():
    global candle3minPath
    data = request.json
    fullPath = candle3minPath + '/' + str(data["token"])+".json"
    
    if(os.path.exists(fullPath) == False):
        print("updating candle data 3M for "+str(data["symbol"]))
        candleData = {
                "symbol": str(data["symbol"]),
                "high": str(data["high"]),
                "low": str(data["low"]),
                "exchange_time_stamp": str(data["timestamp"])
            }
        writeToFile(fullPath, candleData)
    return {'data': 'Updated 3Min candle for '+str(data["symbol"])}


@app.route('/api/candle/update/5M', methods=['POST'])
@cross_origin(origin='*')
def updateCandle5Min():
    global candle5minPath
    data = request.json
    fullPath = candle5minPath + '/' + str(data["token"])+".json"
    
    if(os.path.exists(fullPath) == False):
        print("updating candle data 5M for "+str(data["symbol"]))
        candleData = {
                "symbol": str(data["symbol"]),
                "high": str(data["high"]),
                "low": str(data["low"]),
                "exchange_time_stamp": str(data["timestamp"])
            }
        writeToFile(fullPath, candleData)
    return {'data': 'Updated 5Min candle for '+str(data["symbol"])}

@app.route('/api/candle/update/15M', methods=['POST'])
@cross_origin(origin='*')
def updateCandle15Min():
    global candle15minPath
    data = request.json
    fullPath = candle15minPath + '/' + str(data["token"])+".json"
    
    if(os.path.exists(fullPath) == False):
        print("updating candle data 15M for "+str(data["symbol"]))
        candleData = {
                "symbol": str(data["symbol"]),
                "high": str(data["high"]),
                "low": str(data["low"]),
                "exchange_time_stamp": str(data["timestamp"])
            }
        writeToFile(fullPath, candleData)
    return {'data': 'Updated 15Min candle for '+str(data["symbol"])}

@app.route('/api/candle/update/60M', methods=['POST'])
@cross_origin(origin='*')
def updateCandle60Min():
    global candle60minPath
    data = request.json
    fullPath = candle60minPath + '/' + str(data["token"])+".json"
    
    if(os.path.exists(fullPath) == False):
        print("updating candle data 60M for "+str(data["symbol"]))
        candleData = {
                "symbol": str(data["symbol"]),
                "high": str(data["high"]),
                "low": str(data["low"]),
                "exchange_time_stamp": str(data["timestamp"])
            }
        writeToFile(fullPath, candleData)
    return {'data': 'Updated 60Min candle for '+str(data["symbol"])}
        

@app.route('/api/fetch/access', methods=['POST'])
@cross_origin(origin='*')
def fetchAccessToken():
    data = request.json
    username = str(data["username"])
    password = str(data["password"])
    api_secret = str(data["api_secret"])
    answer = str(data["answer"])
    appid = str(data["appid"])
    if not appid:
        appid = None
    print("requested accessToken for username = "+str(username))

    try:
        accessToken = AliceBlue.login_and_get_access_token(username = username, password = password, twoFA = answer,  api_secret = api_secret, app_id = appid)
        
    except Exception as e:
        print(str(e))
        accessToken = AliceBlue.login_and_get_access_token(username = username, password = password, twoFA = answer,  api_secret = api_secret, app_id = appid)
        
    return {'access_token': str(accessToken), "username": username}




@app.route('/api/websocket/start', methods=['GET'])
@cross_origin(origin='*')
def startWebsocket():
    
    global final_directory, livePath, candle3minPath, candle5minPath, candle15minPath, candle60minPath, upstoxAccessToken
    global exitWS1, isCandle3MinDataGot, isCandle5MinDataGot, isCandle15MinDataGot, isCandle60MinDataGot
    exitWS1 = False
    isCandle3MinDataGot = False
    isCandle5MinDataGot = False
    isCandle15MinDataGot = False
    isCandle60MinDataGot = False
    
    upstoxAccessToken = request.args.get('upstoxAccessToken')
    print(upstoxAccessToken)
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'aliceblue')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    else:
        os.system("rm -rf "+final_directory)
    
    livePath = os.path.join(final_directory, r'live')
    if not os.path.exists(livePath):
        os.makedirs(livePath)
    else:
        os.system("rm -rf "+livePath)
    
    candle3minPath = os.path.join(final_directory, r'candle3min')
    if not os.path.exists(candle3minPath):
        os.makedirs(candle3minPath)
    else:
        os.system("rm -rf "+candle3minPath)
    
    candle5minPath = os.path.join(final_directory, r'candle5min')
    if not os.path.exists(candle5minPath):
        os.makedirs(candle5minPath)
    else:
        os.system("rm -rf "+candle5minPath)

    candle15minPath = os.path.join(final_directory, r'candle15min')
    if not os.path.exists(candle15minPath):
        os.makedirs(candle15minPath)
    else:
        os.system("rm -rf "+candle15minPath)

    candle60minPath = os.path.join(final_directory, r'candle60min')
    if not os.path.exists(candle60minPath):
        os.makedirs(candle60minPath)
    else:
        os.system("rm -rf "+candle60minPath)
   
    startUpdate()
    return {'status': 'started'}

@app.route('/api/websocket/start/exit', methods=['GET'])
@cross_origin(origin='*')
def startWebsocketForExit():
    global final_directory, livePathExit, upstoxAccessToken, exitWS2, isCandle3MinDataGot, isCandle5MinDataGot, isCandle15MinDataGot, isCandle60MinDataGot
    exitWS2 = False
    isCandle3MinDataGot = False
    isCandle5MinDataGot = False
    isCandle15MinDataGot = False
    isCandle60MinDataGot = False
    
    upstoxAccessToken = request.args.get('upstoxAccessToken')
    print(upstoxAccessToken)
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'aliceblue-exit')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    else:
        os.system("rm -rf "+final_directory)
    
    livePathExit = os.path.join(final_directory, r'live')
    if not os.path.exists(livePathExit):
        os.makedirs(livePathExit)
    else:
        os.system("rm -rf "+livePathExit)
   
    startUpdateExit()
    return {'status': 'started'}


    
    
@app.route('/api/websocket/start/end', methods=['GET'])
@cross_origin(origin='*')
def endWebsocketStart():
    global exitWS1
    exitWS1 = True
    print('reset variable for websocket start')
    return {'status': 'reset variable for websocket start'}

@app.route('/api/websocket/start/exit/end', methods=['GET'])
@cross_origin(origin='*')
def endWebsocketExit():
    global exitWS2
    exitWS2 = True
    print('reset variable for websocket exit')
    return {'status': 'reset variable for websocket exit'}



@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    # Allow crossdomain for other HTTP Verbs
    #if request.method != 'OPTIONS' and 'Origin' in request.headers:
    h['Access-Control-Allow-Origin'] = '*'

    return resp


@app.route('/api/live/all/full', methods=['GET'])
@cross_origin(origin='*')
def getFullData():
    data = []
    global livePath
    try:        
        path = livePath+'/'
        
        mypath = path
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        print(onlyfiles)

        for file in onlyfiles:
            fullPath = path + file
            
            with open(fullPath,'r') as f:
                s = f.read()
                s = s.replace('\t','')
                s = s.replace('\n','')
                s = s.replace(',}','}')
                s = s.replace(',]',']')
                s = s.replace("'", '"')
                
                data.append(json.loads(s))
                f.close()
    except Exception as e:
        print(str(e))
    return {"data": data}



   
#print(getExistingAccessToken()) 
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)







