with open("./data/raw_data_sta_10.txt", "r") as data_file, open("./data/cleaned_data_sta_10.txt", "w") as clean_file:
    for line in data_file:
        fields = line.split()
        
        if fields[0] == "YSI":
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