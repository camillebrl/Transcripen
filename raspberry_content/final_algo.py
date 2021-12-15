########################################################################################################################
########################################################################################################################
########################################################################################################################
# Cet algorithme permet d'actionner l'enregistrement du micro et d'allumer la led via la raspberry lorsque le boutton 
# est actionné.
########################################################################################################################
########################################################################################################################
########################################################################################################################


import time
from datetime import datetime
import RPi.GPIO as GPIO # Pour utiliser les ports GPIO de la raspberry, il faut utiliser une librarie python. Il en existe plusieurs, mais la plus connue (celle pour laquelle il y a le plus d'exemple sur internet) est Rpi.GPIO.
import pyaudio # PyAudio fournit des liaisons Python pour PortAudio, la bibliothèque de référence qui gère les entrée/sortie usb d'audio sur toutes les plateformes (dont la raspberry). 
import wave # La librairie wave fournit une interface pour le format de son WAV. Il permet d'exporter simplement un fichier .wav.
from pydub import AudioSegment # librairie qui permet de manipuler un fichier audio simplement (ouverture de l'audio, augmentation / diminuaiton du volume de l'audio, segmentation de l'audio, calcul de la durée de l'audio, et toute autre manipulation possible sur un audio. La librairie est en open-source sur https://github.com/jiaaro/pydub). Pour utiliser pydub, il faut installer ffmpeg/avlib.


# Il est important de comprendre que pyaudio découpe les données en CHUNKS (trames), au lieu d'avoir une quantité continue d'audio, afin de limiter la puissance de traitement requise (RAM), puisque la Raspberry a une RAM assez faible (512M pour notre Raspberry Pi Zero W). 
CHUNK = 1024 # nombre de trames dans lesquelles les signaux sont divisés (ce chiffre est une puissance de 2, ici 2**10)
FORMAT = pyaudio.paInt16 # Le son est stocké en binaire, comme tout ce qui concerne les ordinateurs. Ici, 16 bits sont stockés par échantillon
CHANNELS = 1 # chaque trame a 1 échantillon (16 bits)
RATE = 48000 # 48000 images sont collectées par secondes. L'unité est le Hz. On a obtenu ce chiffre en faisant "p.get_device_info_by_index(0)['defaultSampleRate']" (sachant que l'index de notre usb microphone device est de 0)
# En d'autres termes, par seconde, le système lit 48000/1025 morceaux de la mémoire (soit c.4,7). Ici, cela dépend du microphone. 

p = pyaudio.PyAudio() # On instancie un objet Pyaudio

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
		        input_device_index=0, # identification du device audio utilisé. Pour le trouver, nous avons au préalable printé "p.get_host_api_info_by_index(0)"" et nous avons obtenu le port usb, c'est à dire notre microphone. C'est donc bien le port 0 qui corresond au microphone. On peut aussi faire : numdevices = info.get('deviceCount') puis for i in range (0,numdevices): p.get_device_info_by_index(i).get("name") pour voir le nom des devices en question et trouver celui qui correspond à notre micro.
                frames_per_buffer=CHUNK)

GPIO.setwarnings(False) # Pour ne pas avoir les warnings dans les logs 
GPIO.setmode(GPIO.BOARD) # Il y a 2 façons d'identifier les boards sur la raspberry: BCM et BOARD. L’option GPIO.BOARD indique que l'on se réfère aux broches par le numéro de la broche du connecteur, c’est-à-dire les numéros imprimés sur la carte, alors que L’option GPIO.BCM signifie que l'on se réfère aux broches par le numéro "Broadcom SOC channel". Ce sont les numéros après "GPIO" dans les schémas des pins de la raspberry.Puisque l'idenfication BCM est différente entre les différentes Raspberry, et afin de ne pas faire d'erreur, nous avons opté pour l'identification BOARD.
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # On définit le pin du bouton (le pin de l'output du bouton). Quand au GPIO.PUD_DOWN, il faut comprendre cela: une entrée gpio flotte entre 0 et 1 si elle n'est pas connectée à une tension. Dès lors, la variable pull_up_down fournit cette tension afin que le gpio ait une valeur définie jusqu'à ce qu'elle soit remplacée par une force plus forte. GPIO.PUD_DOWN signifie que, l'on s'attend à ce que la force la plus forte le tire jusqu'à 1, alors uqe PUD_UP signifie que l'on s'attend à ce que la force la plus forte le tire vers 0.
GPIO.setup(7, GPIO.OUT) # On définit le pin de la led (input de la led)
isPressed = False # On initialise la variable isPressed (True quand l'utilisateur appuis sur le bouton, False sinon)
recorded = False # On initialise la variable recorded (True quand l'audio record, False quand il ne record pas)
array = [] # Lorsque l'utilisateur appuie sur le bouton, il y a, comme expliqué ci-dessus, plusieurs entrées qui arrivent (entre 0 et 1, que l'on arrondie à 1 (PUD_DOWN décrit ci-dessus)). Dès lors, on ne peut pas juste considérer que l'utilisateur appuie sur le bouton quand le port GPIO 11 (input) est à 1, puisqu'on a, à ce moment là, un grand nombre de 1. Comment savoir alors si la personne a appuyé sur le bouton? Par exemple, si elle appuie 2 fois sur le bouton, on a un grand nombre de fois GPIO 11 égal à 1. Tout comme si la personne appuie 1 fois. Nous avons décidé de gérer cela de la manière suivante: si l'utilsateur appuie sur le bouton, l'ensemble des input (lorsque GPIO = 1) est stocké dans une liste (ici, array). On considère qu'un array correspond à un appuuie sur le bouton. On ajoute ces input dans l'array tant que le premier input a été ajouté dans les 2 secondes qui suivent l'input en question. Si ça dépasse 2 secondes, on considère un nouvel array (on vide l'array), et donc on considère que la personne a de-nouveau appuyé sur le bouton. Cette méthode nous permet de différencier les inputs qui suivent nécessairement un appui sur le bouton des vrais appuis sur le bouton. 
frames = [] # Comme expliqué ci-dessus, pyaudio ne permet pas d'enregistrer un audio en continue, mais à la place enregistre sous forme de slot. Dès lors, nous ajoutons ces slots d'audio (1 slot = 1s) dans cet array "frame".

