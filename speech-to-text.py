import threading
import time
import pyaudio
import wave

# Audio recording configuration
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1              # Mono audio
RATE = 44100              # Sample rate
CHUNK = 1024              # Buffer size
RECORD_SECONDS = 3        # Recording duration per session
OUTPUT_FILENAME_PREFIX = "output"  # Prefix for output files

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Function to capture microphone input
def capture_audio():
    counter = 0
    while True:
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print("Recording...")

        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        # Save the recording
        output_filename = f"{OUTPUT_FILENAME_PREFIX}_{counter}.wav"
        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        print(f"Saved {output_filename}")
        counter += 1

        # Wait for 3 seconds before recording again
        time.sleep(3)

# Function to print "Hello" every 5 seconds
def print_hello():
    while True:
        print("Hello")
        time.sleep(5)

# Creating threads
audio_thread = threading.Thread(target=capture_audio)
hello_thread = threading.Thread(target=print_hello)

# Starting threads
audio_thread.start()
hello_thread.start()

# Joining threads to main thread
audio_thread.join()
hello_thread.join()