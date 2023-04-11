import requests
import re
from bs4 import BeautifulSoup 
import time
import yfinance as yf
import datetime
import matplotlib.pyplot as plt

now = datetime.datetime.now()
current_time_1 = now.strftime("%H:%M:%S")
time.sleep(3)
now = datetime.datetime.now()  # call datetime.now() again to get a new time
current_time_2 = now.strftime("%H:%M:%S")

dt_format = '%H:%M:%S'  # format string for datetime objects
time_1 = datetime.datetime.strptime(current_time_1, dt_format)
time_2 = datetime.datetime.strptime(current_time_2, dt_format)
time_diff = time_2 - time_1
seconds_diff = int(time_diff.total_seconds())  # get total number of seconds
print(seconds_diff)