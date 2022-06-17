# RugPull Prediction AI Project

## 🔎 Overview
- 2021.09.01 ~ 2021.12.18 [Korea Education Program KITRI BOB 10th project, Team BOBAI]
- This Project aim to Predict Rugpull in Uniswap which enables Investors to swap ERC-20 Tokens on Ethereum Blockchain
- We Collect 50000 Tokens Which listed on Uniswap V2, and all of the Transaction of the Tokens from [The Graph API](https://thegraph.com/hosted-service/subgraph/uniswap/uniswap-v2), [Bitquery](https://graphql.bitquery.io/ide), [Etherscan API](https://docs.etherscan.io/), [Ethplorer API](https://github.com/EverexIO/Ethplorer/wiki/ethplorer-api)  



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

| id | Label | mint_count_per_week | burn_count_per_week | mint_ratio | swap_ratio | burn_ratio | mint_mean_period | swap_mean_period | burn_mean_period |..|token_creator_holding_ratio|
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0xc45681eed9bea2a71cdcc1fa324a40f1d4617285 | True | 3.6242 | 0 | 0.666667 | 0.333333 | 0 | 0.264756 | 0.03685 | 0 |..|0.130261666|
| 0x3f759c3f4cdba32e69ddf607e0cdcc2547061b97 | FALSE | 43.13652027 | 14.77804309 | 0.123232845 |0.834549093 | 0 | 0.125160144 | 0.194190522 | 0.179786452 |..| 0.043933532 |   



# How to Use?

### git clone
- download source code to local
```bash
git clone https://github.com/kangmyoungseok/RugPull_Prediction_AI
```

### Requirements:

```bash
pip install -r requirements.txt
```

### Launch predict.py
- **Note**: this python file require `--address` argument which specify Token's address.
- Use `-v` for detail information
- **Constraints**
    + Token in Ethereum only(ERC-20)
    + Token must have Liquidity Pool in Uniswap v2(Not v3) 
    + Token which is Traded **only** with WETH 

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
[*] 'WETH' IN LIQUIDITY PULL IS DECREASED BY -99.99926340217542%
[*] Before WETH in Liquidity pool : 18.380953708929357370, After WETH : 0.000135393705157493
[*] See : https://etherscan.io/tx/0x858e6c459d9b4e2f30bc6b06f28bd5397e4cb6d3d8199db5a42fb9e227016d9d
```

#### **Case 2**
- if Rugpull is not occured in this token, then print **probability** of rugpull with our ai model.
- in this case, use option `-v` for detail info
 
```py
$python3 predict.py --address 0x888680deda2a1a53c1d93bfae591b93ca1f83bec -v

[!] RUGPULL PREDICTION AI MODEL (MADE BY BOBAI)
[!] Github repo: https://github.com/kangmyoungseok/RugPull_Prediction_AI

[+] Successfully get information of token 0x888680deda2a1a53c1d93bfae591b93ca1f83bec

[+] RUGPULL IS NOT OCCURED IN THIS TOKEN YET.
[+] START COLLECING DATA FOR RUGPULL PREDICTION

[!] Alert!! Token's lock will be expired soon. Be careful regardless of AI Score
[!] Lots of Rugpull occur after Token's Lock is expired

[Pair Info] https://etherscan.io/token/0x3bf9f467d9017d03dc83ec152c7f559757bccb59
[Pair Info] Uniswap Pair Address : 0x3bf9f467d9017d03dc83ec152c7f559757bccb59
[Pair Info] Liquidity Pool's Reserved : 1.3449332624476922Eth
[Pair Info] Liquidity Pool's Lock Ratio : 0
[Pair Info] Liquidity Pool's Lock Expiration Date : 2022-02-22 02:00:00

[Token Info] https://etherscan.io/token/0x888680deda2a1a53c1d93bfae591b93ca1f83bec
[Token Info] Token Creator : 0x6344f90ddec1e57de4dd170b620391a22bd3584c
[Token Info] Swap In(buy token with Ether) count : 273
[Token Info] Swap Out(Sell Token) count : 136
[+] Probabiliy of Rugpull is : 15.53%
[+] Our AI indicate this token is Safe
```

# Video
https://user-images.githubusercontent.com/33647663/155699528-8aaf7c09-11dd-4cd2-b1c5-e0bdec1c6004.mp4



https://user-images.githubusercontent.com/33647663/155700780-af0c217b-d5a4-48d6-b2fc-44dd5e1f36a9.mp4


