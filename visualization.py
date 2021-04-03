import matplotlib.pyplot as plt
import numpy as np

date = []
oxyLvl = []
clrs = []

f = open('./data/cleaned_data_sta_10.txt', 'r')
for row in f:
    row = row.split()
    
    if row[0] != "date":
        date.append(float(row[0]))
        oxyLvl.append(float(row[1]))
        if float(row[1]) <= 2:
            clrs.append('r')
        else:
            clrs.append('r')


plt.plot(date,oxyLvl, label="Oxygen level throughout year")
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