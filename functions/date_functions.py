import datetime as dt

now = dt.datetime.now()
year = now.year
month = now.month
day = now.day
day_of_week = now.weekday()  #  0 = Monday , 1 = Tuesday , 2= Wednesday  etc . 
hour = now.hour
print(now)
print(f"{year}\n{month}\n{day}\n{day_of_week}")


# creating a date time object 
##  create The datatime object by passing the year , month, day    ###tip -  - hh mm ss can be passed but have "00" as default , example below
date_of_birth  = dt.datetime(year = 1986, month = 6, day = 27 ) 
print(date_of_birth)

