########################################################################################################################
########################################################################################################################
########################################################################################################################
# Nous créons ici une classe qui a pour attributs la root d'un fichier audio .wav ainsi que sa langue et qui renvoit le
# texte correspondant à la transcription du fichier audio en question. Cette classe effectue un "préprocessing" de
# l'audio d'entrée (calcul de la durée de l'audio, découpage en sous-audios de 10s), et applique à l'audio préprocessé 
# l'algorithme de Speech Recognition développé par Google et accessible simplement via une API (incluse dans la librarie
# speech_recognition disponible sur Github https://github.com/Uberi/speech_recognition).
########################################################################################################################
########################################################################################################################
########################################################################################################################

import math
import os
from pydub import AudioSegment # librairie qui permet de manipuler un fichier audio simplement (ouverture de l'audio, augmentation / diminuaiton du volume de l'audio, segmentation de l'audio, calcul de la durée de l'audio, et toute autre manipulation possible sur un audio. La librairie est en open-source sur https://github.com/jiaaro/pydub). Pour utiliser pydub, il faut installer ffmpeg/avlib.
import speech_recognition as sr # librairie (https://github.com/Uberi/speech_recognition) qui effectue de la reconnaissance vocale via diverses APIs, en ligne et hors ligne, notamment CMU Sphinx, Google Cloud Speech, WIT.ai, Microsoft Azure Speech, Houndify, IBM Speech to Text, ou encore Snowboy Hotword Detection.

