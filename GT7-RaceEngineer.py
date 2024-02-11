import signal
from datetime import datetime as dt
from datetime import timedelta as td
import os
import socket
import sys
import struct
import time
import random
#pip3 install salsa20
import simpleaudio as sa
from salsa20 import Salsa20_xor

# ansi prefix
pref = "\033["

# ports for send and receive data
SendPort = 33739
ReceivePort = 33740

# ctrl-c handler
def handler(signum, frame):
	sys.stdout.write(f'{pref}?1049l')	# revert buffer
	sys.stdout.write(f'{pref}?25h')		# restore cursor
	sys.stdout.flush()
	exit(1)

# handle ctrl-c
signal.signal(signal.SIGINT, handler)

sys.stdout.write(f'{pref}?1049h')	# alt buffer
sys.stdout.write(f'{pref}?25l')		# hide cursor
sys.stdout.flush()

# get ip address from command line
if len(sys.argv) == 3:
    ip = sys.argv[1]
    language = sys.argv[2]
else:
    print('Run like : python3 gt7telemetry.py <playstation-ip>')
    exit(1)

absolute_path = os.path.dirname(__file__)
full_path1 = os.path.join(absolute_path, "audio/EN_Voice1_TyresHot1.wav")
full_path2 = os.path.join(absolute_path, "audio/EN_Voice1_TyresHot2.wav")
full_path3 = os.path.join(absolute_path, "audio/EN_Voice1_TyresHot3.wav")
full_path4 = os.path.join(absolute_path, "audio/SE_Voice1_TyresHot1.wav")
full_path5 = os.path.join(absolute_path, "audio/SE_Voice1_TyresHot2.wav")
full_path6 = os.path.join(absolute_path, "audio/SE_Voice1_TyresHot3.wav")

overTemp = 0
wave_obj1 = sa.WaveObject.from_wave_file(full_path1)
wave_obj2 = sa.WaveObject.from_wave_file(full_path2)
wave_obj3 = sa.WaveObject.from_wave_file(full_path3)
wave_obj4 = sa.WaveObject.from_wave_file(full_path4)
wave_obj5 = sa.WaveObject.from_wave_file(full_path5)
wave_obj6 = sa.WaveObject.from_wave_file(full_path6)

# Create a UDP socket and bind it
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', ReceivePort))
s.settimeout(10)

# data stream decoding
def salsa20_dec(dat):
	KEY = b'Simulator Interface Packet GT7 ver 0.0'
	# Seed IV is always located here
	oiv = dat[0x40:0x44]
	iv1 = int.from_bytes(oiv, byteorder='little')
	# Notice DEADBEAF, not DEADBEEF
	iv2 = iv1 ^ 0xDEADBEAF
	IV = bytearray()
	IV.extend(iv2.to_bytes(4, 'little'))
	IV.extend(iv1.to_bytes(4, 'little'))
	ddata = Salsa20_xor(dat, bytes(IV), KEY[0:32])
	magic = int.from_bytes(ddata[0:4], byteorder='little')
	if magic != 0x47375330:
		return bytearray(b'')
	return ddata

# send heartbeat
def send_hb(s):
	send_data = 'A'
	s.sendto(send_data.encode('utf-8'), (ip, SendPort))
	#print('send heartbeat')

# generic print function
def printAt(str, row=1, column=1, bold=0, underline=0, reverse=0):
	sys.stdout.write('{}{};{}H'.format(pref, row, column))
	if reverse:
		sys.stdout.write('{}7m'.format(pref))
	if bold:
		sys.stdout.write('{}1m'.format(pref))
	if underline:
		sys.stdout.write('{}4m'.format(pref))
	if not bold and not underline and not reverse:
		sys.stdout.write('{}0m'.format(pref))
	sys.stdout.write(str)

def secondsToLaptime(seconds):
	remaining = seconds
	minutes = seconds // 60
	remaining = seconds % 60
	return '{:01.0f}:{:06.3f}'.format(minutes, remaining)



# start by sending heartbeat
send_hb(s)

printAt('GT7 Tyre Temperature Display 0.1 (ctrl-c to quit)', 1, 1, bold=1)

printAt('Tyre Data', 3, 3, underline=1)
printAt('FL:        °C', 4, 1)
printAt('FR:        °C', 5, 1)
printAt('RL:        °C', 6, 1)
printAt('RR:        °C', 7, 1)



sys.stdout.flush()

prevlap = -1
pktid = 0
pknt = 0

