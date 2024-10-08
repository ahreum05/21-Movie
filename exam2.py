import requests
import sys
import json
import datetime as dt
from pandas import DataFrame
import matplotlib.pyplot as plt
'''
# 1) 데이터 수집
url = 'http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
param = '?key={key}&targetDt={date}'
api_key = '331d3820194d5d8c9e32b68724a4aa9b'
# 조회날짜 문자열 만들기
# => 어제 날짜로 준비
today = dt.datetime.now()
delta = dt.timedelta(days=-1) # 오늘 기준으로 며칠 전 날짜 계산에 사용
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
    print('[ERROR]%s'%r.status_code)
    sys.exit(0)

# 데이터 확인    
print(r.text)
print('-' * 20)

# 딕셔너리 변경 "" -> ''로 변경됌
result = json.loads(r.text)
print(result)
print('-' * 20)

# 데이터 전처리
df = DataFrame(result['boxOfficeResult']['dailyBoxOfficeList'])   
print(df)
print('-' * 20)
'''
# 영화명, 관객수 컬럼 추출
df = df.filter(['movieNm','audiCnt'])
print(df)
print('-' * 20)

df_r = df.rename(columns={'audiCnt':'관람객'})
print(df_r)
print('-' * 20)

df_r = df_r.set_index('movieNm')
print(df_r)
print('-' * 20)

# 관람객 자료형 확인
print(df_r.dtypes)
print('-' * 20)

# 관람객 데이터를 정수로 변경
df_r['관람객'] = df_r['관람객'].astype(int)
print(df_r.dtypes)
print('-' * 20)

# 데이터 시각화
# 그래프 초기화
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] = 16
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['axes.unicode_minus'] = False

df_r.plot.barh()
plt.gca().invert_yaxis() 
plt.legend(loc='lower right')
plt.title('20240529 박스오피스 순위')
plt.ylabel('')
plt.grid()
plt.show()








