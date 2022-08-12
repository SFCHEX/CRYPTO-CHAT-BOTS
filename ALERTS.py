
import discord
import time
import requests
import json
from discord.ext import commands
import asyncio
# above I'm importing the libraries Im gonna use
api_key='0VCBO0B3MGL9XO6H'

secret='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImdldGV6ZEBnbWFpbC5jb20iLCJpYXQiOjE2MDEzMzM2MjAsImV4cCI6NzkwODUzMzYyMH0._BPI_HLgGJvd2YG8jx36R4v5XFGYstE-wjRI-xuek1k'

bot_token='NzUzNzQ3OTY1NjUwNDAzMzQ4.X1qsfg.Psvb55sgG_HnKlpZLW-vpGsZQhA'

client= commands.Bot(command_prefix='s!')
# the bot prefix
notify_forex_list_keltner=['USDEUR','AUDCAD','AUDCHF','AUDHKD','AUDJPY','AUDNZD','AUDSGD','AUDUSD',
        'CADCHF','CADHKD','CADJPY','CADSGD','CHFHKD','CADJPY','CADSGD','CHFHKD','CHFJPY','CHFZAR',
        'EURAUD','EURCAD','EURCHF','EURCZK','EURDKK','EURGBP','EURHKD','EURHUF','EURJPY','EURNOK','EURNZD',
        'EURPLN','EURSEK','EURSGD','EURTRY','EURZAR','GBPAUD','GBPCAD','GBPCHF','GBPHKD','GBPJPY','GBPNZD',
        'GBPPLN','GBPSGD','GBPUSD','GBPZAR','HKDJPY','NZDCAD','NZDCHF','NZDHKD','NZDJPY','NZDSGD','NZDUSD',
        'SGDCHF','SGDHKD','SGDJPY','TRYJPY','USDCAD','USDCHF','USDCZK','USDDKK','USDHKD','USDHUF','USDJPY',
        'USDMXN','USDNOK','USDPLN','USDSAR','USDSEK','USDSGD','USDTHB','USDTRY','USDZAR','ZARJPY']
