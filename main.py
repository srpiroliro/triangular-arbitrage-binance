
msg={
    "method": "SUBSCRIBE",
    "params": [
        "!ticker@arr"
    ],
    "id": 1
}
"""
"""

base_url="wss://stream.binance.com:443/ws"

# import asyncio
# import websockets
# import json
# async def hello():
#     async with websockets.connect(base_url) as websocket:
#         await websocket.send(json.dumps(msg))
#         print(await websocket.recv())
    
# asyncio.run(hello())

# exit()

import websocket,json
# import rel

def on_message(ws, message):
    data=json.loads(message)
    print()

def on_error(ws, error):
    print("ERROR:",error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    ws.send(json.dumps(msg))

if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(base_url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    print("this")
    ws.run_forever()  # dispatcher=rel, reconnect=5 Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    print("this")
    # rel.signal(2, rel.abort)  # Keyboard Interrupt
    # rel.dispatch()
