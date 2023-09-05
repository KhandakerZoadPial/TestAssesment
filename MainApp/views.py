from django.shortcuts import render
import pandas as pd
import asyncio
import json
from django.core.files import File
from django.http import JsonResponse
from .models import JsonFiles

import string    
import random
import os




# Defining Candle Class, we could use Django Models too
# As we do not need to save every row on database, 
# We can simply use normal Classes-Objects
class Candle():
    def __self__(self, symbol, open, high, low, close, date):
        self.symbol = symbol
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.date = date
    
    def to_dict(self):
        return {
            "symbol": self.symbol,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "date": self.date
        }




async def convert_candles_to_timeframe(one_minute_candles):
    output_candle = Candle()

    
    output_candle.open = one_minute_candles[0].open
    output_candle.close = one_minute_candles[-1].close
    output_candle.volume = sum(candle.volume for candle in one_minute_candles)
    output_candle.high = max(candle.high for candle in one_minute_candles)
    output_candle.low = min(candle.low for candle in one_minute_candles)
    output_candle.date = one_minute_candles[0].date
    output_candle.symbol = one_minute_candles[0].symbol

    

    return output_candle


# This View Shows user the uploading form(GET) And Accepts the Form Data(POST)
def upload_csv(request):
    if request.method == 'POST':
        uploaded_csv_file = request.FILES['csv']
        selected_timeframe = int(request.POST.get('timeframe'))

        # We are reading the received CSV file
        df = pd.read_csv(uploaded_csv_file)
        # Taking only the rows for the selected_timeframe
        df = df.head(selected_timeframe)
        print(df.keys())

        one_minute_candles = []

        for i, row in df.iterrows():
            candle = Candle()
            candle.symbol = row['BANKNIFTY']
            candle.date = row['DATE']
            candle.time = row['TIME']
            candle.open = row['OPEN']
            candle.high = row['HIGH']
            candle.low = row['LOW']
            candle.close = row['CLOSE']
            candle.volume = row['VOLUME']


            one_minute_candles.append(candle)

        # Using asyncio to convert
        converted_candle = asyncio.run(convert_candles_to_timeframe(one_minute_candles))
        print(converted_candle)

        

        
        candle_json = json.dumps(converted_candle.to_dict(), indent=4)
        

        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))  
        file_name = f'{random_string}.json'

        
        with open(file_name, 'w') as file:
            file.write(candle_json)

       
        json_file = JsonFiles()
        with open(file_name, 'rb') as file:
            json_file.file.save(file_name, File(file))

        json_file.save()
        
        os.remove(file_name)

        
        response_data = {
            "success": True,
            "json_url": json_file.file.url
        }

        return JsonResponse(response_data)

    else:
        return render(request, 'MainApp/upload_csv.html')