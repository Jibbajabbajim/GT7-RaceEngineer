# GT7-RaceEngineer v0.3
Python script to provide simple "race engineer" audio feedback while driving. The main goal was to assist a friend who uses PSVR during endurance type races, but this may grow into something other players could find useful.
Current version only gives feedback when your tyres hit the temperature you input. More functionality to be added in furture versions.

This work is based entirely on Bornhalls work found here:- https://github.com/Bornhall/gt7telemetry

**Needs to be run from the terminal**

Run like this:

    python GT7-RaceEngineer.py

**Before running edit the config.json file**

{
	"ip" : "10.224.1.141",
	"language" : "EN",
	"voice" : "1",
	"tyreTempHigh" : "90",
	"tyreTempNormal" : "69.0"
}

"ip"
 - This is your consoles ip address.
	
"language"
 - This is the language/accent of your race engineer. Current supported languages/accents are "EN" and "SE".

"voice"
 - Leave set to 1. There is currently only 1 voice per language. More voices will be added.

"tyreTempHigh"
 - This is the tyre temparature in degrees centigrade that will trigger the engineer to warn of high tyre temparatures. 

"tyreTempNormal"
 - NOT CURRENTLY USED. This is the tyre temparature in degrees centigrade that will trigger the engineer to advise your tyres are in the normal temparature window. 

"enableLapSummary"
 - NOT CURRENTLY USED. Leave set to "false". This will be used to trigger a "summary" of information at the start of each lap. E.g. "25% fuel remaining" "around 6 laps left in the race".

## Requirements
You will need python 3.x installed, and you need to install the salsa20 and simpleaudio modules via pip:

    pip3 install salsa20
    pip3 install simpleaudio


## Future Versions

VOICES/LANGUAGES - More to be be added.

TYRE TEMPERATURES - More information such as cold tyres warning and normal temp notification.

FUEL/LAPS - FUEL/LAP summary triggered at each start finish line cross. Maybe an option to manually trigger feedback (button press)?
Calculate remaining laps possible in the time remaining.

STRATEGY - Predefined strategies (Plan A, Plan B etc). Monitor during the race and provide feedback (e.g. "Two more laps needed in this stint"). Monitor tyre use and percentage and provide feedback ("You are using too much tyres/fuel to last the stint". Calculate the number of laps remaining in the race? Not sure is this is possible yet.

CONFIG FILE - As the number of parameters increases, a config file may make more sense.

IMPROVED AUDIO - edit the audio to include radio "beeps" and radio quality sound.
