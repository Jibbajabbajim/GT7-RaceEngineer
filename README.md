# GT7-RaceEngineer
Python script to provide simple "race engineer" audio feedback while driving.

**Needs to be run from the terminal**, and works best with a terminal of at least 92 x 42 characters. The output is in a separate buffer, but you can comment out lines 10-29 to just write to your current terminal (might want to clear the terminal first).

Run like this (substitute with your own console's LAN IP address):

    python3 GT7-RaceEngineer.py <IP ADDRESS> <LANGUAGE> <VOICE> <TYRE TEMP>

Where:
    <IP ADDRESS> - This is your consoles ip address
    <LANGUAGE> - This is the language of your race engineer. Current supported languages are "EN" and "SE".
    <VOICE> - There are currently 3 different voices per language. Valid options are "1" "2" "3".
    <TYRE TEMP> - This is the tyre temparature in degrees centigrade that will trigger the engineer. 

Example:

    python3 GT7-RaceEngineer.py 129.168.1.123 EN 1 120

This work is based entirely on Bornhalls work found here:- https://github.com/Bornhall/gt7telemetry

## Requirements
You will need python 3.x installed, and you need to install the salsa20 and simpleaudio module via pip:

    pip3 install salsa20
    pip3 install simpleaudio
