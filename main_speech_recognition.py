from pydub import AudioSegment
import speech_recognition as sr
import math
import os
class ConvertAudioToText():
    def __init__(self, filename, language):
        self.filename = filename
        self.language = language
        self.final_result = ""
        self.audio = AudioSegment.from_wav(self.filename)
    
    def conversion(self, audio_file):
        '''audio_file: wav format'''
        r = sr.Recognizer()
        audio_ex = sr.AudioFile(audio_file)
        with audio_ex as source:
            audiodata = r.record(audio_ex)
            return r.recognize_google(audiodata, language=self.language)

    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min):
        t1 = from_min * 1000
        t2 = to_min * 1000
        split_audio = self.audio[t1-300:t2+300]
        if split_audio.duration_seconds == 0:
            split_audio = self.audio[t1-300:t2]
            if split_audio.duration_seconds == 0:
                split_audio = self.audio[t1:t2+300]
        try:
            os.remove("audio_exported.wav")
        except:
            pass
        split_audio.export("audio_exported.wav", format="wav")
        try:
            res = self.conversion("audio_exported.wav")
            self.final_result += " " + res
        except:
            pass
        os.remove("audio_exported.wav")
                
    def main(self):
        total_sec = math.ceil(self.get_duration())
        for i in range(0, total_sec, 10): # 10: seconds per split
            self.single_split(i, i+10) # 10: seconds per split
        return self.final_result


def speech_recognition_algorithm(filepath, language):
    '''
    - filepath: xxxxx.wav
    - language: fr-FR for french, en-GB for english (UK), en-US for english (us), de-DE for german, es-ES for spanish, it-IT for italian
    '''
    audio_split = ConvertAudioToText(filepath, language)
    return audio_split.main()

