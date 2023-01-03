import websocket,json

msg={"method": "SUBSCRIBE","params": ["!ticker@arr"],"id": 1}
base_url="wss://stream.binance.com:443/ws"

with open("paths.json") as f:
    paths=json.loads(f.read())

def on_message(ws, message):
    data=json.loads(message)
    if "result" in data: return
    
    prices={
        i["s"]:{"b":i["b"], "B":i["B"], "a":i["a"], "A":i["A"]}
        for i in data
    }
    mvp=paths[0]
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
            
            if profit_perc>mvp["profit"]:
                mvp=path.copy()
    if mvp["profit"]>0.005 or True:
        print(mvp["p1"],"->",mvp["p2"],"->",mvp["p3"])
        print(str(mvp["profit"])+"%\n")
    
    
def on_open(ws):
    print("# # # connection OPENED # # #")
    ws.send(json.dumps(msg))
def on_error(ws, error): print("ERROR:",error)
def on_close(ws, close_status_code, close_msg): print("# # # connection CLOSED # # #")
if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(base_url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.run_forever()