class ConvertAudioToText():
    def __init__(self, filename, language):
        '''
        Cette classe va découper l'audio en sous-audios de 10s et va appeler au fur et à mesure l'API Google de Speech Recognition pour effectuer la transcription sur chaque bout de 10s. Effectivement, l'algorithme de Google a été entraîné sur des audios dont la taille varie entre 1 seconde à 20 secondes.
        - filename: chemin du fichier (exemple: audio/test.wav)
        - language: fr-FR for french, en-GB for english (UK), en-US for english (us), de-DE for german, es-ES for spanish, it-IT for italian
        '''
        self.filename = filename
        self.language = language
        self.final_result = "" # stocke le résultat final (le texte de l'audio transcrit)
        self.audio = AudioSegment.from_wav(self.filename) # ouvre le fichier .wav en tant qu'instance AudioSegment à l'aide de la méthode AudioSegment.from_file() (ici, from_wav)
    
    def conversion_into_text(self, audio_file):
        '''
        - audio_file: chemin du fichier .wav exporté (ce n'est pas le fichier original, mais le fichier préprocessé qui a été sauvegardé
        '''
        r = sr.Recognizer() # instancie un objet de type Recognizer
        audio_ex = sr.AudioFile(audio_file) # nécessaire d'avoir ce format pour le Recognizer de Speech_recognition
        with audio_ex as source:
            audiodata = r.record(audio_ex) # lit l'audio
            return r.recognize_google(audiodata, language=self.language) # appelle l'API Google en utilisant la clé d'API par défaut (pas de limite d'appel)

    def get_duration(self):
        return self.audio.duration_seconds # la fonciton duration_seconds permet donner la durée en secondes d'un fichier audio à l'aide de pydub
    
    def algorithm_on_single_split_of_audio(self, from_sec, to_sec):
        '''
        Cette fonction découpe un fichier audio initial entre la seconde from_sec de l'audio et la seconde to_sec de l'audio. 
        - from_sec:
        - to_sec
        '''
        t1 = from_sec * 1000 # il faut convertir le temps de début en milisecondes
        t2 = to_sec * 1000 # il faut convertir le temps de fin en milisecondes
        split_audio = self.audio[t1-1000:t2+1000] # on récupère l'audio entre les milisecondes t1 et t2. Afin d'avoir le moins possible de mot haché lors du découpage, ce qui empêche une transcription correcte, nous prenons 1 secondes avant et après pour chaque slot d'audio (soit 1000 milisecondes avant et après)
        if split_audio.duration_seconds == 0: # Si on est en début ou fin de l'audio, il se peut que le slot de ait une durée de 0 (car on ne peut pas prendre l'audio à partir de la -1000ème miliseconde ou jusqu'à la +1000ème). Du coup, on doit gérer ces cas:
            split_audio = self.audio[t1-1000:t2] # Dans le cas où on est à la fin de l'audio (si on est au début, split_audio.duration == 0 ici)
            if split_audio.duration_seconds == 0: # Dans le cas où on est au début  de l'audio (si on est à la fin de l'audio, on a self.audio[t1-1000:t2].duration_seconds != 0 donc on ne rentre pas ici), mais où self.audio[t1-1000:t2].duration_seconds == 0 puisque self.audio[t1-1000] n'existe pas.
                split_audio = self.audio[t1:t2+1000] # Dans le cas où on est au début  de l'audio
        try:
            os.remove("audio_exported.wav") # s'il y a déjà un slot d'audio exporté (voir ci-dessous: on exporte chaque slot d'audio, que l'on traite avec la fonction de speech_recognition, et que l'on supprime une fois la transcription du slot effectuée). Le try / except permet de ne pas avoir d'erreur si jamais on est au premier découpage de l'audio, par exemple.
        except:
            pass
        split_audio.export("audio_exported.wav", format="wav") # On exporte le slot de 10 secondes (entre 11 et 12 exactement puisqu'on a pris une seconde de plus au début et une de plus à la fin (à part quand on est au début ou à la fin de l'audio, comme expliqué ci-dessus))
        try:
            res = self.conversion_into_text("audio_exported.wav") # on appelle la fonction conversion_into_text détaillée ci-dessus qui retourne la transcription (en string) de l'audio (path du slot de l'audio: audio_exported.wav, qu'on connaît puisque c'est nous qui l'avons exporté ci-dessus)
            self.final_result += " " + res # On ajoute la transcription du slot au résultat final. On a ajouté un espace entre chaque transcription de slots (" ") qui est nécessaire pour ne pas avoir 2 mots collés. 
        except:
            pass
        os.remove("audio_exported.wav") # On supprime le slot une fois la transcription effectuée
                
    def main(self):
        total_sec = math.ceil(self.get_duration()) # self.get_duration retourne un flottant. On veut ici itérer sur l'ensemble des slots de 10 secondes de l'audio. Si on a la durée totale de l'audio qui n'est pas égale à un nombre rond, on va prendre l'entier supérieur à ce-dernier (35.4s donne 36s), car on veut être sûr d'avoir l'intégtalité de l'audio, quitte à avoir un slot plus petit que 10 secondes à la fin. On a nécessairement besoin d'avoir un entier ici pour pouvoir itérer avec la fonction "range" ci-dessous. 
        for i in range(0, total_sec, 10): # On itère sur le nombre total de slots (de 0 à total_sec avec un saut de 10, car on veut des slots de 10s)
            self.algorithm_on_single_split_of_audio(i, i+10) # On applique l'algorithme de transcription de l'audio entre la seconde i et la seconde i+10 de l'audio.
        return self.final_result.strip() # on retourne, sous forme de string, le texte final. La fonction strip() permet d'enlever les espaces en trop au début et à la fin du texte.


def speech_recognition_algorithm(filepath, language):
    '''
    Cette fonction instancie un objet de type ConvertAudioToText et appelle la fonction "main" de cette classe, qui effectue le préprocessing de l'audio et lance l'algorithme de transcription de l'audio en texte de Google sur celui-ci. C'est cette fonction qui va ête appelée par l'application.
    - filepath: xxxxx.wav
    - language: fr-FR for french, en-GB for english (UK), en-US for english (us), de-DE for german, es-ES for spanish, it-IT for italian
    '''
    audio_split = ConvertAudioToText(filepath, language)
    return audio_split.main()