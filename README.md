# インストール
はじめにapacheのアクセスログを解析するモジュールであるapache-log-parserをインストールした。

```
$ pip install apache-log-parser
```

# apache-log-parser

apach-log-parserはアクセスログを解析するライブラリである。

```python
import apache_log_parser as ap
from pprint import pprint

dammy = '108.81.70.158 - - [16/Jun/2015:13:59:34 +0000] "GET /item/electronics/3717 HTTP/1.1" 200 86 "-" "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"' #ダミーデータ
log = ap.make_parser('%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"')
pprint(log(dammy))
'''
{'remote_host': '108.81.70.158',
 'remote_logname': '-',
 'remote_user': '-',
 'request_first_line': 'GET /item/electronics/3717 HTTP/1.1',
 'request_header_referer': '-',
 'request_header_user_agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.11 '
                              '(KHTML, like Gecko) Chrome/17.0.963.56 '
                              'Safari/535.11',
 'request_header_user_agent__browser__family': 'Chrome',
 'request_header_user_agent__browser__version_string': '17.0.963',
 'request_header_user_agent__is_mobile': False,
 'request_header_user_agent__os__family': 'Windows',
 'request_header_user_agent__os__version_string': 'Vista',
 'request_http_ver': '1.1',
 'request_method': 'GET',
 'request_url': '/item/electronics/3717',
 'request_url_fragment': '',
 'request_url_hostname': None,
 'request_url_netloc': '',
 'request_url_password': None,
 'request_url_path': '/item/electronics/3717',
 'request_url_port': None,
 'request_url_query': '',
 'request_url_query_dict': {},
 'request_url_query_list': [],
 'request_url_query_simple_dict': {},
 'request_url_scheme': '',
 'request_url_username': None,
 'response_bytes_clf': '86',
 'status': '200',
 'time_received': '[16/Jun/2015:13:59:34 +0000]',
 'time_received_datetimeobj': datetime.datetime(2015, 6, 16, 13, 59, 34),
 'time_received_isoformat': '2015-06-16T13:59:34',
 'time_received_tz_datetimeobj': datetime.datetime(2015, 6, 16, 13, 59, 34, tzinfo='0000'),
 'time_received_tz_isoformat': '2015-06-16T13:59:34+00:00',
 'time_received_utc_datetimeobj': datetime.datetime(2015, 6, 16, 13, 59, 34, tzinfo='0000'),
 'time_received_utc_isoformat': '2015-06-16T13:59:34+00:00'}
 '''
```
ここでホスト名と時間だけを抽出するよう関数を定義する。

```python
def read_log(log, parser='%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'):
    #host名と時間を取得
    line_parser = ap.make_parser(parser)
    log_line = line_parser(log)
    return [log_line['remote_host'], log_line['time_received_datetimeobj']]
```

#　複数ファイルの対応

複数ファイルの対応をするためにaccess_logが含まれるファイル名を全て抽出した。

```python
path = '/var/log/httpd/access_log*'
files = glob.glob(path)
```

# 時間帯の指定
開始時間と終了時間を指定した。

```python
start_time = datetime.datetime(1800, 1, 1, 0,0)
end_time = datetime.datetime(2200, 1,1,0,0,0) 
```
上の時間は（年、月、日、時、分、秒）の順である。そのため、開始時間終了時間を指定する場合はその順で変更が必要。

# 表

このような事前準備を元にアクセスログを時間及びホスト名を元に分類していく。
この表はcsvファイル（ファイル名：log_collection.csv）として保存した。
表は縦にホスト名で分類し、横には時間帯で分類した。
またホスト名で分類したとき、その並び順は総時間帯内でのアクセス数の大きい順にし、時間帯で分類したときは、時系列が古い順に並べてある。

また、時間帯は1時間毎に設定した。

```python
df = df.resample('H').sum()
# 3H:3時間毎、T：1分毎、D：1日毎、W：一週間毎、M:月毎
# W-MON：月曜はじめの一週間毎
```
このように設定を変えることで設定したい時間帯を変えられる。
