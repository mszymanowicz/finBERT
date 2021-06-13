import os
import csv
import dateparser
from dateutil.relativedelta import relativedelta
import time
import datetime
import pandas as pd

example_query = "https://query1.finance.yahoo.com/v7/finance/download/GME?period1=1573689600&period2=1620000000&interval=1d&events=history&includeAdjustedClose=true"


def close_date_frame(data_frame, date):
    if len(data_frame.loc[data_frame['Date'] == str(date)]) != 0:
        return data_frame.loc[data_frame['Date'] == str(date)]
    elif len(data_frame.loc[data_frame['Date'] == str(date + relativedelta(days=1))]) != 0:
        return data_frame.loc[data_frame['Date'] == str(date + relativedelta(days=1))]
    elif len(data_frame.loc[data_frame['Date'] == str(date - relativedelta(days=1))]) != 0:
        return data_frame.loc[data_frame['Date'] == str(date - relativedelta(days=1))]
    elif len(data_frame.loc[data_frame['Date'] == str(date + relativedelta(days=2))]) != 0:
        return data_frame.loc[data_frame['Date'] == str(date + relativedelta(days=2))]
    elif len(data_frame.loc[data_frame['Date'] == str(date - relativedelta(days=2))]) != 0:
        return data_frame.loc[data_frame['Date'] == str(date - relativedelta(days=2))]
    else:
        return []


def labeler(price_article, price_future, positive_margin, negative_margin):
    diff_percent = ((price_future - price_article) / price_article) * 100
    return diff_percent
    # if diff_percent > positive_margin:
    #     return 'positive'
    # elif diff_percent < -negative_margin:
    #     return 'negative'
    # else:
    #     return 'neutral'


def query_maker(asset_name, begin_date, ending_date):
    return str(
        f"https://query1.finance.yahoo.com/v7/finance/download/{asset_name}?period1={int(time.mktime(begin_date.timetuple()))}&period2={int(time.mktime(ending_date.timetuple()))}&interval=1d&events=history&includeAdjustedClose=true")


file_list = [fi for fi in os.listdir("./dir/") if fi.endswith('.csv')]

files = [["./dir/"+file, os.path.getsize("./dir/"+file)] for file in file_list if os.path.getsize("./dir/"+file) > 0]

files.sort(key=lambda file: file[1], reverse=True)

da_curated_dir = './priced dir/'
dates = []
for file in files:
    if file[0] == "other-listed_csv.csv" or file[0] == "nasdaq-listed-symbols_csv.csv" or file[
        0] == "nyse-listed_csv.csv":
        continue
    asset = (os.path.splitext(file[0])[0]).split("/")[-1]
    csv_file = open(file[0], encoding='utf-8')
    csv_reader = csv.reader(csv_file)
    curated_csv = []
    end_date = (datetime.date.today() - relativedelta(months=3, days=1))
    for row in csv_reader:
        if len(row) == 0:
            continue
        row[2] = dateparser.parse(row[2])
        if ~isinstance(type(row[2]), datetime.datetime):
            row[2] = row[2].date()
        if row[2] > end_date:
            continue
        curated_csv.append(row)
    print(f"{asset} - {len(curated_csv)}")
    if len(curated_csv) == 0:
        continue
    backup = curated_csv
    curated_csv.sort(key=lambda csv_row: csv_row[2], reverse=True)
    start_date = curated_csv[-1][2]
    try:
        prices_df = pd.read_csv(query_maker(asset, start_date, datetime.date.today() + relativedelta(days=1)))
        prices_df['Date'] = prices_df['Date'].apply(lambda date: dateparser.parse(str(date)))
    except:
        continue
    csv_file = open(da_curated_dir + f"{asset}.csv", mode='w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    for row in curated_csv:
        price_at_article = close_date_frame(prices_df, row[2])
        price_at_future = close_date_frame(prices_df, (row[2] + relativedelta(months=3)))
        if len(price_at_article) == 0 or len(price_at_future) == 0:
            continue
        label = labeler(float(price_at_article['Adj Close']), float(price_at_future['Adj Close']), 20, 5)
        article = ''
        for paragraph in range(3, len(row)):
            article += " " + row[paragraph]
        csv_writer.writerow([label, article])
    csv_file.close()
    zero = 0
