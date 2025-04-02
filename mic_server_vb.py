import asyncio
import websockets
import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
INPUT_CHANNELS = 1
OUTPUT_CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

# Try to find VB-Cable output device
def get_vb_output_device():
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"{i}: {info.get('name')}")
        if "VB-Audio" in info.get("name", "") or "CABLE Input" in info.get("name", ""):
            return i
    return None

output_device_index = 3
OUTPUT_CHANNELS = 1      

if output_device_index is None:
    print("VB-Cable not found. Using default output device.")
    output_device_index = None
else:
    print("VB-Cable found. Using it as output device.")

try:
    stream = p.open(format=FORMAT,
                channels=OUTPUT_CHANNELS,
                rate=RATE,
                output=True,
                output_device_index=output_device_index,
                frames_per_buffer=CHUNK)


except Exception as e:
    print("ERROR: Could not open audio stream.")
    print(e)
    p.terminate()
    exit()

async def handler(websocket):
    print("iPhone connected...")
    try:
        async for message in websocket:
            mono = np.frombuffer(message, dtype=np.int16)
            stereo = np.column_stack((mono, mono)).flatten()
            stream.write(stereo.tobytes())
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed.")

async def main():
    async with websockets.serve(handler, "", 8000):
        print("Server running on port 8000")
        await asyncio.Future()

asyncio.run(main())
