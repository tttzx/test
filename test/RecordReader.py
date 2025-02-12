import aiofiles
import asyncio
import struct

class RecordReader:
    def __init__(self, filename, index_filename):
        self.filename = filename
        self.index_filename = index_filename
        self.index_map = {}

        # 读取索引文件并建立索引映射
        asyncio.create_task(self.load_index())

    async def load_index(self):
        """加载索引文件，构建索引映射"""
        async with aiofiles.open(self.index_filename, mode='r') as f:
            async for line in f:
                index, offset = line.strip().split()
                self.index_map[int(index)] = int(offset)

    async def read(self, index: int) -> bytes:
        """读取指定索引的记录"""
        if index not in self.index_map:
            raise ValueError("Index not found")

        offset = self.index_map[index]
        async with aiofiles.open(self.filename, mode='rb') as f:
            await f.seek(offset)
            length_bytes = await f.read(4)  # 读取长度字段
            if len(length_bytes) < 4:
                raise ValueError("Corrupted file: failed to read length")
            length = struct.unpack('I', length_bytes)[0]
            data = await f.read(length)
            if len(data) != length:
                raise ValueError("Corrupted file: record size mismatch")
            return data

    def __aiter__(self):
        """顺序读取文件中的所有记录"""
        async def iterate():
            async with aiofiles.open(self.filename, mode='rb') as f:
                index_items = list(self.index_map.items())  
                for index, offset in index_items:
                    await f.seek(offset)
                    length_bytes = await f.read(4)
                    if len(length_bytes) < 4:
                        break  # 文件结束
                    length = struct.unpack('I', length_bytes)[0]
                    data = await f.read(length)
                    if len(data) != length:
                        raise ValueError("Corrupted file: record size mismatch")
                    yield index, data
        return iterate()
