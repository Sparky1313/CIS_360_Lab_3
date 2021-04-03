with open("./data/raw_data_sta_10.txt", "r") as data_file, open("./data/cleaned_data_sta_10.txt", "w") as clean_file:
    for line in data_file:
        fields = line.split()
        
        if fields[0] == "YSI":
            continue
        elif fields[0] == "date":
            for field in fields:
                clean_file.write(field + "\t")
            clean_file.write("\n")
        else:
            for field in fields:
                if float(field) < 0:
                    clean_file.write("0.00\t")
                else:
                    clean_file.write(field + "\t")
            clean_file.write("\n")