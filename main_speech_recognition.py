import speech_recognition as sr
def main(audio_file):
    '''audio_file: wav format'''
    r = sr.Recognizer()
    return r.recognize_google(audio_file)