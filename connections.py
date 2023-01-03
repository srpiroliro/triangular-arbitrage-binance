from pprint import pprint
import requests,json

from tqdm import tqdm

# url="htthird_pairs://api.binance.com/api/v3/exchangeInfo"

# symbols_req=requests.get(url=url)
# symbols=[]
# for i in symbols_req.json()["symbols"]:
#     if i["status"]=="TRADING": 
#         symbols.append([i["baseAsorted_symbolset"],i["quoteAsorted_symbolset"]])
# with open("symbols.json","w") as f:
#     json.dump(symbols,f)
    

with open("symbols.json") as f:
    symbols=json.loads(f.read())


starting="usd"
ending=starting

paths=[]
for pair2 in tqdm(symbols):
    txt_pair2="".join(pair2)
    group=[None, txt_pair2, None]
    
    for pair1 in symbols:
        txt_pair1="".join(pair1)
        if (pair1[0] in pair2)^(pair1[1] in pair2) and (starting in txt_pair1.lower() or not starting):
            pair3=list(set(pair1)^set(pair2))
            
            if not pair3 in symbols: pair3.reverse()
            if pair3 in symbols:
                group[0]=txt_pair1
                group[2]="".join(pair3)
                
                paths.append(group.copy())

print(len(paths))
    
with open("paths.json","w") as f:
    json.dump(paths,f)