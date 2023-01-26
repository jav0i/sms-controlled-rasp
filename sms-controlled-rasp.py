#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time
Import os

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)


ser = serial.Serial("/dev/ttyS0",115200)
ser.flushInput()

phone_number = '' # +639xx xxx xxxx phone number to text
text_message = ''
power_key = 6
rec_buff = ''


def send_at(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(timeout)
	
	if ser.inWaiting():
		time.sleep(0.01 )
		rec_buff = ser.read(ser.inWaiting())
	if rec_buff != '':
		print(rec_buff.decode())
		if 'red' in rec_buff.decode(): GPIO.output(21, GPIO.HIGH), time.sleep(3), GPIO.output(21, GPIO.LOW)
		if back not in rec_buff.decode():print(command + ' back:\t' + rec_buff.decode())
		return 0
	else:
		global TEXTDATA
		TEXTDATA = str(rec_buff)
		print(TEXTDATA)
		return 1
	
	
def ReceiveShortMessage():
	rec_buff = ''
	send_at('AT+CMGF=1','OK',1)
	send_at('AT+CMGL="REC UNREAD"', 'OK', 1)
	answer = send_at('AT+CMGL="REC UNREAD"', '+CMTI', 1)
	
	if 1 == answer:
		answer = 0
		if 'start-kali' in rec_buff:
			answer = 1
			os.system("/bin/bash -e /root/start-remote-kali.sh")
	else:
		print('No New text')
		return False
	return True

def power_on(power_key):
	print('SIM7600X is starting:')
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(power_key,GPIO.OUT)
	time.sleep(0.1)
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(20)
	ser.flushInput()
	print('SIM7600X is ready')

def power_down(power_key):
	print('SIM7600X is loging off:')
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(3)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(18)
	print('Good bye')

power_on(power_key)
while True:
	
	ReceiveShortMessage()
