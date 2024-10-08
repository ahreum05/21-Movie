import requests
import sys
import json
import datetime as dt
from pandas import DataFrame

# 1. 데이터 수집
url = 'http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
param = '?key={key}&targetDt={date}'
api_key = 'f5eef3421c602c6cb7ea224104795888'
# 조회날짜 문자열 만들기
# => 어제 날짜로 준비
today = dt.datetime.now()
delta = dt.timedelta(days= -1)  # 오늘 기준으로 며칠 전 날짜 계산에 사용
yesterday = today + delta
# yyyymmdd 형식
yesterday_str = yesterday.strftime('%Y%m%d')
print(yesterday_str)
print('-' * 20)

# 최종 url 완성
api_url = url + param.format(key=api_key, 
                             date=yesterday_str)
print(api_url)
print('-' * 20)

# 데이터 요청
r = requests.get(api_url)

if r.status_code != 200 :
    print('[ERROR] %s' %r.status_code)
    sys.exit(0)
    
# 데이터 확인
print(r.text)    
print('-' * 20)

# 딕셔너리 변경
result = json.loads(r.text)
print(result)    
print('-' * 20)

# 2. 데이터 전처리
df = DataFrame(result['boxOfficeResult']['dailyBoxOfficeList'])
print(df)    
print('-' * 20)







