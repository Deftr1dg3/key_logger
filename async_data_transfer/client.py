import struct
import asyncio


class AsyncClient:
    def __init__(self, host: str, port: str | int):
        self._host = host 
        self._port = port 
        self._reader = None 
        self._writer = None
        
    async def send_data(self, data: bytes):
        self._reader, self._writer = await asyncio.open_connection(self._host, self._port)
        
        file_size = len(data)
        
        file_size = struct.pack('<L', file_size)
        
        self._writer.write(file_size)
        await self._writer.drain()
        
        self._writer.write(data)
        await self._writer.drain()
    
    async def close(self):
        if self._writer is not None:
            self._writer.close()
            await self._writer.wait_closed()
        # print('Connection closed')
        


