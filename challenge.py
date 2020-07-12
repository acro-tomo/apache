import pandas as pd
import apache_log_parser as ap
import glob
import csv
import datetime

def read_log(log, parser='%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'):
    #host名と時間を取得
    line_parser = ap.make_parser(parser)
    log_line = line_parser(log)
    return [log_line['remote_host'], log_line['time_received_datetimeobj']]

path = '/var/log/httpd/access_log*'
files = glob.glob(path)#accesslogのファイル全てをリスト化

start_time = datetime.datetime(1800, 1, 1, 0,0)
end_time = datetime.datetime(2200, 1,1,0,0,0) #Startとendの時間を便宜的に設定

for file in files:
    with open(file, 'r') as f:
        lines = f.readlines()
    lines = [i.rstrip('\n') for i in lines]

    host_and_time = []#host名と時間のリスト
    hosts = set()#host名のリスト（重複なし）
    for i in lines:
        host, time = read_log(i)
        if start_time <= time <= end_time:
            host_and_time.append([host, time])
            hosts.add(host)

    title = list(hosts) 
    data = dict()
    dates = []#列名を時間帯に配置する
    sum_row = [0] * len(hosts)
    for a, i in enumerate(host_and_time):
        zero = [0] * len(hosts)
        index = title.index(i[0])
        zero[index] = 1
        sum_row[index] += 1
        dates.append(i[1])
        data[a] = zero
    data[a+1] =sum_row#最後の行にhost別の合計を挿入
    dates.append(datetime.datetime(1800, 1, 1, 0,0,0))#最後の行の列名を便宜的に設定
    dates = pd.to_datetime(dates)#pandasのdatetimeに型変換
    df=pd.DataFrame(list(data.values()), index=dates, columns=title)
    df = df.sort_values(df.index[-1],axis=1, ascending=False)#アクセスの多い順にソート
    df = df[:-1]
    df = df.sort_index()#時間を早い順にソート
    
    df = df.resample('H').sum() #1時間帯に分ける
    # 3H:3時間毎、T：1分毎、D：1日毎、W：一週間毎、M:月毎
    # W-MON：月曜はじめの一週間毎


    df.to_csv('log_collection.csv')
