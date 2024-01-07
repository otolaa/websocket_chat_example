"""
//textual.textualize.io/guide/widgets/#loading-indicator
"""
import asyncio
import websockets
from random import randrange as rr
from textual import on
from textual.containers import Grid
from textual.app import App, ComposeResult
from textual.widgets import Input, TextArea, Button, Header, Footer

port_ = 3193
us_ = f"user_tui_{rr(0, 100)}"
ws = f"ws://127.0.0.1:{port_}/{us_}"

class MyApp(App):

    TITLE = "TUI_client_0.0.2"

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    CSS = """
        Grid { grid-size: 4 4; grid-gutter: 1 2; }
        #p1 { column-span: 4; row-span: 3; }
        #p2 { column-span: 3; row-span: 1; }
        #p3 { column-span: 1; row-span: 1; width:95%; }
    """

    async def on_load(self) -> None:
        self.interval = 1/120
        asyncio.create_task(self.update_ws())

    async def update_ws(self):    
        async with websockets.connect(ws, ping_interval=None) as websocket:
            try:
                self.ws = websocket
                async for message in websocket:
                    tts = self.query_one(TextArea)
                    tts.insert(f"{message}\n")
            except websockets.exceptions.ConnectionClosedOK as e:
                print(e, sep=' / ')

    def compose(self) -> ComposeResult:       

        yield Header(show_clock=True)    

        with Grid():
            yield TextArea(language="python", id="p1")
            yield Input(placeholder="Message here...", id="p2")
            yield Button("Send message", variant="success", id="p3")

        yield Footer()

    @on(Button.Pressed)
    async def button_click(self, event: Button.Pressed):
        asyncio.create_task(self.send_message())

    @on(Input.Submitted)
    async def input_submitted(self, event: Input.Submitted):       
        asyncio.create_task(self.send_message())

    async def send_message(self) -> None:
        input = self.query_one(Input)
        if len(input.value):
            await self.ws.send(input.value)
            input.value = ""

if __name__ == "__main__":
    app = MyApp()
    app.run()