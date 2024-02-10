# GT7-RaceEngineer
Python script to provide simple "race engineer" audio feedback while driving.

**Needs to be run from the terminal**, and works best with a terminal of at least 92 x 42 characters. The output is in a separate buffer, but you can comment out lines 10-29 to just write to your current terminal (might want to clear the terminal first).

Run like this (substitute with your own console's LAN IP address):

    python3 GT7-RaceEngineer.py 129.168.1.123

This work is based entirely on Bornhalls work found here:- https://github.com/Bornhall/gt7telemetry

![Screenshot of output](https://user-images.githubusercontent.com/3602224/182450262-56992d54-409d-4fb7-bfec-35b04dc7f6aa.png)

## Requirements
You will need python 3.x installed, and you need to install the salsa20 module via pip:

    pip3 install salsa20
