import csv
import os

directory = "priced dir/"
files = os.listdir(directory)
full = []

for file in files:
    csv_file = open(directory + file, encoding='utf-8')
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        if len(row) == 0:
            continue
        full.append(row)
    csv_file.close()
    print(file)
csv_file = open('learning data.csv', mode='w', encoding='utf-8', newline='')
dialect = csv.Dialect
csv_writer = csv.writer(csv_file)
for row in full:
    csv_writer.writerow(row)
csv_file.close()