while True:
	try:
		data, address = s.recvfrom(4096)
		pknt = pknt + 1
		ddata = salsa20_dec(data)
		if len(ddata) > 0 and struct.unpack('i', ddata[0x70:0x70+4])[0] > pktid:
			pktid = struct.unpack('i', ddata[0x70:0x70+4])[0]

			bstlap = struct.unpack('i', ddata[0x78:0x78+4])[0]
			lstlap = struct.unpack('i', ddata[0x7C:0x7C+4])[0]
			curlap = struct.unpack('h', ddata[0x74:0x74+2])[0]
			if curlap > 0:
				dt_now = dt.now()
				if curlap != prevlap:
					prevlap = curlap
					dt_start = dt_now
				curLapTime = dt_now - dt_start
				
			else:
				curLapTime = 0
				
					
			cgear = struct.unpack('B', ddata[0x90:0x90+1])[0] & 0b00001111
			sgear = struct.unpack('B', ddata[0x90:0x90+1])[0] >> 4
			if cgear < 1:
				cgear = 'R'
			if sgear > 14:
				sgear = '–'

			fuelCapacity = struct.unpack('f', ddata[0x48:0x48+4])[0]
			isEV = False if fuelCapacity > 0 else True
				

			boost = struct.unpack('f', ddata[0x50:0x50+4])[0] - 1
			hasTurbo = True if boost > -1 else False


			tyreDiamFL = struct.unpack('f', ddata[0xB4:0xB4+4])[0]
			tyreDiamFR = struct.unpack('f', ddata[0xB8:0xB8+4])[0]
			tyreDiamRL = struct.unpack('f', ddata[0xBC:0xBC+4])[0]
			tyreDiamRR = struct.unpack('f', ddata[0xC0:0xC0+4])[0]

			tyreSpeedFL = abs(3.6 * tyreDiamFL * struct.unpack('f', ddata[0xA4:0xA4+4])[0])
			tyreSpeedFR = abs(3.6 * tyreDiamFR * struct.unpack('f', ddata[0xA8:0xA8+4])[0])
			tyreSpeedRL = abs(3.6 * tyreDiamRL * struct.unpack('f', ddata[0xAC:0xAC+4])[0])
			tyreSpeedRR = abs(3.6 * tyreDiamRR * struct.unpack('f', ddata[0xB0:0xB0+4])[0])

			carSpeed = 3.6 * struct.unpack('f', ddata[0x4C:0x4C+4])[0]

			if carSpeed > 0:
				tyreSlipRatioFL = '{:6.2f}'.format(tyreSpeedFL / carSpeed)
				tyreSlipRatioFR = '{:6.2f}'.format(tyreSpeedFR / carSpeed)
				tyreSlipRatioRL = '{:6.2f}'.format(tyreSpeedRL / carSpeed)
				tyreSlipRatioRR = '{:6.2f}'.format(tyreSpeedRR / carSpeed)
			else:
				tyreSlipRatioFL = '  –  '
				tyreSlipRatioFR = '  –  '
				tyreSlipRatioRL = '  -  '
				tyreSlipRatioRR = '  –  '

			
			tyreTempFL = struct.unpack('f', ddata[0x60:0x60+4])[0]
			tyreTempFR = struct.unpack('f', ddata[0x64:0x64+4])[0]
			tyreTempRL = struct.unpack('f', ddata[0x68:0x68+4])[0]
			tyreTempRR = struct.unpack('f', ddata[0x6C:0x6C+4])[0]
			
			printAt('{:6.1f}'.format(struct.unpack('f', ddata[0x60:0x60+4])[0]), 4, 5)					# tyre temp FL
			printAt('{:6.1f}'.format(struct.unpack('f', ddata[0x64:0x64+4])[0]), 5, 5)					# tyre temp FR
			printAt('{:6.1f}'.format(struct.unpack('f', ddata[0x68:0x68+4])[0]), 6, 5)					# tyre temp RL
			printAt('{:6.1f}'.format(struct.unpack('f', ddata[0x6C:0x6C+4])[0]), 7, 5)					# tyre temp RR
			
			#printAt(tyreTempFL, 20, 5)
			# If temp is high play sound and delay
			
			if tyreTempFL > 70.0 or tyreTempFR > 70.0 or tyreTempRL > 70.0 or tyreTempRR > 70.0:
				
				if overTemp == 0:
					printAt('TYRE TEMPERATURE WARNING!!!!!', 9, 1, bold=1)
					tyreMessage = 0
					tyreMessage = random.randint(1,3)
					#printAt(, 9, 1, bold=1)
					if tyreMessage == 1:
						if language == "EN":
							play_obj1 = wave_obj1.play()
							play_obj1.wait_done()
						else:
							play_obj4 = wave_obj4.play()
							play_obj4.wait_done()
					if tyreMessage == 2:
						if language == "EN":
							play_obj2 = wave_obj2.play()
							play_obj2.wait_done()
						else:
							play_obj5 = wave_obj5.play()
							play_obj5.wait_done()
					if tyreMessage == 3:
						if language == "EN":
							play_obj3 = wave_obj3.play()
							play_obj3.wait_done()
						else:
							play_obj6 = wave_obj6.play()
							play_obj6.wait_done()
					overTemp = 1

				#Play sound and delay
				#printAt('TYRE TEMPERATURE WARNING!!!!!', 9, 1, bold=1)
				#printAt('                             ', 9, 1, bold=1)

			else:
				printAt('                             ', 9, 1, bold=1)
				overTemp = 0	
			
		if pknt > 100:
			send_hb(s)
			pknt = 0
	except Exception as e:
		printAt('Exception: {}'.format(e), 41, 1, reverse=1)
		send_hb(s)
		pknt = 0
		pass

	sys.stdout.flush()
