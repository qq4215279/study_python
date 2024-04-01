# encoding: utf-8

import websocket

# WebSocket服务器的URL地址
url = "ws://example.com/your_endpoint"


def on_message(ws, message):
    print("Received Message:", message)


def on_error(ws, error):
    print("Error:", error)


def on_close(ws):
    print("Connection Closed")


def on_open(ws):
    # 连接建立时触发的函数
    ws.send("Hello Server!")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
