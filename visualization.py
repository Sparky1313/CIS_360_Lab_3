import matplotlib.pyplot as plt

date = []
oxyLvl = []

f = open('./data/cleaned_data_sta_10.txt', 'r')
for row in f:
    row = row.split()
    
    if row[0] == "date":
        continue
    date.append(row[0])
    oxyLvl.append(float(row[1]))

plt.hist(oxyLvl, bins=len(oxyLvl))

plt.xlabel('Date', fontsize=12)
plt.ylabel('Oxygen Levels', fontsize=12)

plt.title('Oxygen Levels over a Year', fontsize=20)
plt.legend()
plt.show()