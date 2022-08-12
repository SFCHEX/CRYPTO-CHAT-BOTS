import discord
import requests
import json
from discord.ext import commands
import bs4
import binance.client

binance_key='GrGWA0SGe2R0BuaosslKnYmKD53J3mROdyPrz0zjq62DAOixw5pTpG2FP7kfvMdm'
binance_secret='9dh3qHiDMy7jXdmQ8iTNECzhYMSW4pfsIteJ1PokCErxWIlmTMv9osgLqgYg5yAR' 
binance_client = binance.client.Client(binance_key, binance_secret)
#symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC


info = binance_client.get_margin_price_index(symbol='BTCUSDT')


api_key='0VCBO0B3MGL9XO6H'
secret='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImdldGV6ZEBnbWFpbC5jb20iLCJpYXQiOjE2MDEzMzM2MjAsImV4cCI6NzkwODUzMzYyMH0._BPI_HLgGJvd2YG8jx36R4v5XFGYstE-wjRI-xuek1k'
bot_token='NzUzNzQ3OTY1NjUwNDAzMzQ4.X1qsfg.Psvb55sgG_HnKlpZLW-vpGsZQhA'


crytpos_list=['BTCUSD','ETHUSD','LINKUSD','TRXUSD','BNBUSD','DOTUSD','BCHUSD','ADAUSD','SXPUSD','XRPUSD','EOSUSD','LTCUSD','BANDUSD','COMPUSD','ATOMUSD','XLMUSD','NEOUSD','VETUSD','ETCUSD','ONTUSD','ZECUSD','XMRUSD','BATUSD','IOTAUSD','DASHUSD']

client= commands.Bot(command_prefix='s!')

def grab(function, parameters):
    raw_data= requests.get(url='https://api.taapi.io/'+function+'?', params=parameters).json()
    return raw_data



@client.event
async def on_ready():
    print(str(client.user)+' is online!')
    alert_channel=client.get_channel(753731537115283518)
    stream_channel=client.get_channel(764425665168146432)
    
    while True:
        for crypto in crytpos_list:
            val=float(binance_client.get_margin_price_index(symbol=crypto+'T')['price'])
            value=round(val,4)
            bollinger_band=grab('bbands2',parameters={'secret':secret,'exchange':'binance','symbol':crypto[0:-3]+'/'+crypto[-3:]+'T','interval':'1m','period':'200'})

            if round(bollinger_band['valueLowerBand'],4)==value or round(bollinger_band['valueUpperBand'],4)==value:
                await alert_channel.send('symbol: {}\nvalue:{}\nbbands: {}'.format(crypto,value,bollinger_band))
                await alert_channel.send('\n-----------------------------------')
            else:

                await stream_channel.send('symbol: {}\nvalue:{}\nbbands: {}'.format(crypto,value,bollinger_band))                
                await stream_channel.send('\n-----------------------------------')

client.run(bot_token)


            
