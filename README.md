# GT7-RaceEngineer
Python script to provide simple "race engineer" audio feedback while driving. The main goal was to assist a friend who uses PSVR during endurance type races, but this may grow into something other players could find useful.
Current version only gives feedback when your tyres hit the temperature you input. More functionality to be added in furture versions.

This work is based entirely on Bornhalls work found here:- https://github.com/Bornhall/gt7telemetry

**Needs to be run from the terminal**

Run like this (substitute with your own console's LAN IP address):

    python3 GT7-RaceEngineer.py <IP ADDRESS> <LANGUAGE> <TYRE TEMP>
    
IP ADDRESS
This is your consoles ip address.
	
LANGUAGE
This is the language of your race engineer. Current supported languages are "EN" and "SE".

TYRE TEMP
This is the tyre temparature in degrees centigrade that will trigger the engineer. 

Example:

    python3 GT7-RaceEngineer.py 129.168.1.123 EN 120.0

VOICE
There is currently only 1 voice per language. More voices will be added.

## Requirements
You will need python 3.x installed, and you need to install the salsa20 and simpleaudio modules via pip:

    pip3 install salsa20
    pip3 install simpleaudio


## Future Versions

VOICES - More voices will be added.

TYRE TEMPERATURES - More information such as cold tyres warning and normal temp notification.

FUEL/LAPS - FUEL/LAP summary triggered at each start finish line cross. Maybe an option to manually trigger feedback (button press)?

STRATEGY - Predefined strategies (Plan A, Plan B etc). Monitor during the race and provide feedback (e.g. "Two more laps needed in this stint"). Monitor tyre use and percentage and provide feedback ("You are using too much tyres/fuel to last the stint". Calculate the number of laps remaining in the race? Not sure is this is possible yet.

CONFIG FILE - As the number of parameters increases, a config file may make more sense.
