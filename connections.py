from pprint import pprint
import requests,json

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

def is_equal(p1,p2)->bool:
    return (p1[0]==p2[0] and p1[1]==p2[1]) or (p1[0]==p2[1] and p1[1]==p2[0])

# CHECK: is this necesorted_symbolsary?
sorted_symbols={}
for pair in symbols:
    for x in pair:
        if x in sorted_symbols: 
            sorted_symbols[x].append(pair)
        else: sorted_symbols[x]=[pair]

starting=""

paths=[]
for pair in symbols:
    base,quote=pair # middle part

    for first_pair in sorted_symbols[base]:
        if not is_equal(pair,first_pair) and (not starting or starting in first_pair):
            base1,quote1=first_pair
            for third_pair in sorted_symbols[quote1]:
                if quote in third_pair and (not starting or starting in third_pair) and not is_equal(third_pair,first_pair) and not is_equal(third_pair,pair):
                    paths.append(["".join(first_pair),"".join(pair),"".join(third_pair)])
    
    for first_pair in sorted_symbols[quote]:
        if not is_equal(pair,first_pair) and (not starting or starting in first_pair):
            base1,quote1=first_pair
            for third_pair in sorted_symbols[quote1]:
                if base in third_pair and (not starting or starting in third_pair) and not is_equal(third_pair,first_pair) and not is_equal(third_pair,pair):
                    paths.append(["".join(first_pair),"".join(pair),"".join(third_pair)])

print(len(paths))
# for path in paths:
#     print(" - ".join(path))
    
with open("paths.json","w") as f:
    json.dump(paths,f)