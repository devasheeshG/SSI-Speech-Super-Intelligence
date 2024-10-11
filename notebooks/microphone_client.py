# File: notebooks/microphone_client.py
# Description: This script demonstrates how to create a simple microphone client that sends audio data to a FastAPI server.

import pyaudio
from websockets.sync.client import connect
from termcolor import colored

CHUNK_SIZE = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

def list_microphones():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    devices = []

    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            devices.append({
                'index': i,
                'name': device_info.get('name'),
                'defaultSampleRate': device_info.get('defaultSampleRate'),
                'maxInputChannels': device_info.get('maxInputChannels'),
                'maxOutputChannels': device_info.get('maxOutputChannels')
            })
    
    p.terminate()
    return devices

def main():
    server_ip = input("Enter server IP address (default: 192.168.0.253): ") or "192.168.0.253"
    server_port = input("Enter server port (default: 8000): ") or 8000
    server_url = f"ws://{server_ip}:{server_port}/ws/transcribe"
    # server_url = f"ws://{server_ip}:{server_port}/temp"

    devices = list_microphones()
    print(colored("Available microphones:", "cyan"))
    # for index, name in devices:
    #     print(colored(f"{index}: {name}", "yellow"))
        
    for device in list_microphones():
        print(colored(f"Index: {device['index']}", "white"))
        print(colored(f"Name: {device['name']}", "yellow"))
        print(colored(f"Default Sample Rate: {device['defaultSampleRate']}", "yellow"))
        print(colored(f"Max Input Channels: {device['maxInputChannels']}", "yellow"))
        print(colored(f"Max Output Channels: {device['maxOutputChannels']}", "yellow"))
        print()

    mic_index = int(input("Select a microphone by index: "))

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=mic_index,
                    frames_per_buffer=CHUNK_SIZE)

    try:
        with connect(server_url) as websocket:
            print(colored("Connection established", "green"))

            while True:
                data = stream.read(CHUNK_SIZE, exception_on_overflow=True)
                websocket.send(data)

    except KeyboardInterrupt:
        print(colored("Exiting...", "red"))
        
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))
    
    finally:
        if stream is not None:
            if stream.is_active():
                stream.stop_stream()
            stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