while True: # tant qu'il n'y a pas de bug, tant que l'algorithme n'a pas été arrêté: tourne en permanence
    start_time = time.time() # comme expliqué ci-dessus (dans array), pour différencier les inputs qui suivent nécessairement un appui sur le bouton des vrais appuis sur le bouton, on considère que si l'input est dans les 2s du premier input reçu, il s'agit d'un input qui suit l'appui, et non d'un véritable appui sur le bouton. Du coup, il faut instancier le temps du premier appui, comme fait ici.
    while GPIO.input(11) == 1 and time.time() - start_time < 2: # cf ci-dessus (tant qu'on a un input et que ce-dernier est à moins de 2s du premier input)
        array.append(not isPressed) # On ajoute dans l'array l'état (l'état est opposé à l'état précédent: si on avait isPressed = True (bouton appuyé), on va avoir isPressed = False, etc.)
    if len(array) > 1: # Si on a bien un input
        isPressed = array[0] # On ne considère que le premier état, qui correspond au premier input
    if isPressed: # Si on a isPressed à True, alors on allume la led & on enregistre.
        GPIO.output(7, GPIO.HIGH) # on allume la led
        input_audio = stream.read(2 * RATE, exception_on_overflow = False) # on enregistre 1s
        frames.append(input_audio) # on ajoute la seconde d'enregistrement à frames (voir explication de la variable "frames")
        recorded = True # ça veut dire qu'on a bien record qqch, donc on passe la variable "recorded" (définie ci-dessus) à True.
    else:
        GPIO.output(7, GPIO.LOW) # Si on a isPressed = False, alors on met la led à éteint
        if recorded: # si on avait recorded à True avant (ça veut dire que l'utilisateur a rappuyé sur le bouton pour éteindre la led & arrêter le record): on sauve le fichier "frames" de l'ensemble des enregistrements de slots de 1s (on a l'enregistrement final)
            WAVE_OUTPUT_FILENAME = datetime.now().strftime("audio_folder/%d%b%Y_%Hh%Mmin.wav") # on nomme le fichier avec %d le jour d'aujourd'hui, %b le nom du mois en anglais, %Y l'année en 4 chiffres, puis _, puis l'heure suivie de h, et les minutes suivies de "min". On place l'audio dans le folder "audio_folder".
            wav_file = wave.open(WAVE_OUTPUT_FILENAME, "wb") # on ouvre ce document wav qui porte le nom ci-dessus (WAVE_OUTPUT_FILENAME) pour écrire dessus
            wav_file.setnchannels(1) # On rappelle les channels de l'audio
            wav_file.setsampwidth(2)
            wav_file.setframerate(48000) # On rappelle les Hz de l'audio
            wav_file.writeframes(b''.join(frames)) # on écrit dans le fichier wav ce qu'on a enregistré ("frames")
            wav_file.close() # on ferme le fichier wav.
            recorded = False # On remet à False le recorded. On a maintenant enregistré le fichier, le micro n'est plus en train de record.
            frames = [] # On vide l'enregistrement de la mémoire.
            song = AudioSegment.from_wav(WAVE_OUTPUT_FILENAME) # On récupère le fichier wav sauvé
            song = song + 20 # On lui ajoute manuellement 20db (pour que le son soit plus fort)
            song.export(WAVE_OUTPUT_FILENAME, "wav") # On exporte de nouveau le fichier wav qui a ce coup-ci 20db de plus.
    array = [] # On vide l'array d'input du bouton une fois qu'on a dépassé les 2 secondes (les inputs que l'on reçoit ne sont plus dues aux inputs automatiques qui suivent l'appuie sur le bouton)

GPIO.cleanup()
stream.stop_stream()
stream.close()
p.terminate()
