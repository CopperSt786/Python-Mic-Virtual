import pyaudio

p = pyaudio.PyAudio()

print("Available Output Devices:\n")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info.get('maxOutputChannels') > 0:
        print(f"Index {i}: {info['name']} — Channels: {info['maxOutputChannels']}")

p.terminate()
