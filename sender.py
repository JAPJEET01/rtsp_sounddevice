import socket
import pyaudio

# Constants
SENDER_IP = 'YOUR_SENDER_IP'  # Replace with the sender's IP address
RECEIVER_IP = 'YOUR_RECEIVER_IP'  # Replace with the receiver's IP address
PORT = 12345

# Initialize PyAudio
p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Start audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

while True:
    audio_data = stream.read(CHUNK)
    sock.sendto(audio_data, (RECEIVER_IP, PORT))

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
sock.close()
