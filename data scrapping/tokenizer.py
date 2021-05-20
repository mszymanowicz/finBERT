import csv
import re
import nltk
from nltk import word_tokenize, WordNetLemmatizer, PunktSentenceTokenizer
from nltk.tokenize import MWETokenizer

file_csv = "reworked.csv"
file = open(file_csv, mode='r', encoding='utf-8')
csv_reader = csv.reader(file)
tokenizer = nltk.tokenize.RegexpTokenizer('\w+|\$[\d\.]+|\S+')

for row in csv_reader:
    row[1] = re.sub(r'(?<=[A-z][.,])(?=[^\s])', r' ', row[1])
    text = row[1]
    zero = 0
