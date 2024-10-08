import requests
import sys
import json
import datetime as dt
from pandas import DataFrame, merge
import matplotlib.pyplot as plt
'''
# 1.데이터 수집
url = 'http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
param = '?key={key}&targetDt={date}'
api_key = 'f5eef3421c602c6cb7ea224104795888'

# 빈 데이터 프레임
df = DataFrame()

for i in range(-7, 0):
    print('=', end='')  # 진행중 표시
    # 조회날짜 문자열 만들기
    # => 어제 날짜로 준비
    today = dt.datetime.now()
    delta = dt.timedelta(days=i)  # 오늘 기준으로 며칠 전 날짜 계산에 사용함
    day = today + delta
    # 문자열 서식 지정 => yyyymmdd 형식
    day_str = day.strftime('%Y%m%d')
    #print(day_str)
    #print('-'*20)

    # 최종 url 완성
    api_url = url+param.format(key=api_key,
                               date=day_str)
    #print(api_url)
    #print('-'*20)

    # 데이터 요청
    r = requests.get(api_url)

    if r.status_code != 200:
        print('[ERROR] %s' % r.status_code)
        #sys.exit(0)
        continue

    # json 데이터를 딕셔너리로 변경
    result = json.loads(r.text)
    #print(result)
    #print('-'*20)
    
    df_tmp = DataFrame(result['boxOfficeResult']['dailyBoxOfficeList'])
    df_tmp = df_tmp.filter(['movieNm', 'audiCnt'])
    #print(df_tmp)
    #print('-'*20)
    
    # movieNm는 인덱스로 변경하고 삭제, audiCnt는 날짜로 변경
    df_tmp = df_tmp.rename(index=df_tmp['movieNm'],
                           columns={'audiCnt':day_str})
    df_tmp = df_tmp.drop('movieNm', axis=1)
    #print(df_tmp)
    #print('-'*20)

    # 열 병합
    df = merge(df, df_tmp, left_index=True,
               right_index=True, how='outer')
    
print(df)
print('-'*20)   
'''

# 결측치 확인
print(df.isna().sum())
print('-'*20)  

# 결측치 nan 값 0으로 변경
df = df.fillna(0)
# 결측치 확인
print(df.isna().sum())
print('-'*20) 

# 관람객수를 정수로 변경
df = df.astype(int)

# 어제 날짜 가져오기
today = dt.datetime.now()
delta = dt.timedelta(days=-1)  
yesterday = today + delta
yesterday_str = yesterday.strftime('%Y%m%d')
#print(yesterday_str)
#print('-'*20) 

# 어제 날짜 기준 내림차순 정렬
df_r = df.sort_values(yesterday_str, ascending=False)
#print(df_r)
#print('-'*20)  

# 상위 5건 추출
df_r=df_r.head(5)
print(df_r)
print('-'*20) 

# 데이터 시각화
# 그래프 초기화
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] = 16
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['axes.unicode_minus'] = False

# 1) 막대 그래프
df_r.plot.bar(rot=0,fontsize=14)
plt.title('날짜별 관람객 빈도')
plt.ylabel('관객수')
plt.legend(loc='upper right')
plt.show()

# 2) 선 그래프
df_r.T.plot(fontsize=14,marker='X')
plt.title('일주일간의 영화별 관람객수 변화')
plt.grid()
plt.show()
