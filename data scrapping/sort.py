import csv
import regex as re
import os

if not os.path.exists("reworked.csv"):
    csv_reader = csv.reader(open('learning data.csv', mode='r', encoding='utf-8'))

    database = []

    for row in csv_reader:
        database.append(row)

    database.sort(key=lambda entry: float(entry[0]))

    database_repaired = []
    csv_writer = csv.writer(open("reworked.csv", mode='w', newline='', encoding='utf-8'))
    for row in database:
        if "BRIEF" in row[1]:
            continue
        added_spaces = re.finditer("[a-z][A-Z]", row[1])
        article_body = re.split("((\()+(\s*)+Reuters+(.*?).?(\)))", row[1])
        try:
            article_body = article_body[6]
        except:
            continue
        article_body = re.sub(r'(?<=[A-z][.,])(?=[^\s])', r' ', article_body[3:])
        database_repaired.append([row[0], article_body])
        csv_writer.writerow([row[0], article_body])
    database = database_repaired
else:
    csv_reader = csv.reader(open("reworked.csv", mode='r', encoding='utf-8'))
    database = []
    for row in csv_reader:
        database.append(row)

negative = -15
neutral_negative = 5
neutral_positive = 11
positive = 20

neg = []
neut = []
pos = []

for item in database:
    item[0] = float(item[0])
    if item[0] < negative:
        neg.append(item)
    elif item[0] < neutral_negative:
        continue
    elif item[0] < neutral_positive:
        neut.append(item)
    elif item[0] < positive:
        continue
    else:
        pos.append(item)

print("Negative: " + str(len(neg)))
print("Neutral: " + str(len(neut)))
print("Positive: " + str(len(pos)))

csv_result = csv.writer(open("sorted.csv", mode='w', encoding='utf-8'))
csv_result.writerows(neg)
csv_result.writerows(neut)
csv_result.writerows(pos)
