import requests
import os.path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime, timedelta


STA_7_FILE_URL = "https://www.glerl.noaa.gov/res/projects/ifyle/data/Mooring/ysi/2007/Y07.txt"
STA_7_RAW_DATA_FILENAME = "./data/raw_data_sta_7.txt"
STA_7_CLEANED_DATA_FILENAME = "./data/cleaned_data_sta_7.txt"

STA_10_FILE_URL = "https://www.glerl.noaa.gov/res/projects/ifyle/data/Mooring/ysi/2007/Y10.txt"
STA_10_RAW_DATA_FILENAME = "./data/raw_data_sta_10.txt"
STA_10_CLEANED_DATA_FILENAME = "./data/cleaned_data_sta_10.txt"

STA_11_FILE_URL = "https://www.glerl.noaa.gov/res/projects/ifyle/data/Mooring/ysi/2007/Y11.txt"
STA_11_RAW_DATA_FILENAME = "./data/raw_data_sta_11.txt"
STA_11_CLEANED_DATA_FILENAME = "./data/cleaned_data_sta_11.txt"

FILE_URLS = [STA_7_FILE_URL, STA_10_FILE_URL, STA_11_FILE_URL]
RAW_FILENAMES = [STA_7_RAW_DATA_FILENAME, STA_10_RAW_DATA_FILENAME, STA_11_RAW_DATA_FILENAME]
CLEANED_FILENAMES = [STA_7_CLEANED_DATA_FILENAME, STA_10_CLEANED_DATA_FILENAME, STA_11_CLEANED_DATA_FILENAME]


BASE_DATE = datetime(2007, 1, 1)


def extrd_and_clned_chk(url, raw_filename, cleaned_filename):
    if not os.path.exists(raw_filename):
        extract(url, raw_filename)

    if not os.path.exists(cleaned_filename):
        clean(raw_filename, cleaned_filename)


def time_thing(date):
    day = int(date) - 1
    currDatetime = BASE_DATE + timedelta(date - 1)
    
    if currDatetime.minute < 15:
        currDatetime = currDatetime.replace(minute=0, second=0, microsecond= 0)
    elif currDatetime.minute < 45:
        currDatetime = currDatetime.replace(minute=30, second=0, microsecond= 0)
    else:
        currHour = currDatetime.hour
        currDatetime = currDatetime.replace(hour=currHour + 1,\
             minute=0, second=0, microsecond= 0)
    return (currDatetime)

def extract(url, raw_filename):
    #add in a try block
    req = requests.get(url, allow_redirects = True)

    with open(raw_filename, "wb") as extracted_file:
        extracted_file.write(req.content)


def clean(raw_filename, cleaned_filename):
    with open(raw_filename, "r") as raw_file,\
         open(cleaned_filename, "w") as cleaned_file:

        for line in raw_file:
            fields = line.split()

            if len(fields) == 0 or fields[0] == "YSI":
                continue
            elif fields[0] == "date":
                cleaned_file.write(fields[0] + "\t" + fields[4] + "\n")
            else:
                cleaned_file.write(fields[0] + "\t")

                # Measured in mg/L
                dis_oxy = fields[4]
                
                # A reading of -999.000 indicates a missing measurement given by the documentation describing the data.
                # We decided to allow for a calibration error of 1.000 mg/L after looking through the data.  So if the levels
                # of dissolved oxygen are below -1.000 mg/L we decided that the reading was bad and indicated a calibration error.
                # Also, judging from the research we did, a dissolved oxygen concentration of above 20 mg/L should
                # be extremely rare in a lake if not impossible.  Most sensors won't read above 20 mg/L, so we
                # added an extra 1 mg/L to that limit to account for calibration errors.  Anything above that we viewed as bad data.
                if dis_oxy == "-999.000" or float(dis_oxy) < -1.000 or float(dis_oxy) > 21.000:
                    dis_oxy = "nan"

                # Negative values are not physically possible so we assume that it is 0 mg/L.
                elif float(fields[4]) < 0:
                    dis_oxy = "0.000"
                
                # Use the actual reading since it is a good reading.
                else:
                    dis_oxy = fields[4]
                
                cleaned_file.write(dis_oxy + "\n")


def visualize(cleaned_filenames):
    dates = []
    oxy_lvls = []
    sta_num = [7, 10, 11]
    clrs = ['b', 'g', 'm']
    i = 0

    for filename in cleaned_filenames:
        data_file = open(filename, 'r')
        dates.append([])
        for row in data_file:
            row = row.split()
            
            if row[0] != "date":
                test = time_thing(float(row[0]))
                dates[i].append(test)
                oxy_lvls.append([])
                oxy_lvls[i].append(float(row[1]))
         
        
        plt.plot(dates[i], oxy_lvls[i], color=clrs[i], label="Station " + str(sta_num[i]))
        i += 1
    # plt.locator_params(axis="x", nbins=10)
    plt.ylim([0, 20])

    plt.xticks(rotation=40)
    plt.subplots_adjust(bottom=0.2)
    plt.axhline(y=2, color='r', linestyle='-', label="Threshold for hypoxia")
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Oxygen Levels (mg/L)', fontsize=12)

    plt.title('Oxygen Levels at Stations in 2007', fontsize=20)
    plt.legend()
    plt.show()


i = 0

while i < len(FILE_URLS):
    extrd_and_clned_chk(FILE_URLS[i], RAW_FILENAMES[i], CLEANED_FILENAMES[i])
    i += 1


# time_thing(200.1875)
# time_thing(200.2083)
visualize(CLEANED_FILENAMES)
