import requests
import os.path
import time

def extract():
    #add in a try block

    if not os.path.exists("./data/raw_data_sta_10.txt"):
        url = "https://www.glerl.noaa.gov/res/projects/ifyle/data/Mooring/ysi/2007/Y10.txt"
        req = requests.get(url, allow_redirects = True)

        with open("./data/raw_data_sta_10.txt", "wb") as extract_file:
            extract_file.write(req.content)
        
    else:
        print("cool")

def clean():
    with open("./data/raw_data_sta_10.txt", "r") as data_file, open("./data/cleaned_data_sta_10.txt", "w") as clean_file:

        # data_file.seek(0)
        for line in data_file:
            fields = line.split()

            # time.sleep(5)

            if len(fields) == 0 or fields[0] == "YSI":
                continue
            elif fields[0] == "date":
                clean_file.write(fields[0] + "\t" + fields[4] + "\n")
            else:
                clean_file.write(fields[0] + "\t")

                dissolved_oxy = ""
                
                if fields[4] == "-999.000":
                    dissolved_oxy = "Missing"
                elif float(fields[4]) < 0:
                    dissolved_oxy = "0.000"
                else:
                    dissolved_oxy = fields[4]
                
                clean_file.write(dissolved_oxy + "\n")

extract()
clean()