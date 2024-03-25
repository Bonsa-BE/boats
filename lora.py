#!usr/bin/python
import serial
import time

port = "/dev/ttyS0" #should be correct serial port I hopes
baudrate = 115200
time_out = 7000 #timeout for listening in ms, doesn't do much tbh
ser = serial.Serial(port, baudrate, timeout=1) #keep timeout for sending low
ser.flushInput()
ser.flushOutput()

def wait_response(serial_port, time_out):
	response=""
	start = time.time()*1000
	while True:
		current_millis = time.time()*1000
		if serial_port.in_waiting or (current_millis - start) < time_out:
			msg = serial_port.readline().decode()
			response += msg
		else:
			break
	return response

#TO DO: use this fucntion to write cleaner code
def send_command(command):
    time.sleep(0.1)
    ser.write(("AT+" + command + "\r\n").encode())
    print(wait_response(ser, 7))
    
#check connection by sending an empty AT command.
ser.write(b"AT\r\n")
time.sleep(0.1)
print(wait_response(ser, 7))
#This should return "+AT: OK"

#set Join Mode to OTAA (Over The Air Activation)
send_command("CJOINMODE=0")
#this should return: "OK"

#manually set DEVEUI to what the Digita network expects
send_command("CDEVEUI=05B18B2C5428A0DA")
#This should return: "OK"

#manually set APPEUI (now JOINEUI) to what Digita network expects
send_command("CAPPEUI=0000000000000000")
#This should return: "OK"

#manually set APPKEY to what Digita network expects
send_command("CAPPKEY=00000000000000000000000000000000") #16 byte address
#This should return: "OK"

#manually set frequency band mask
send_command("CFREQBANDMASK=0001") #4 byte address
#This should return: "OK"

#manually set upload/downloadmode on different frequencies
send_command("CULDLMODE=2") #1 = same, 2 = different frequency
#This should return: "OK"

#manually set the workmode to "Normal"
send_command("CWORKMODE=2") #only this option is supported
#This should return: "OK"


#for lowest energy consumption we will use this device as a class A
send_command("CCLASS=0") #0 = CLASS A, 1 = CLASS B, 2 = CLASS C
#This should return: "OK"

#get battery level
send_command("CBL?") 
#this should return: "+CBL:x" with x = battery percentage
#if no battery is present this will return: "CBL:100"

send_command("CSTATUS?\r\n") 
#status response overview
#00 = no data operation
#01 = data sending
#02 = data sending failed
#03 = data sending success
#04 join succes
#05 join fail
#06 netowkr may abnormal (res from Link Check)
#07 data sent success, no download
#08 data sent success, yes download

#Try to join the network with OTAA
send_command("CJOIN=1,1,10,8")
#this should return: "OK"

#Set up for uplink confirmation for messaging:
send_command("CCONFIRM=1") #1 =confirm, 0 = unconfirm uplink message
#this should return: "OK"

#Set up application port
send_command("CAPPPORT=5") #decimal number in [1:223], 0x00 is reserved for LoRaWAN MAC command
#this should return: "OK"

#Set up spreading factor and datarate
send_command("CDATARATE=5") #decimal number in [0:5], higher number = lower SF
#this should return: "OK"

#inquire RSSI
send_command("CRSSI FREQBANDIDX?")
#this should return a list x:<RSSI value> with x decimal number in [0:7]
#this lists the RSSI for all the frequency channels set previously with command "CFREQBANDMASK"

#Set number of trials for sending data
send_command("CNBTRIALS=1,3") #first number 1 = confirm, 0 = uncomfirm package, second number in range [1:15] sets number of trials
#this should return: "OK"

#Set report mode
send_command("CTXP=0,0")#first number 0 = non periodic, 1 = periodic data reporting, second number sets period (dependant on datarate)
#this should return: "OK"

#Set TX power
send_command("CTXP=0")#0 = 17dBm
#this should return: "OK"

#Set linkcheck
send_command("CLINKCHECK=2")#0 = disable, 1 = one time, 2 each time check link after sending data
#this should return: "OK"

#enable ADR
send_command("CADR=1")#0 = disable, 1 = enable ADR (adaptive data rate) function
#this should return: "OK"

#set RX-window parameter
send_command("CRXP=0,0,869525000")#first nr = offset left, second nr = offset right, third nr = frequency
#this should return: "OK"

#set receive delay
send_command("CRX1DELAY=2")#decimal number for amount of seconds to hold receive window open
#this should return: "OK"

#save all parameters
send_command("CSAVE")
#this should return: "OK"

#send a testframe of data
send_command("DTRX=1,3,10,0123456789")
#this should return:
#"OK+SEND:03"
#"OK+SENT:01"
#"OK+RECV:02,01,00"

send_command("DRX?")

ser.close()

