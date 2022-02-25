from lib.Thegraph import *
from lib.FeatureLib import *

class Token:
    def __init__(self,token):
        self.id = token['id']
        self.symbol = token['symbol']
        self.name = token['name']
        self.txCount = token['txCount']
        self.totalLiquidity = token['totalLiquidity']
        self.decimals = token['decimals']

    def set_creator(self,creator):
        self.creator = creator
    
    def set_unlock_date(self,unlock_date):
        self.unlock_date = unlock_date


class Pair:
    def __init__(self,pair,token0,token1):
        self.id = pair['id']
        self.token0 = token0
        self.token1 = token1
        self.reserve0 = pair['reserve0']
        self.reserve1 = pair['reserve1']
        self.totalSupply = pair['totalSupply']
        self.reserveUSD = pair['reserveUSD']
        self.reserveETH = pair['reserveETH']
        self.txCount = pair['txCount']
        self.createdAtTimestamp = pair['createdAtTimestamp']
        self.cretedAtBlockNumber =  pair['createdAtBlockNumber']

    def setToken00(self):
        if(self.token0.symbol == 'WETH' ):
            self.token00 = self.token1
        else:
            self.token00 = self.token0

