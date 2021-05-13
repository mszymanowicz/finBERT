import csv
import regex as re

file_path = "learning data.csv"
csv_read_file = open(file_path, mode='r', encoding='utf-8')
csv_reader = csv.reader(csv_read_file)
reworked_path = "reworked.csv"
csv_reworked_file = open(reworked_path, mode='w', encoding='utf-8',newline='')
csv_writer = csv.writer(csv_reworked_file)
for row in csv_reader:
    print(row[1])
    print("")
    if "BRIEF" in row[1]:
        continue
    added_spaces = re.finditer("[a-z][A-Z]", row[1])
    article_body = re.split("((\()+(\s*)+Reuters+(.*?).?(\)))", row[1])
    try:
        article_body = article_body[6]
    except:
        continue
    csv_writer.writerow([row[0], article_body[3:]],)
csv_read_file.close()
csv_reworked_file.close()
