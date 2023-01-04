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

with open("example.json") as f:
    prices={i["s"]:{"b":i["b"], "B":i["B"], "a":i["a"], "A":i["A"]} for i in json.loads(f.read())}

# starting=""
# ending=starting

# paths=[]
# for pair2 in tqdm(symbols):
#     txt_pair2="".join(pair2)
#     group=[None, txt_pair2, None]
    
#     for pair1 in symbols:
#         txt_pair1="".join(pair1)
#         if (pair1[0] in pair2)^(pair1[1] in pair2) and (starting in txt_pair1.lower() or not starting):
#             pair3=list(set(pair1)^set(pair2))
            
#             if not pair3 in symbols: pair3.reverse()
#             if pair3 in symbols:
#                 txt_pair3="".join(pair3)
                
#                 if ending in txt_pair3.lower() or not ending:
#                     # what do we have after each order?
#                     i1=list(set(pair1).intersection(pair2))[0]
#                     i2=list(set(pair2).intersection(pair3))[0]
#                     i3=list(set(pair3).intersection(pair1))[0]
                    
#                     """
#                         "b": "0.0024",      // Best bid price
#                         "B": "10",          // Best bid quantity
#                         "a": "0.0026",      // Best ask price
#                         "A": "100",         // Best ask quantity
#                     """
                    
#                     paths.append({
#                         "p1":txt_pair1,
#                         "p2":txt_pair2,
#                         "p3":txt_pair3,
#                         "profit":0,
#                         "orders":[ # 0-sell, 1-buy
#                             pair1.index(i3),
#                             pair2.index(i1),
#                             pair3.index(i2)
#                         ]
#                     })

# print(len(paths))
    
# with open("paths.json","w") as f:
#     json.dump(paths,f)

with open("paths.json") as f:
    paths=json.loads(f.read())


most_profitable=None
for path in paths:
    if all([ x in prices for x in [path["p1"],path["p2"],path["p3"]]]):
        pp1=prices[path["p1"]]
        pp2=prices[path["p2"]]
        pp3=prices[path["p3"]]
        o1,o2,o3=path["orders"]
        
        # 0-sell, 1-buy
        os=["b","a"]
        
        # operation 1:
        p1_result=float(pp1[os[o1]])**(1 if o1==0 else -1)
        p1_spent=1
        
        # operation 2:
        p2_result=p1_result*float(pp2[os[o2]])**(1 if o2==0 else -1)
        p2_spent=p1_result
        
        # operation 3:
        p3_result=p2_result*float(pp3[os[o3]])**(1 if o3==0 else -1)
        p3_spent=p2_result
        
        profit_perc=p3_result/p1_spent - 1
        path["profit"]=profit_perc
        
        if profit_perc>most_profitable["profit"]:
            most_profitable=path.copy()
        
paths.sort(key=lambda path: -path["profit"])