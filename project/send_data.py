#!usr/bin/python
import serial
import time

def open_serial():
    port = "/dev/ttyS0" #should be correct serial port I hopes
    baudrate = 115200
    ser = serial.Serial(port, baudrate, timeout=1) #keep timeout for sending low
    ser.flushInput()
    ser.flushOutput()
    return ser

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

def send_message(serial_port, confirm, nbtrials, message):
    time.sleep(0.1)
    hex_msg = encode_msg(message)
    hex_msg_length = len(hex_msg)
    serial_port.write(("AT+DTRX="+ str(confirm) + "," + str(nbtrials) + "," + str(hex_msg_length) + "," + str(hex_msg)+ "\r\n").encode())
    
#convert messages from String to Hex
def encode_msg(message):
    byte_array = bytearray(message, 'utf-8')
    hex_string = ''.join(format(byte, '02x') for byte in byte_array)
    return hex_string

#example for testing
#ser = open_serial()
#send_message(ser,0,0,"1")
#print(wait_response(ser, 5))

#this should return:
#"OK+SEND:XY" with X and Y hex representation of how many bytes were sent