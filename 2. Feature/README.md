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

 - 정상 : 30일 이내
 - 스캠 : RugPull 발생 지점 직전까지

# Labeling 파일 버전 관리
- Labeling_v1.0.csv : 이전 Labeling 단계에서 가져온 파일
- Labeling_v1.1.csv : False_data_timestamp.py , 정상 데이터의 TimeStamp를 구해서 'feature_timestamp' 열 추가
- Labeling_v1.2.csv : 토큰의 Last Transaction이 30일 이후인 데이터들 정제했음. 이게 최종 Labeling Data
