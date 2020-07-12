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
開始時間と終了時間を
