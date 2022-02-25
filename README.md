# RugPull Prediction AI Project

## 🔎 Overview
- 2021.09.01 ~ 2021.12.18 [BoB10기 2차프로젝트]
- This Project aim to Predict Rugpull in Uniswap which enables Investors to swap ERC-20 Tokens on Ethereum Blockchain
- We Collect 50000 Tokens Which listed on Uniswap V2, and all of the Transaction of the Tokens Using [The Graph API](https://thegraph.com/hosted-service/subgraph/uniswap/uniswap-v2), [Bitquery](https://graphql.bitquery.io/ide), [Etherscan API](https://docs.etherscan.io/), [Ethplorer API](https://github.com/EverexIO/Ethplorer/wiki/ethplorer-api)  



## 1. Labeling
- Total Data Input : __Tokens which are Listed in Uniswap V2__ (only ERC-20 Tokens That can be swap with WETH)
- Labeling all of the token Based on the Liquidity Pool's Change (if Rugpull Occurs, Liquidty Pool is Removed at once)


## 2. Feature Extraction
- For all of the Tokens which are Labeled True or False, get Feature until TimeLimit.  
- __TimeLimit?__
  +  Labeled True (Scam Token)
--> From first transcation timestamp to timestamp before Rugpull occur 
  +  Labeled False (Normal Token)
--> From first transcation timestamp to last traction timestamp




### Dataset Example

- Full Dataset is in **2. Feature/4. Labeling File**
- Total 18 Features, we used 20000 Tokens for AI Training

| id | Label | mint_count_per_week | burn_count_per_week | mint_ratio | swap_ratio | burn_ratio | mint_mean_period | swap_mean_period | burn_mean_period |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| 0xc45681eed9bea2a71cdcc1fa324a40f1d4617285 | True | 3.6242 | 0 | 0.666667 | 0.333333 | 0 | 0.264756 | 0.03685 | 0 |
| 0x3f759c3f4cdba32e69ddf607e0cdcc2547061b97 | FALSE | 43.13652027 | 14.77804309 | 0.123232845 |0.834549093 | 0 | 0.264756 | 0.03685 | 0 |    


### Training
- AI 모델 대충 설명 ?


How to Use?
----------------------
#### git clone
- download source code to local
```bash
git clone https://github.com/kangmyoungseok/RugPull_Prediction_AI
```

#### Requirements:

```bash
pip install -r requirements.txt
```

#### Launch predict.py
- **Note**: this python file require `--address` argument which specify Token's address
#### **Case 1**
- if Rugpull is already occured in this token, then print the Rugpull Event information. 
```py
$python3 predict.py --address 0xb73428a159a02a4b377e940d0919eb5ba91c67e7

[!] RUGPULL PREDICTION AI MODEL (MADE BY BOBAI)
[!] Github repo: https://github.com/kangmyoungseok/RugPull_Prediction_AI

[+] Successfully get information of token 0xb73428a159a02a4b377e940d0919eb5ba91c67e7

[*] RUGPULL IS ALREADY OCCRED IN THIS TOKEN
[*] EVENT TX_ID : 0x858e6c459d9b4e2f30bc6b06f28bd5397e4cb6d3d8199db5a42fb9e227016d9d
[*] AT TIME 2022-02-21 06:59:23
[*] RUGPULL IS DRIVEN BY swap TRANSACTION
[*] 'WETH' IN LIQUIDITY PULL IS DECREADED BY -99.99926340217542%
[*] Before WETH in Liquidity pool : 18.380953708929357370, After WETH : 0.000135393705157493
[*] See : https://etherscan.io/tx/0x858e6c459d9b4e2f30bc6b06f28bd5397e4cb6d3d8199db5a42fb9e227016d9d
```

#### **Case 2**


