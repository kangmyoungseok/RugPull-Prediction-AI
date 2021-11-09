# 주어진 TimeStamp까지 Feature 구하기
 - 사용할 API : TheGraph / BitQuery
 - Feature를 구할 때, Input : Timestamp,Pairs / Output : Feature 형태로 함수를 만든다.
```
def get_feature1(pairs,Timestamp):
 ''' 
 API를 이용하여 데이터를 얻어오고
 데이터의 처리를 한다음
 '''
 return feature1
```

 - 정상 : 7일 이내
 - 스캠 : RugPull 발생 지점 직전까지

# Labeling 파일 버전 관리
- Labeling_v1.0.csv : 이전 Labeling 단계에서 가져온 파일
- Labeling_v1.1.csv : False_data_timestamp.py , 정상 데이터의 TimeStamp를 구해서 'feature_timestamp' 열 추가
- Labeling_v1.2.csv : 토큰의 Last Transaction이 30일 이후인 데이터들 정제했음. 이게 최종 Labeling Data
- Labeling_v1.3.csv : False_data_timestamp.py , 정상 데이터의 TimeStamp를 7일로 변경
- Labeling_v1.4.csv : TimeStamp_Feature.py , LP_Creator_address, LP_Creator_amount, LP_avg, LP_stdev, total_LP_amount 피처 추가
- Labeling_v1.5.csv : Initial_supply.py , 초기 토큰을 받은 사람을 개발자로 정의. 초기 개발자와 초기 토큰 발행량을 찾음.
-> 초기 개발자가 찾아지지 않는 경우(ABI문제)가 많아서 데이터 양이 많이 줄었음. 현재 약 18000개 pair
- Labeling_v1.6.csv : Reduce_receiver.py, Receiver가 여러개의 주소인 경우 하나의 주소를 특정하여 개발자 주소로 바꿈. 600개 데이터 증발
- 

# Feature 도출 단계에서 발생한 Issue들
 1. __정상__ 토큰들에서 많은 경우가 유니스왑풀을 개발자가 아닌, 사용자가 임의로 만든 풀인 경우가 있음. 이 부분에 대한 처리 어케하지
 2. 
