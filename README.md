# Transcripen
IMT Atlantique Project - connected pen for speech recognition

As part of our specialization in the design of communicating objects (TAF CooC) in our training at ITM Atlantique, we had a project which aimed at creating value through the current needs of business and industry using communicating objects. In other words, we had to create a communicating object that meets a user need. 
 
Each member of the group being in daily contact with students and / or journalists, we noted, during our field study, a recurring problem with these two types of individuals, who are confronted daily with many conferences and many long oral exchanges, even tedious, and during which the people in question cannot be passive (need for reflection / understanding / bounce back on questions, ...) and take note of the entire oral. We therefore decided to answer the following problem during this project: How to allow the interlocutors of an exchange, with the help of a connected object, to recover all the information conveyed during the latter?
 
After our field studies, we imagined and prototyped a connected pen/microphone that records a speech when the user decides to do so (using a button) and sends the audio recorded on the pen/microphone in text format (transcribed) to the user's computer via an application. Thanks to this object, the user can totally concentrate during the speech and does not have to take note of the information conveyed. We have decided that our object will take the shape of a pen, since everyone use such an object during interviews / speeches. This prototyping phase of this pen / microphone connected was done using an agile method (SCRUM) over 3 weeks.


This Github repository is composed by:
- A raspberry pi zero w (folder "raspberry"), connected to a button & a led through its GPIO ports, and connected to a microphone. When the user clicks on the button, not only does the led switch on, but the record also starts. When the user clicks on the button again, the led switch off, and the record stops. The led helps the user to know when the pen is recording or not. Also, the raspberry contains a code which sends, via wifi, the .wav recorded files to the laptop of the user from where the button of the application (described below) "récupérer les fichiers audio" is clicked.
- A Django Application (folder "application"), where the user choses the .wav file he wants to convert to text (recorded by the raspberry), choses the language of the audio file, clicks on the "transcrire le fichier audio" button, which calls the function speech_recognition (in the folder application/transcription_text), and returns as a .txt file, as well as directly in the application, the text file corresponding to the transcription of the audio file.

For each pieces of code (both for the raspberry pi and the application), we have provided in the corresponding files a detailed documentation.


If you want to test the whole prototype, you can follow the following steps:

If you want to reproduce our project, you need to:
1) Connection to the Raspberry
- Buy a Raspberry Pi Zero W with an SD card
- Install an imager https://www.raspberrypi.com/software/ 
- Download Raspberry Pi OS Lite https://www.raspberrypi.com/software/operating-systems/ 
- Put your SD Card in your computer and install the image of the Raspberry Pi Os Lite you've just downloaded in your SD Card thanks to the imager installed
- One finished, remove the SD Card and then Put in again in your computer
- Open the "boot" of the SD Card. Put in it a ssh file with no extension & a file called "wpa_supplicant.conf". In this file, you need to write:

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US
network={
	ssid="{your_network_ssid}"
	psk="{yout_network_password}"
	key_mgmt=WPA-PSK
}

- Please note that if you are on Windows, you might need another step. Otherwise it is enough.
- Remove the SD Card & put it in the Raspberry. Power your Raspberry Pi Zero W (there are 2 micro-usb inputs, use the one at the extremity of the Raspberry to power it.
- Connect your laptop to the same network as the one you've entered in the wpa_supplicant.conf file.
- Install an IP screener on your laptop such as https://angryip.org/
- Wait from 1 to 5 min to let time to the Raspberry to configure.
- Launch the IP screener. You need to look for raspberrypi.local. Note the corresponding IP address.
- Open a terminal, and write "ssh pi@theipaddressyouvenoted"
- If you have an error message, write "ssh-keygen -f pi@theipaddressyouvenoted" and follow the instructions
- Enter the raspberry default password: raspberry

2) Connect the microphone, the button & the led to the Raspberry according to the following schema:
[schema in progress]

3) Configuration of the Raspberry
- Check python (>3.0 version) is installed : "python --version"
- Install pip3 in the Raspberry : 
sudo apt-get update
sudo apt-get -y install python3-pip
- Check pip3 is installed : "pip3 --version"
- To install pyaudio, you need to follow the following commands:
sudo apt-get update 
sudo apt-get upgrade 
sudo apt-get dist-upgrade
sudo apt-get install portaudio19-dev 
sudo pip3 install pyaudio
- To install pydub, you need to follow the following commands:
sudo apt install ffmpeg
sudo pip3 install pydub
- Install the other required libraries:
sudo pip3 install wave
sudo pip3 install RPi.GPIO
- Configure the sound with alsamixer: launch the command "alsamixer", click on F6, select the USB microphone, then click on F5, then put everything to the maximum
- Add the folder raspberry_content to the Raspberry thanks to the scp command scp yourpathtothefolder pi@raspberryiponnetwork
- Add a file called lancement.sh to the Rasberry: nano lancement.sh and write on it:
cd /home/pi/final_algo.py
python3 final_algo.py
- Make this file executable: chmod 755 lancement.sh
- Test that the algorithm is launching with the command sh lancement.sh
- Create a log file with the command mkdir /home/pi/logs
- Open the crontab with the command: sudo contab -e
- At the end of the crontab, add the following line:
@reboot sh /home/pi/lancement.sh > /home/pi/logs/log.txt 2>&1
- Reboot your raspberry (sudo reboot)