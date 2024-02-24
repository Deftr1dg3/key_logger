#!/usr/bin/env python3

import os
import sys
import struct
import asyncio
import aiofiles
import datetime
from pathlib import Path

this_dir = Path(__file__).parent.parent
sys.path.append(this_dir.__str__())

from settings import settings


class AsyncServer:
    def __init__(self, host: str, port: str | int):
        self._host = host
        self._port = port
    
    def _validate_file_path(self) -> Path:
        file_name = settings['data_file_name']
        dir_path = settings['data_dir_name']
        os.makedirs(dir_path, exist_ok=True)
        filepath = dir_path / file_name
        return filepath
        
        
    async def _save_data(self, data: bytes, writer: asyncio.streams.StreamWriter) -> None:

        filepath = self._validate_file_path()
        
        client_ip, client_port = writer.transport.get_extra_info('peername')
        date_time = datetime.datetime.now()
        
        prefix = ''.ljust(50, '-') + f'\n[{date_time}]\n[{client_ip}, {client_port}]\n'
        
        print(f'{prefix}\n{data.decode("utf-8")}\n')
        
        async with aiofiles.open(filepath, 'ab') as f:
            await f.write(prefix.encode('utf-8') + data + b'\n')
            
        print(f'SAVED TO -> {filepath}')
        
    async def _handle_data(self, reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter) -> None:
        file_size = struct.unpack('<L', await reader.read(4))[0]
        data = b''
        while file_size > 0:
            chunck = await reader.read(min(settings['chunck_size'], file_size))
            data += chunck 
            file_size -= len(chunck)
        await self._save_data(data, writer)

    async def run_server(self):
        server = await asyncio.start_server(self._handle_data, self._host, self._port)
        async with server:
            print(f'Server is listening on {self._host}:{self._port}')
            await server.serve_forever()
        
        
        
if __name__ == '__main__':
    s = AsyncServer(settings['host'], settings['port'])
    asyncio.run(s.run_server())
    # print(datetime.datetime.timestamp(datetime.datetime.now()))