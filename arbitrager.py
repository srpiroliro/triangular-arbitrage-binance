import websocket,json,requests,time

def get_symbols():
    symbols_req=requests.get(url="https://api.binance.com/api/v3/exchangeInfo")
    symbols=[]
    for i in symbols_req.json()["symbols"]:
        if i["status"]=="TRADING": 
            symbols.append([i["baseAsset"],i["quoteAsset"]])
    return symbols
def make_paths(symbols,starting=""):
    ending=starting

    paths=[]
    for pair2 in symbols:
        for pair1 in symbols:
            txt_pair1="".join(pair1)
            i1=list(set(pair1).intersection(pair2))
            if len(i1)==1 and (starting in txt_pair1.lower() or not starting): #(pair1[0] in pair2)^(pair1[1] in pair2)
                pair3=list(set(pair1)^set(pair2))
                
                if not pair3 in symbols: pair3.reverse()
                if pair3 in symbols:
                    txt_pair3="".join(pair3)
                    
                    if ending in txt_pair3.lower() or not ending:
                        # what do we have after each order?
                        i2=list(set(pair2).intersection(pair3))[0]
                        i3=list(set(pair3).intersection(pair1))[0]
                        
                        paths.append({
                            "p1":txt_pair1,
                            "p2":"".join(pair2),
                            "p3":txt_pair3,
                            "profit":0,
                            "orders":[ # 0-sell, 1-buy
                                pair1.index(i3),
                                pair2.index(i1[0]),
                                pair3.index(i2)
                            ]
                        })
    return paths

def on_message(ws, message):
    global sub_start,cnt
    
    if cnt==target: ws.close()
    else: cnt+=1
    
    data=json.loads(message)
    if "result" in data: return
    
    prices={
        i["s"]:{"b":i["b"], "B":i["B"], "a":i["a"], "A":i["A"]}
        for i in data
    }
    mvp=paths[0]
    # start=time.perf_counter()
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
            # p2_spent=p1_result
            
            # operation 3:
            p3_result=p2_result*float(pp3[os[o3]])**(1 if o3==0 else -1)
            # p3_spent=p2_result
            
            profit_perc=p3_result/p1_spent - 1
            path["profit"]=profit_perc
            
            if profit_perc>mvp["profit"]: mvp=path
    # print(f"took {time.perf_counter()-start}seconds")
        
    if mvp["profit"]>output_x_profits:
        found=time.time()
        took=found-sub_start
        sub_start=found
        
        p=[mvp["p1"],mvp["p2"],mvp["p3"]]
        # print("->".join(p))
        # print(str(mvp["profit"]*100)+"%\n")
        # print(f"took {took}seconds to find.")
        
        findings.append([found, p, mvp["profit"]])
        time_it.append(took)
def on_open(ws):
    global sub_start
    print(f"# # # connection to \"{BASE_URL}\" OPENED # # #")
    ws.send(json.dumps({"method": "SUBSCRIBE","params": ["!ticker@arr"],"id": 1}))
    sub_start=time.time()
# def on_error(ws, error): print("ERROR:",error)
def on_close(ws, close_status_code, close_msg): 
    print(f"# # # connection to \"{BASE_URL}\" CLOSED # # #")


BASE_URL="wss://stream.binance.com:443/ws"

symbols=None
paths=None

cnt=0

start_counter=time.time()
sub_start=0
findings=[]
time_it=[]

# output all profits wich are bigger than `output_x_profits`
output_x_profits=0.005 # 0.5%
starting="usd"
target=20000

if __name__ == "__main__":
    print("getting symbols...")
    symbols=get_symbols()
    print(f"got {len(symbols)} symbols\n")

    print("generating paths...")
    paths=make_paths(symbols,starting)
    print(len(paths),"paths were generated!\n")

    try:
        ws=websocket.WebSocketApp(BASE_URL,
                                on_open=on_open,
                                on_message=on_message,
                                # on_error=on_error,
                                on_close=on_close)
        ws.run_forever()
    except Exception as e: print("stopped!")
    finally:
        stop_counter=time.time()
        print(f"\ntook {stop_counter-start_counter} seconds\n")
        
        print(f"got {len(findings)} profits bigger than {output_x_profits*100}%: ")
        for fi in findings:
            print(f"\t{round(fi[2]*100, 4)}%   [{' -> '.join(fi[1])}]") 
        
        if time_it:
            print(f"\ntook on avarage: {round(sum(time_it)/len(time_it), 4)}sec")