# the forex list is above, u can add an item with a comma and make sure to put it in quotes
crytpos_list=['BTCUSD','ETHUSD','LINKUSD','TRXUSD','BNBUSD','DOTUSD','BCHUSD','ADAUSD','SXPUSD','XRPUSD','EOSUSD','LTCUSD','BANDUSD','COMPUSD','ATOMUSD',
#        'XLMUSD','NEOUSD','VETUSD','ETCUSD','ONTUSD','ZECUSD','XMRUSD','BATUSD','IOTAUSD','DASHUSD']
# cryptos I havnt done these yet
notify_stocks_list_keltner=['IBM','AAPL']

notify_stocks_list_bollinger=['IBM','AAPL']
notify_forex_list_bollinger=['USDEUR','AUDCAD','AUDCHF','AUDHKD','AUDJPY','AUDNZD','AUDSGD','AUDUSD',
        'CADCHF','CADHKD','CADJPY','CADSGD','CADJPY','CADSGD','CHFHKD','CHFZAR',
        'EURAUD','EURCAD','EURCHF','EURCZK','EURDKK','EURGBP','EURHKD','EURHUF','EURJPY','EURNOK','EURNZD',
        'EURPLN','EURSEK','EURSGD']
#stock list, you can add any stocks here 

#https://www.alphavantage.co/query?function=ATR&symbol=IBM&interval=daily&time_period=14&apikey=demo


def grab(parameters):
    raw_data=requests.get(url='https://www.alphavantage.co/query?',params=parameters).json()
    return raw_data 

def grab_taapio(function,paramters):
    raw_data= requests.get(url='https://api.taapi.io/'+function+'?',params=parameters).json()
    return raw_data['value']

def current_value_indicator(parameters):
    grab(parameters)
    raw_data=grab(parameters)

    return float(list(raw_data["Technical Analysis: "+parameters['function']].values())[0][parameters['function']])
def current_value_intraday(parameters):
    grab(parameters)
    raw_data=grab(parameters)
    return float(list(raw_data["Time Series "+'('+parameters['interval']+')'].values())[0]['4. close'])

def bollinger_band(parameters):
    grab(parameters)
    raw_data=grab(parameters)
    return list(raw_data["Technical Analysis: "+parameters['function']].values())[0]



def grab_keltner(symbol):
    ATR=current_value_indicator({'function':'ATR','symbol':symbol,'interval':'1min','time_period':'10','apikey':api_key})

    Middle_Line= current_value_indicator({'function':'EMA','symbol':symbol,'interval':'1min','time_period':'144','series_type':'close','apikey':api_key})
    Upper_Channel_Line= (Middle_Line ) +( 9  * ATR)
    Lower_Channel_Line= (Middle_Line) -(9 * ATR)
    keltner_channel={'Middle_Line':Middle_Line,'Upper_Channel_Line':Upper_Channel_Line,'Lower_Channel_Line':Lower_Channel_Line}
    return keltner_channel

def grab_keltner_crypto(symbol):
    ATR = grab_taapio('atr',{'secret'=secret,'exchange':'binance','symbol':symbol,'interval':'1min','optInTimePeriod':'14'})
    Middle_Line=grab_taapio('ema',{'secret'=secret,'exchange':'binance','symbol':symbol,'interval':'1min','period':'10'})
    Upper_Channel_Line= (Middle_Line ) +( 9  * ATR)
    Lower_Channel_Line= (Middle_Line) -(9 * ATR)
    keltner_channel={'Middle_Line':Middle_Line,'Upper_Channel_Line':Upper_Channel_Line,'Lower_Channel_Line':Lower_Channel_Line}
    return keltner_channel


    



   

#https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo
@client.event
async def on_ready():
    print(str(client.user)+' is online!')
    channel_alert=client.get_channel(753731537115283518)
    channel_stream_forex_keltner=client.get_channel(753731615435391147)
    channel_stream_forex_bollinger=client.get_channel(757329382623936555)
    channel_stream_stocks_bollinger=client.get_channel(757329611045601442)
    channel_stream_stocks_keltner=client.get_channel(754414240474857572)


    while True:
        #https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=LINK&to_currency=USD&apikey=0VCBO0B3MGL9XO6H
    
        for currency in notify_forex_list_keltner:
            value=float(grab({'function':'CURRENCY_EXCHANGE_RATE','from_currency':currency[0:3],'to_currency':currency[3:],'apikey':api_key})["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
            kelt=grab_keltner(currency)
            if kelt['Upper_Channel_Line']==value or kelt['Lower_Channel_Line']==value:
                await channel_alert.send('{} is currently valued at ${} and has a keltner channel of {}'.format(currency,value,kelt))
                await channel_alert.send('\n----------------------')
            else:
                await channel_stream_forex_keltner.send('Currency: {}\nValueUSD: {}\n Keltner: {}\n'.format(currency,value,kelt))
                await channel_stream_forex_keltner.send('\n------------------------')






        for currency in notify_forex_list_bollinger:
            value=float(grab({'function':'CURRENCY_EXCHANGE_RATE','from_currency':currency[0:3],'to_currency':currency[3:],'apikey':api_key})["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
            Bband=bollinger_band({'function':'BBANDS','symbol':currency,'interval':'1min','time_period':'5','series_type':'close','apikey':api_key})
            if float(Bband['Real Upper Band'])==value or float(Bband['Real Lower Band'])==value:
                await channel_alert.send('{} is currently valued at ${} and has a Bollinger band of {}'.format(currency,value,Bband))
                await channel_alert.send('\n----------------------------')

            else:
                await channel_stream_forex_bollinger.send('Currency: {}\nValueUSD: {}\n Bollinger: {}\n'.format(currency,value,Bband))

                await channel_stream_forex_bollinger.send('\n----------------------------')



    


        for stocks in notify_stocks_list_keltner:
            value=current_value_intraday({'function':'TIME_SERIES_INTRADAY','symbol':stocks,'interval':'1min','apikey':api_key})
            kelt=grab_keltner(stocks)
            if kelt['Upper_Channel_Line']==value or kelt['Lower_Channel_Line']==value:
                await channel_alert.send('{} is currently valued at ${} and has a keltner channel of {}'.format(stocks,value,kelt))
                await channel_alert.send('\n--------------------')
            else:
                await channel_stream_stocks_keltner.send('Symbol: {}\nValueUSD: {}\n Keltner: {}\n'.format(stocks,value,kelt))
                await channel_stream_stocks_keltner.send('\n-----------------------')





        
        for stocks in notify_stocks_list_bollinger:
            value=current_value_intraday({'function':'TIME_SERIES_INTRADAY','symbol':stocks,'interval':'1min','apikey':api_key})
            Bband=bollinger_band({'function':'BBANDS','symbol':stocks,'interval':'1min','time_period':'144','series_type':'close','apikey':api_key})
            if float(Bband['Real Upper Band'])==value or float(Bband['Real Lower Band'])==value:
                await channel_alert.send('{} is currently valued at ${} and has a Bollinger band of {}'.format(stocks,value,Bband))
                await channel_alert.send('\n----------------------------')
            else:
                await channel_stream_stocks_bollinger.send('Currency: {}\nValueUSD: {}\n Bollinger: {}\n'.format(stocks,value,Bband))
                await channel_stream_stocks_bollinger.send('\n----------------------------')




        for crypto in cryptos_list:
            value=grab_taapio()
            Bband=grab_taapio()
            kelt=grab_taapio()
            if value=kelt['Lower_Channel_Band'] or value=kelt['Upper_Channel_Band']:
                await channel_alert.send('{} is currenty values at ${} and has a keltner of {}'.format(crypto,value, kelt))
                await channel_alert.send('---------------------')
            else:
                await channel_stream_keltner_crypto.send('{} is currenty values at ${} and has a keltner of {}'.format(crypto,value, kelt))
                await channel_stream_keltner_crypto.send('------------------------')
             if float(Bband['Real Upper Band'])==value or float(Bband['Real Lower Band'])==value:
                await channel_alert.send('{} is currently valued at ${} and has a Bollinger band of {}'.format(crypto,value,Bband))
                await channel_alert.send('\n----------------------------')
            else:
                await channel_stream_bollinger_crypto.send('Currency: {}\nValueUSD: {}\n Bollinger: {}\n'.format(crypto,value,Bband))
                await channel_stream_bollinger_crytpo.send('\n----------------------------')


 



 

client.run(bot_token)
