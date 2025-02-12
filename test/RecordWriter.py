import os
import struct
import aiofiles
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

class RecordWriter:
    def __init__(self, filename, index_filename, buffer_size=1024):
        self.filename = filename
        self.index_filename = index_filename
        self.buffer_size = buffer_size
        self.lock = threading.Lock()
        self.index_counter = 0  # 初始索引
        self.buffer = []  # 缓冲区
        self.executor = ThreadPoolExecutor(max_workers=4)  # 多线程池，4个工作线程

        # 读取现有索引文件，获取最后的索引
        asyncio.create_task(self.load_index_counter())

    async def load_index_counter(self):
        """加载现有索引文件，获取最后一个索引值"""
        if os.path.exists(self.index_filename):
            async with aiofiles.open(self.index_filename, mode='r') as f:
                lines = await f.readlines()
                if lines:
                    last_line = lines[-1]
                    last_index, _ = last_line.strip().split()
                    self.index_counter = int(last_index) + 1  # 递增索引

    async def append(self, data: bytes) -> int:
        """异步写入单条记录"""
        length = len(data)
        index = self.index_counter

        # 将数据添加到缓冲区
        self.buffer.append((index,length, data))

        if len(self.buffer) >= self.buffer_size:
            await self.flush_buffer()  # 如果缓冲区满了，刷新写入磁盘

        # 更新索引计数
        self.index_counter += 1
        return index

    async def append_batch(self, batch: list) -> list:
        """异步写入多条记录"""
        indices = []
        for data in batch:
            index = await self.append(data)
            indices.append(index)
        return indices

    async def flush_buffer(self):
        """刷新缓冲区，将数据写入文件"""
        with self.lock:
            # 使用线程池进行批量写入
            await asyncio.get_event_loop().run_in_executor(self.executor, self._write_buffer)

    def _write_buffer(self):
        """实际写入文件的操作（同步）"""
        with open(self.filename, 'ab') as f, open(self.index_filename, 'a') as idx_f:
            for index,length, data in self.buffer:
                record = struct.pack('I', length) + data
                f.write(record)
                idx_f.write(f"{index} {f.tell() - len(record)}\n")
        self.buffer.clear()  # 清空缓冲区

    async def close(self):
        """关闭并确保缓冲区数据被写入"""
        if self.buffer:
            await self.flush_buffer()
        await asyncio.sleep(0)  # 保证所有异步任务完成
