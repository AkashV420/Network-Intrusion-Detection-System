import asyncio
import websockets
import time
import json

async def produce(message: str, host: str, port: int) -> None:
	async with websockets.connect(f"ws://{host}:{port}") as ws:
		await ws.send(message)
		await ws.recv()

if __name__ == '__main__':
	msg = json.dumps({'Time': 1, 'Source': "Hello", 'Destination': "11", 'Protocol': 0, 'Transfer Rate': "qq", 'Avg Packet Size': "SS", 'Attack Type': "QQ"})
	for i in range(10):
		asyncio.run(produce(message=msg, host='localhost', port=4000))
