''' server websockets '''
import asyncio
import http
import websockets
import sys

all_ws = set()

async def health_check(path, request_headers):
    if path == "/healthz":
        return http.HTTPStatus.OK, [], b"OK\n"

async def send_ws(message: str):
    dell_ws = []
    for websocket in all_ws:
        try:
            try:
                await websocket.send(message)
            except websockets.exceptions.ConnectionClosedOK as e:
                dell_ws.append(websocket)
                print("send_message", e, sep=' / ', end='\n')
        
        except Exception as e:
            dell_ws.append(websocket)
            print("send_ws", sys.exc_info()[1], len(all_ws), len(dell_ws), sep=' / ')
    
    if len(dell_ws) > 0:
        list(map(all_ws.remove, dell_ws))

async def echo(websocket, path:str): 
    try:
        print("[+] new client commect!", path, sep=' / ')
        await websocket.send(f'[+] welcome in chat: {path.replace("/", "")} - this your nic.')
        all_ws.add(websocket)

        async for message in websocket:
            try:
                print("[+] message from client", message, sep=' / ')
                await send_ws(message)
            
            except websockets.exceptions.ConnectionClosedOK as e:
                print('echo', e, sep=' / ', end='\n')
    
    except Exception as e:
        print(sys.exc_info()[1], len(all_ws), sep=' / ')

async def start_server():
    await websockets.serve(echo, "127.0.0.1", 3193, ping_timeout=None, ping_interval=None, process_request=health_check)

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(start_server())
    event_loop.run_forever()