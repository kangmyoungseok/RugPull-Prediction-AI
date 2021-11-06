# Labeling
Uniswap Token들 수집 후 라벨링

## 1. 데이터의 수집 (Pair.py)
 - [TheGraph API](https://thegraph.com/hosted-service/subgraph/uniswap/uniswap-v2, "thegraph link")를 이용하여, 2020 년 5월 Uniswap v2에 유동성 풀을 생성한 5만여개의 토큰쌍을 모두 가져온다.
 - 가져오는 항목은 아래의 쿼리를 통해 유동성 풀에 대한 정보/ 유동성 풀에 존재하는 각각의 토큰에 대한 정보를 가져온다.
```{
pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: desc) {
   id
   token0{
    id
    symbol
    name
    txCount
    totalLiquidity
  }
   token1{
    id
    symbol
    name
    txCount
    totalLiquidity
  }
   reserve0
   reserve1
   totalSupply
   reserveUSD
   reserveETH
   txCount
   createdAtTimestamp
   createdAtBlockNumber
 }
}
```

- 실행 결과 
```json
{
  "data": {
    "pairs": [
      {
        "createdAtBlockNumber": "13559693",
        "createdAtTimestamp": "1636156718",
        "id": "0xb84e4624df93acc5705cea41f5793bbc8217e4c7",
        "reserve0": "4.469344505437440958",
        "reserve1": "304883.483603199",
        "reserveETH": "8.938689010874881915999999999999999",
        "reserveUSD": "39993.08998211250734223008028635412",
        "token0": {
          "id": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
          "name": "Wrapped Ether",
          "symbol": "WETH",
          "totalLiquidity": "520059.167074018835841431",
          "txCount": "59649166"
        },
        "token1": {
          "id": "0xc629674f0331c32923b0b77c592200c0e5b770ef",
          "name": "Tanjiro",
          "symbol": "Tanjiro",
          "totalLiquidity": "304883.483603199",
          "txCount": "78"
        },
        "totalSupply": "0.036742346141746671",
        "txCount": "78"
      }
    ]
  }
}

```
## 2. 데이터의 라벨링(Labeling.py)
 - TheGraph API를 이용하면 각각의 Pair에 대해 **Mint/Swap/Burn**의 모든 트랜잭션을 가져올 수 있다.
 ###  2.1 라벨링 로직
  + 정상     
     __정상인 토큰들은 하나의 조건으로 정상인지 아닌지 판단할 수 없다.__     
     * txCount, 토큰의 마지막 트랜잭션이 발생한 날짜, 유동성 풀 이더의 변화량, 현재 남아있는 이더의 양, 유동성 풀의 마지막 트랜잭션 날짜 등을 종합적으로 고려하여 정상인지 판단한다. ( False 데이터 9212 -> 2700개 정도로 추려짐 )  
  + 스캠    
    __러그풀이 발생했는지에 대한 유무는 유동성 풀을 보고 판단 가능하다.__
    * 초기 유동성 풀 크기에 비해 현재 유동성 풀이 99%이상 감소한 경우에 대해서, 아래의 두가지 타입(Burn,Swap)에 대한 검사를 하여 러그풀이 발생했는지 탐지한다.
    - Burn RugPull : 토큰의 유동성 풀을 추적하여, Burn Transaction으로 인해서 유동성 풀이 한번에 99%이상 사라진 경우 RugPull로 탐지
    - Swap RugPull : 토큰의 유동성 풀을 추적하여, Swap Transaction으로 인해서 유동성 풀이 한번에 99%이상 사라진 경우 RugPull로 탐지
      - 단) Swap RugPull의 탐지에 경우 단순히 Swap Transaction으로 인해서 유동성 풀의 감소를 탐지한 경우, MEV봇들의 시세조작 행위들이 탐지가 되었다. 따라서 MEV 봇들과 실제 러그풀을 구분하기 위해서 Swap Transaction으로 들어오는 토큰의 양이 초기 유동성 풀의 토큰 대비 5배 이상 들어온 경우만 Swap RugPull로 탐지했다.
 ### 2.2 라벨링 결과
 |  | 스캠 | 정상 |이외 |
 ---|:---:|:---:|---:
 갯수 | 34052 | 2700 | 6512
 비율 | 78.7% | 6.2% | 15.1%
 
 
 + 전체 43264 Uniswap Pair에 대해서 34052(78.7%)개가 러그풀 발생. 나머지 9212개 중 2700개가 정상

## 3. 라벨링된 데이터의 정제(Cleansing.py)
- 스캠으로 라벨링된 데이터중 학습에 쓰이기 부적합한 데이터들을 제외 시킨다.
  - 1. TxCount가 너무 작은(<5)인 데이터들 삭제
  - 2. 러그풀 발생까지의 시간이 너무 작은(<1h) 데이터들 삭제
    - 결과 : 34052 -> 19985 
### + 최종 학습 데이터
 |  | 스캠 | 정상 
 ---|:---:|:---:
 갯수 | 19985 | 2700 
 비율 | 88.1% | 11.9% 
 
## 4. 최종 라벨링 결과 파일(Labeling_v1.0.csv)



 
