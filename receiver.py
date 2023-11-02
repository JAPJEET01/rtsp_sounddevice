import socket
import sounddevice as sd

# Constants
SENDER_IP = 'YOUR_SENDER_IP'  # Replace with the sender's IP address
RECEIVER_IP = 'YOUR_RECEIVER_IP'  # Replace with the receiver's IP address
PORT = 12345

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((RECEIVER_IP, PORT))

# Initialize sounddevice
CHUNK = 1024
FORMAT = 'int16'
CHANNELS = 1
RATE = 44100

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    sock.sendto(indata, (SENDER_IP, PORT))

with sd.InputStream(callback=callback, channels=CHANNELS, dtype=FORMAT, samplerate=RATE):
    sd.sleep(-1)
