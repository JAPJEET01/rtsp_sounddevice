import pyaudio
import threading
import tkinter as tk
from PIL import Image, ImageTk
from pythonosc import osc_message_builder, udp_client, dispatcher, osc_server

# Sender configuration
RECEIVER_IP = '192.168.202.208'  # Receiver's IP address
RECEIVER_PORT = 12345  # Port for receiver
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4024
MAX_PACKET_SIZE = 5096  # Maximum size of each packet

# Initialize PyAudio
audio = pyaudio.PyAudio()
sender_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
receiver_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

ptt_active = False

# Create a function to simulate key press
def simulate_key_press(client):
    global ptt_active
    ptt_active = True
    client.send_message("/ptt", 1)
    print("Talking")

# Create a function to simulate key release
def simulate_key_release(client):
    global ptt_active
    ptt_active = False
    client.send_message("/ptt", 0)
    print("Not Talking")

def receive_audio(unused_addr, args, data):
    receiver_stream.write(data)

def key_pressed(event, client):
    if event.keysym == 'p':
        simulate_key_press(client)

def key_released(event, client):
    if event.keysym == 't':
        simulate_key_release(client)

# Create the main window
root = tk.Tk()
root.title("PTT Control")

# Calculate the center coordinates of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 440
window_height = 440
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create buttons for key press and key release
client = udp_client.SimpleUDPClient(RECEIVER_IP, RECEIVER_PORT)
key_press_button = tk.Button(root, text="Key Press (P)", command=lambda: simulate_key_press(client), bg="blue", padx=10, pady=10)
key_release_button = tk.Button(root, text="Key Release (T)", command=lambda: simulate_key_release(client), bg="red", padx=10, pady=10)

# Create a canvas for drawing circles
canvas = tk.Canvas(root, width=window_width, height=window_height, bg='black', highlightbackground="black")

# Pack the elements to display them in the window
key_press_button.pack(pady=10)
key_release_button.pack(pady=10)
canvas.pack()

# Initialize the canvas with a blue circle for "Ready to Use"
canvas.create_oval(170, 100, 270, 200, fill="blue")
canvas.create_text(220, 150, text="Available", fill="white", font=("Helvetica", 16, "bold"))

root.bind('<KeyPress>', lambda event: key_pressed(event, client))
root.bind('<KeyRelease>', lambda event: key_released(event, client))

# Create an OSC server to receive audio data
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/audio", receive_audio)
server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", RECEIVER_PORT), dispatcher)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

# Start the Tkinter main loop
root.mainloop()
