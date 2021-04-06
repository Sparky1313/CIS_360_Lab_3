import requests
import os.path
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


# FILE_URL = "https://www.glerl.noaa.gov/res/projects/ifyle/data/Mooring/ysi/2007/Y10.txt" # our actual file
FILE_URL = "https://www.glerl.noaa.gov/res/projects/ifyle/data/Mooring/ysi/2007/Y07.txt"
RAW_DATA_FILE = "./data/raw_data_sta_10.txt"
CLEANED_DATA_FILE = "./data/cleaned_data_sta_10.txt"

BASE_DATE = datetime(2007, 1, 1)

def time_thing(date):
    day = int(date) - 1
    currDatetime = BASE_DATE + timedelta(date - 1)
    
    if currDatetime.minute < 15:
        currDatetime = currDatetime.replace(minute=0, second=0, microsecond= 0)
    elif currDatetime.minute < 45:
        currDatetime = currDatetime.replace(minute=30, second=0, microsecond= 0)
    else:
        currHour = currDatetime.hour
        currDatetime = currDatetime.replace(hour=currHour + 1, minute=0, second=0, microsecond= 0)
    print(currDatetime)

def extract():
    #add in a try block
    req = requests.get(FILE_URL, allow_redirects = True)

    with open(RAW_DATA_FILE, "wb") as extract_file:
        extract_file.write(req.content)


def clean():
    with open(RAW_DATA_FILE, "r") as raw_file, open(CLEANED_DATA_FILE, "w") as clean_file:

        for line in raw_file:
            fields = line.split()

            if len(fields) == 0 or fields[0] == "YSI":
                continue
            elif fields[0] == "date":
                clean_file.write(fields[0] + "\t" + fields[4] + "\n")
            else:
                clean_file.write(fields[0] + "\t")
                dissolved_oxy = ""
                
                if fields[4] == "-999.000":
                    dissolved_oxy = "nan"
                elif float(fields[4]) < 0:
                    dissolved_oxy = "0.000"
                else:
                    dissolved_oxy = fields[4]
                
                clean_file.write(dissolved_oxy + "\n")


def visualize():
    dates = []
    oxy_lvls = []
    # clrs = []

    data_file = open(CLEANED_DATA_FILE, 'r')
    for row in data_file:
        row = row.split()
        
        if row[0] != "date":
            dates.append(float(row[0]))
            oxy_lvls.append(float(row[1]))
            # if float(row[1]) <= 2:
            #     clrs.append('r')
            # else:
            #     clrs.append('r')

    plt.plot(dates,oxy_lvls, label="Oxygen level throughout year")
    # plt.locator_params(axis="x", nbins=10)
    plt.ylim([0, 15])
    plt.xlim([199, 268])
    # plt.xticks(np.arange(199, 268, 5), rotation="vertical")
    plt.axhline(y=2, color='r', linestyle='-', label="Threshold for hypoxia")
    plt.xlabel('Day of Year (out of 365 days)', fontsize=12)
    plt.ylabel('Oxygen Levels (mg/L)', fontsize=12)

    plt.title('Oxygen Levels at Station 10 in 2007', fontsize=20)
    plt.legend()
    plt.show()


if not os.path.exists(RAW_DATA_FILE):
    extract()

if not os.path.exists(CLEANED_DATA_FILE):
    clean()

time_thing(200.1875)
time_thing(200.2083)
visualize()