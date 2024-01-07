![server.py](https://github.com/otolaa/websocket_chat_example/blob/main/web/scrin.png "server.py")

![client_tui.py](https://github.com/otolaa/websocket_chat_example/blob/main/web/scrin_tui.png "client_tui.py")

![index.html](https://github.com/otolaa/websocket_chat_example/blob/main/web/scrin_web.png "index.html")

# websockets chat example
```
# start server
python3 server.py

# start client customtkinter
python3 client.py

# start client textual
python3 client_tui.py

# and start client JavaScript
index.html
```

## client tk
```
sudo apt-get install python3-tk
```

### dell python3 port
```
# <YOUR_PID> -> 3193 
lsof -i :3193
sudo kill -9 <YOUR_PID>
```