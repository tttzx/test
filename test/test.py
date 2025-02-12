import asyncio
import os
from time import time
from RecordReader import RecordReader
from RecordWriter import RecordWriter

async def test_advanced_operations():
    # 设置文件路径
    data_file = "test_records.db"
    index_file = "test_records.index"

    # 删除旧文件，确保测试环境干净
    if os.path.exists(data_file):
        os.remove(data_file)
    if os.path.exists(index_file):
        os.remove(index_file)

    # 创建 RecordWriter 和 RecordReader
    writer = RecordWriter(data_file, index_file, buffer_size=3)
    reader = RecordReader(data_file, index_file)

    # 创建一些测试数据
    test_data = [f"record_{i}".encode() for i in range(10)]


    # 写入数据
    start_time = time()
    await writer.append_batch(test_data)
    await writer.close()  # 确保所有数据写入完成
    print(f"Data written in {time() - start_time:.4f} seconds")

    # 读取数据
    start_time = time()
    async for index, data in reader:
        print(f"Read index {index}: {data.decode()}")
    print(f"Data read in {time() - start_time:.4f} seconds")

    # 模拟损坏文件（删除最后一个记录）
    print("Simulating corrupted file...")
    with open(data_file, 'r+b') as f:
        f.seek(-len(test_data[-1]), os.SEEK_END)
        f.truncate()  # 删除最后一个记录

    # 尝试读取已损坏的文件
    try:
        print("Attempting to read corrupted file...")
        async for index, data in reader:
            print(f"Read index {index}: {data.decode()}")
    except Exception as e:
        print(f"Error reading corrupted file: {e}")


# 运行高级测试用例
asyncio.run(test_advanced_operations())