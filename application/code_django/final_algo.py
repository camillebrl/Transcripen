import pyaudio
import wave
from pydub import AudioSegment
import RPi.GPIO as GPIO
import time
from datetime import datetime


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
		input_device_index=0,
                frames_per_buffer=CHUNK)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(7, GPIO.OUT)
isPressed = False
recorded = False
array = []
frames = []

while True:
    start_time = time.time()
    while GPIO.input(11) == 1 and time.time() - start_time < 2:
        array.append(not isPressed)
    if len(array) > 1:
        isPressed = array[0]
    if isPressed:
        GPIO.output(7, GPIO.HIGH)
        input_audio = stream.read(2 * RATE, exception_on_overflow = False)
        frames.append(input_audio)
        recorded = True
    else:
        GPIO.output(7, GPIO.LOW)
        if recorded:
            WAVE_OUTPUT_FILENAME = datetime.now().strftime("audio_folder/%d%b%Y_%Hh%Mmin.wav")
            wav_file = wave.open(WAVE_OUTPUT_FILENAME, "wb")
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(48000)
            wav_file.writeframes(b''.join(frames))
            wav_file.close()
            recorded = False
            frames = []
            song = AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)
            song = song + 20
            song.export(WAVE_OUTPUT_FILENAME, "wav")
    array = []

GPIO.cleanup()
stream.stop_stream()
stream.close()
p.terminate()
