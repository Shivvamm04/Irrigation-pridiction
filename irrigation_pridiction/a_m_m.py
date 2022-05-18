
# from joblib import dump, load
# import numpy as np

# model = load('irrigation.joblib') 
# features = np.array([[40, 440, 39, 83, 0]])
# pred = model.predict(features)
# print(pred)

import time
from Adafruit_IO import Client, Feed, Data,RequestError

from joblib import dump, load
import numpy as np

ADAFRUIT_IO_KEY = 'aio_GCDg9655saFFanNEKrPMt9UqS5yc'
ADAFRUIT_IO_USERNAME = 'shivvamm'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

model = load('irrigation.joblib') #ML model

hum_threshold = 60
hum_val = 0

temp_threshold1 = 15
temp_threshold2 = 23
temp_val = 0

rain = aio.feeds('rain')
humidity = aio.feeds('humidity1')
temperature = aio.feeds('temperature1')
moisture = aio.feeds('soil')


# data = aio.receive(action.key)
# print('Retrieved value from Test has attributes: {0}'.format(data))
# print('Latest value from Test: {0}'.format(data.value))

# # Finally read the most revent value from feed 'Foo'.
# data = aio.receive(hitaction.key)
# print('Retrieved value from Foo has attributes: {0}'.format(data))
# print('Latest value from Foo: {0}'.format(data.value))

a=0
while(True):

    if(int(aio.receive(rain.key).value)==0):

        print(aio.receive(rain.key).value)
        hum_val = int(aio.receive(humidity.key).value)
        temp_val = int(aio.receive(temperature.key).value)
        mois_val = int(aio.receive(moisture.key).value)


        # model = load('irrigation.joblib') 
        features = np.array([[temp_val, 440, hum_val, mois_val, aio.receive(rain.key).value]])
        pred = model.predict(features)
        print(pred[0])
        aio.send_data('moter',1)
        time.sleep(pred[0])
        print("moter on")
        

        #  if(hum_val<hum_threshold):
            
            # if(a==0):
            #     time.sleep(0.1)
            #     aio.send_data('moter',1)
            #     a=1
            #     time.sleep(10)
            #     print("nooooooo")
            # print("moter on")
            
            # if(temp_val<temp_threshold1):
            #     hum_threshold = 75
            # if(temp_val>temp_threshold2):
            #     hum_threshold = 80
        #  else:
        #     time.sleep(0.1)
        #     aio.send_data('moter',0)
        #     a=0
        #     print("moter off")
        #     hum_threshold = 60
        #     time.sleep(10)
    else:
        time.sleep(0.1)
        aio.send_data('moter',0)
        a=0
        print("moter off due to rain")
        hum_threshold = 60
        time.sleep(10)
    
    
    
