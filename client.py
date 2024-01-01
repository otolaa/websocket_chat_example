''' client websockets chat '''
import asyncio
from tkinter import *
import customtkinter as CTk
import websockets
from random import randrange as rr

CTk.set_appearance_mode("dark")  # Modes: system (default), light, dark
CTk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

port_ = 3193
us_ = f"client_send_message_{rr(0, 100)}"
ws = f"ws://127.0.0.1:{port_}/{us_}"

class App(CTk.CTk):
    def __init__(self, loop, interval=1/120):
        super().__init__()
        self.loop = loop
        self.protocol("WM_DELETE_WINDOW", self.close)        
        self.tasks = []     
        self.tasks.append(loop.create_task(self.updater(interval)))
        self.tasks.append(loop.create_task(self.insert_textbox(interval)))       
        
        self.title('Client_0.0.1')
        self.resizable(False, False)

        for c in range(1): self.columnconfigure(index=c, weight=1)
        for r in range(2): self.rowconfigure(index=r, weight=1)

        self.textbox = CTk.CTkTextbox(master=self, width=400)
        self.textbox.grid(row=0, column=0, ipadx=9, ipady=9, padx=(9, 9), pady=(9, 0), sticky="nsew")

        # 2 frame block row=1 column=0
        self.message_frame = CTk.CTkFrame(master=self, fg_color="transparent")
        self.message_frame.grid(row=1, column=0, padx=(9, 9), pady=(9, 9), sticky="nsew")

        self.entry_message = CTk.CTkEntry(master=self.message_frame, width=350)
        self.entry_message.bind("<Return>", command=lambda event:self.tasks.append(self.loop.create_task(self.click_async(interval))))
        self.entry_message.grid(row=0, column=0, padx=(0, 9))

        self.btn_message = CTk.CTkButton(
            master=self.message_frame, 
            text="<<", width=50, 
            command=lambda: self.tasks.append(self.loop.create_task(self.click_async(interval)))
            )
        self.btn_message.grid(row=0, column=1, padx=(4, 0))

    async def insert_textbox(self, interval):    
        async with websockets.connect(ws, ping_interval=None) as websocket:
            try:
                self.ws = websocket
                async for message in websocket:
                    self.textbox.insert(END, f"{message}\n")
                    # print(message, sep=' / ', end='\n')
            except websockets.exceptions.ConnectionClosedOK as e:
                print(e, sep=' / ')

    async def updater(self, interval):
        while True:
            self.update()
            await asyncio.sleep(interval)
    
    async def click_async(self, interval):
        m_t_ = self.entry_message.get()
        await self.ws.send(m_t_)
        self.entry_message.delete(0, END)
    
    def close(self):
        self.ws.close()
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = App(loop)
    loop.run_forever()
    loop.close()