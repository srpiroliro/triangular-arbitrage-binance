# Triangular Arbitrage Binance

## Disclaimer
This version **ignores volume** completly, meaming the returned profit rates aren't real/sustainable. 

## What it does?
> Arbitrage: the simultaneous buying and selling of securities, currency, or commodities in different markets or in derivative forms in order to take advantage of differing prices for the same asset.

> Triangular Arbitrage: Triangular arbitrage is the result of a discrepancy between three foreign currencies that occurs when the currency's exchange rates do not exactly match up.

In this case, we are going to scan for triangular arbitrage opportunities on Binance. 

Firstly by creating all possible combinations/paths of triangular arbitrage opportunities. 
And later on, each second check the price of each pair and calculate the final profit.


## How to use:
1. install python websoceket-client library `pip3 install websocket-client`
2. clone this reposoitory `git clone INSERT_REPOSITORY_URL_HERE`
3. got into the cloned repository folder
4. run `arbitrage.py` -> `python3 arbitrage.py`
