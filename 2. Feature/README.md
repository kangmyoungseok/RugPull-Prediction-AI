# Feature의 도출
- 스캠코인과 정상코인의 구분을 위해서 크게 2가지 영역에 대해서 Feature를 도출한다.
+ __유동성 풀(Liquidity Pool)의 온체인 데이터__ 
+ __해당 토큰의 온체인 데이터__ 


## 1. Liquidity Pool Feature
 - 스캠이 발생하기 직전에 유동성 풀이 어떻게 변화하는지에 대해 분석한다.
 
 > ## Feature
 > 1. Mint / Burn / Swap 의 발생 횟수(Count)
 > 2. Mint / Burn / Swap 의 발생 비율(ratio)
 > 3. Mint / Burn / Swap 의 발생 분포(각각의 트랜잭션의 발생 분포 / Active Period)
 > 4. 유동성 풀의 지분 분포도(LP Token의 평균 , 분산)
 > 5. SwapIn/SwapOut 의 횟수 + 비율
 > 6. 유동성 풀 생성자(LP Creator)의 유동성 보유 비율  
 > 7. 유동성 풀 중 잠긴(Lock) 유동성의 비율


## 2. Token Feature
 - 토큰과 관련된 온체인 지표중 스캠코인과 관련된 지표를 분석한다.

 > ## Feature
 > 1. 해당 시점에 토큰의 Burn 비율
 > 2. 해당 시점에 개발자의 토큰 보유비율
 > 3. 해당 토큰의 개발자가 만든 다른 토큰의 수


## 3. FixTimeStamp
- 정상 데이터 파일에 대해서 TimeStamp를 1일로 변경해서 관련된 데이터를 다시 가져오는 코드들

## 4. Labeling
 + Labeling_to_Dataset.py 파일로 라벨링 파일에서 Dataset파일 변환 자동화    

<details>
<summary>Labeling 파일 버전 관리</summary>
<div markdown="1">
 
> - Labeling_v1.0.csv : 이전 Labeling 단계에서 가져온 파일
> - Labeling_v1.1.csv : False_data_timestamp.py , 정상 데이터의 TimeStamp를 구해서 'feature_timestamp' 열 추가
> - Labeling_v1.2.csv : 토큰의 Last Transaction이 30일 이후인 데이터들 정제했음. 이게 최종 Labeling Data
> - Labeling_v1.3.csv : False_data_timestamp.py , 정상 데이터의 TimeStamp를 7일로 변경
> - Labeling_v1.4.csv : TimeStamp_Feature.py , LP_Creator_address, LP_Creator_amount, LP_avg, LP_stdev, total_LP_amount 피처 추가
> - Labeling_v1.5.csv : Initial_supply.py , 초기 토큰을 받은 사람을 개발자로 정의. 초기 개발자와 초기 토큰 발행량을 찾음.
> -> 초기 개발자가 찾아지지 않는 경우(ABI문제)가 많아서 데이터 양이 많이 줄었음. 현재 약 18000개 pair
> - Labeling_v1.6.csv : Reduce_receiver.py, Receiver가 여러개의 주소인 경우 하나의 주소를 특정하여 개발자 주소로 바꿈. 600개 데이터 증발
> - Labeling_v1.7.csv : bitquery_feature.py, 현재 시점의 토큰의 양, TimeStamp시점의 유동성 풀 제공자의 LP Token의 양, TimeStamp시점의 개발자의 토큰 보유량 추가.
> - Labeling_v1.8.csv : etherscan_Feature.py, '현재 시점의 토큰의 양' 을 구해오는 로직에서 오류 수정해서 다시 뽑음
> - Labeling_v1.9.csv : 정상 TimeStamp를 1로 바꿔서 False 데이터들의 Feature를 전부 다시 구해서 수정.
> - Labeling_v1.10.csv : 정상과 스캠 토큰의 비율을 맞추기 위해서 임의로 정상 데이터들의 수를 조절
> - Labeling_v2.4.csv : 애매한 애들 정상으로 많이 넣고, 그거에 맞춰서 데이터들 다 다시 구함

</div>
</details>

<details>
<summary>Dataset 파일 버전 관리</summary>
<div markdown="1">

> - Dataset_v1.0.csv : Labeling_v1.8.csv 파일로 Dataset 만듦    
> - Dataset_v1.1.csv : Labeling_v1.9.csv 파일로 Dataset 만듦
> - Dataset_v1.2.csv : 정상 데이터와 스캠 비율 4:1로 맞춰서 다시 데이터셋
> - Dataset_v1.3.csv : 자잘한 오류 고쳐서 데이터 셋 -> 논문에 쓴 데이터셋
> - Dataset_v1.4.csv : Labeling_v2.4.csv / 새로 데이터셋 생성. Feature 수정 : Transaction_count_per_week
 - > 오류 : Burn Ratio 비율을 잘못해서 
 </div>
</details>


# Feature 도출 단계에서 발생한 Issue들
 1. ~~__정상__ 토큰들에서 많은 경우가 유니스왑풀을 개발자가 아닌, 사용자가 임의로 만든 풀인 경우가 있음. 이 부분에 대한 처리 어케하지~~ 
  -> 
 

