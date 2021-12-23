# RugPull Prediction AI Project

## 🔎 Overview
- 2021.09.01 ~ 2021.12.18 [BoB10기 2차프로젝트]
- This Project aim to Predict Rugpull in Uniswap which enables Investors to swap ERC-20 Tokens on Ethereum Blockchain
- We Collect 50000 Tokens Which listed on Uniswap V2, and all of the Transaction of the Tokens Using [The Graph API](https://thegraph.com/hosted-service/subgraph/uniswap/uniswap-v2), [Bitquery](https://graphql.bitquery.io/ide), [Etherscan API](https://docs.etherscan.io/), [Ethplorer API](https://github.com/EverexIO/Ethplorer/wiki/ethplorer-api)  



## 1. Labeling
> - Total Data Input : __Tokens which are Listed in Uniswap V2__ (only ERC-20 Tokens That can be swap with WETH)
> - Labeling all of the token Based on the Liquidity Pool's Change (if Rugpull Occurs, Liquidty Pool is Removed at once)


## 2. Feature Extraction
> - For all of the Tokens which are Labeled True or False, get Feature until TimeLimit.  
> - __TimeLimit?__
> > 1. Labeled True (Scam Token)
> > --> From first transcation timestamp to timestamp before Rugpull occur 
> > 2. Labeled False (Normal Token)
> > --> From first transcation timestamp to last traction timestamp


<details>
<summary> 📌 Dataset Example ( Total 18 Features )</summary>
<div markdown="1">


| id | Label | mint_count_per_week | burn_count_per_week | mint_ratio | swap_ratio | burn_ratio | mint_mean_period | swap_mean_period | burn_mean_period |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| 0xc45681eed9bea2a71cdcc1fa324a40f1d4617285 | True | 3.6242 | 0 | 0.666667 | 0.333333 | 0 | 0.264756 | 0.03685 | 0 |

</div>
</details>

# 3. 학습

# 💀진행하면서 에러 사항
 11.08 
 - 정상 데이터들의 TimeStamp를 30일로 하면, 지금 뽑은 피처들이 스캠 데이터랑 편차가 너무 큼. 확실히 초기 토큰들은 스캠으로 분류될거 같긴한데... 너무 전부 스캠으로 분류 될거 같아서 바꿈
 - Feature를 뽑다보면 별에별 에러가 다 나옴. 현재 Labeling_v1.2가 최종이라고 했는데, Feature를 뽑으면서 에러 나는것들 그냥 삭제시키기로 함. 갯수 줄어들 듯 
 - Feature를 뽑고 보니, 각각의 Feature를 보면 상위 1~2%정도는 지우는게 학습에 좋아보임.. 라벨링이 잘못된 경우도 있는거 같고 너무 튀는 애들이 좀 있음.


# 추후 진행 사항
- 현재 정상으로 라벨링한 데이터들이 __너무 정상__ 인 상황. 너무 정상인 애들과 너무 스캠인 애들이 라벨링 된걸로 학습을 시키니까 정확도가 100퍼가 나오지..
- 정상 라벨링 중, 너무 Official한 애들은 제외한다.(경향성이 너무 커지기 때문) -> TxCount를 기준으로 하던.. Token이 생성된 날짜가 20.05이전이면 그것도 삭제. 특성이 다름
- 시간나면 날잡고 데이터 셋 다시 첨부터 구해봐야 겠다
