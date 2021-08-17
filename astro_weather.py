import requests
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import json
from datetime import datetime, timedelta
import calendar

#getting_location
user_location = input("Where will you be stargazing? ")
api_url = 'http://api.positionstack.com/v1/forward?'
payload = {
    "access_key" : 'bdb5594a0e0f750a4aaeeb3509a8ff17',
    "query" : user_location,
    "timezone_module":1
}

response = requests.get(api_url, params=payload)
status_code = response.status_code
if status_code == 200: 
  response_data = response.json()
  location_data = response_data['data']
  location_dict = location_data[0]
  user_lat = round(location_dict.get('latitude'), 3)
  user_lon = round(location_dict.get('longitude'), 3)
  user_loc = str(user_lat )+ ',' + str(user_lon)
  timezone_dict = location_dict.get('timezone_module')
  user_tz_offset = timezone_dict.get('offset_string')
  user_tz = timezone_dict.get('name')
  user_lon_lat = str(user_lon) + "," + str(user_lat)
  locality = location_dict.get('region_code')
  city = location_dict.get('name')
  city_state = city + ", "+ locality
else:
  print(f"Unsucessful request: {status_code}, {response.text}")

#astro_data
astro_payload = f"lon={user_lon}&lat={user_lat}&product=astro&output=json"
api_url = f"http://www.7timer.info/bin/api.pl?{astro_payload}"

astro_response = requests.get(api_url)
response_data = response.json()
weather_data = pd.read_json(api_url)

#getting_time
api_key = '5b9f79efc0a9403c8cf3d3301c420a1e'
time_url = "https://timezone.abstractapi.com/v1/current_time?"

time_payload = {
    "api_key" : '5b9f79efc0a9403c8cf3d3301c420a1e',
    "location" : user_loc,
}

response = requests.get(time_url, params=time_payload)
time_data = (response.content).decode("utf-8") 
time_dict = json.loads(time_data)

if status_code == 200:
  response_data = response.json()
else:
  print(f"Unsucessful request: {status_code}, {response.text}")

class WhatTimeIsIt:

  def __init__(self):
    self.first_index = 0
    self.second_index = 1
    self.third_index = 2
    self.colon = ":"
    self.dash = "-"

  def get_time(self, time_info):
    self.time_info = time_info
    
    time_date_string = time_dict['datetime']
    time_date_list = time_date_string.split()
    time_hr_min_sec = time_date_list[self.second_index]
    just_nums_list = time_hr_min_sec.split(self.colon)
    hr_min = int(just_nums_list[self.first_index]+just_nums_list[self.second_index])
    return hr_min

  def get_hour(self, time_info):
    self.time_info = time_info
   
    time_date_string = time_dict['datetime']
    time_date_list = time_date_string.split()
    time_hr_min_sec = time_date_list[self.second_index]
    just_nums_list = time_hr_min_sec.split(self.colon)
    hr = int(just_nums_list[self.first_index])
    
    return hr

  def time_of_day(self, time_input):

    self.morning = range(600, 1200)
    self.afternoon = range(1201, 1800)
    self.evening = range(1801, 2400)
    self.evening_after_midnight = range(0,599)
    self.curr_time_of_day = []
    if time_input in self.morning:
      self.curr_time_of_day.append("morning")
    elif time_input in self.afternoon:
      self.curr_time_of_day.append("afternoon")
    elif time_input in self.evening:
      self.curr_time_of_day.append("evening")
    elif time_input in self.evening_after_midnight:
      self.curr_time_of_day.append('evening')

    self.curr_time_of_day.append(time_input)
    return self.curr_time_of_day

clock = WhatTimeIsIt()
nums = clock.get_time(time_dict)
when = clock.time_of_day(nums)
hour = clock.get_hour(time_dict)

#getting_day

class WhatDayIsIt(WhatTimeIsIt):
  
  def GetDate(self, time_info):
    self.time_info = time_info
    time_date_string = time_dict['datetime']
    time_date_list = time_date_string.split()
    date = time_date_list[self.first_index]
    just_nums_list = date.split(self.dash)
    day = int(just_nums_list.pop())
    month = int(just_nums_list.pop())
    year = int(just_nums_list.pop())
    year_month_day = (year , month , day)
    
    return year_month_day

  def findDayofWeek(self, date):
    self.date = date
    day_of_week = datetime(date[0],date[1],date[2]).strftime("%A")
    return day_of_week


