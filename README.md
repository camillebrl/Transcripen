# Transcripen
IMT Atlantique Project - connected pen for speech recognition

The project is composed by:
- A raspberry pi zero w (folder "raspberry"), connected to a button & a led through its GPIO ports, and connected to a microphone. When the user clicks on the button, not only does the led switch on, but the record also starts. When the user clicks on the button again, the led switch off, and the record stops. The led helps the user to know when the pen is recording or not. Also, the raspberry contains a code which sends, via wifi, the .wav recorded files to the laptop of the user from where the button of the application (described below) "récupérer les fichiers audio" is clicked.
- A Django Application (folder "application"), where the user choses the .wav file he wants to convert to text (recorded by the raspberry), choses the language of the audio file, clicks on the "transcrire le fichier audio" button, which calls the function speech_recognition (in the folder application/transcription_text), and returns as a .txt file, as well as directly in the application, the text file corresponding to the transcription of the audio file.

For each pieces of code (both for the raspberry pi and the application), we have provided in the corresponding files a detailed documentation.