def daydayday():
  dayDates = []
  today = datetime.now()
  for i in range(0,4):
    day = today + timedelta(days=i)
    day_str = str(day)
    
    time_date_list = day_str.split()
    date = time_date_list[0]
    just_nums_list = date.split('-')
    day = int(just_nums_list.pop())
    month = int(just_nums_list.pop())
    year = int(just_nums_list.pop())
    year_month_day = (year , month , day)
    day_of_week = datetime(year_month_day[0],year_month_day[1],year_month_day[2]).strftime("%A")
    dayDates.append(day_of_week)
  return dayDates

cal = WhatDayIsIt()
date = cal.GetDate(time_dict)
day = cal.findDayofWeek(date)

#create_forecast
if hour > 18:
  diff = hour + (2 * (21 - hour))
elif hour <= 18:
  diff = 18 - hour

print(diff)

if diff == 0:
  new_diff = 0
elif diff < 3:
  new_diff = 3
elif diff > 3:
  new_diff = (round(diff/3)) * 3
  
 class WhenToStarGaze(WhatTimeIsIt):
  isin_list = []
  nine_hours = 9
  thirty_three_hours = 33
  fifty_seven_hours = 57
  fifteen_hours = 15

  def create_list(self, input_diff):
    self.isin_list.append(input_diff)
    for curr_diff in self.isin_list:
      curr_diff+=3
      if curr_diff >= 72:
        break
      elif curr_diff == self.isin_list[self.first_index] + self.nine_hours:
        jump = curr_diff + self.fifteen_hours
        self.isin_list.append(jump)
      elif curr_diff == self.isin_list[self.first_index] + self.thirty_three_hours:
        jump = curr_diff + self.fifteen_hours
        self.isin_list.append(jump)
      elif curr_diff == self.isin_list[self.first_index] + self.fifty_seven_hours:
        jump = curr_diff + self.fifteen_hours
        self.isin_list.append(jump)
      else:
        self.isin_list.append(curr_diff)
      
    if self.isin_list[len(self.isin_list)-1] > 72:
      self.isin_list.pop() 

    if self.isin_list[0] == 0:  
      self.isin_list.pop(0)

    return self.isin_list

list_of_times = WhenToStarGaze()
curr_time_list=list_of_times.create_list(new_diff)

daylabel_AMPM = []
for curr_diff in curr_time_list:
  x = hour + curr_diff
  if x <= 12:
    list_day = dayDates[0]
    time = x
    y = str(time) + "AM " + list_day
    daylabel_AMPM.append(y)
  elif x < 24 and x > 12:
    list_day = dayDates[0]
    time = x - 12
    if time == 0:
      time = 12
    y=str(time) +"PM "+ list_day
    daylabel_AMPM.append(y)
  elif x >= 24 and x < 36:
    list_day = dayDates[1]
    time = x - 24
    if time == 0:
      time = 12
    y=str(time) +"AM "+ list_day
    daylabel_AMPM.append(y)
  elif x >= 36 and x < 48:
    list_day = dayDates[1]
    time = x - 36
    if time == 0:
      time = 12
    y=str(time) +"PM "+ list_day
    daylabel_AMPM.append(y)
  elif x >= 48 and x < 60:
    list_day = dayDates[2]
    time = x-48
    if time == 0:
      time = 12
    y=str(time) +"AM "+ list_day
    daylabel_AMPM.append(y)
  elif x >= 60 and x < 72:
    list_day = dayDates[2]
    time = x-60
    if time == 0:
      time = 12
    y=str(time) +"PM "+ list_day
    daylabel_AMPM.append(y)
  elif x >= 72 and x < 84:
    list_day = dayDates[3]
    time = x-72
    if time == 0:
      time = 12
    y=str(time) +"AM "+ list_day
    daylabel_AMPM.append(y)
  elif x >= 84 and x < 96:
    list_day = dayDates[3]
    time = x-84
    if time == 0:
      time = 12
    y=str(time) +"AM "+ list_day
    daylabel_AMPM.append(y)
