#!/usr/bin/env python3

import websocket
import json
import time
import argparse
import RPi.GPIO as GPIO

class Statusleds:
	def __init__(self, url, betrled, verbled, txled):
		self.bled = betrled
		self.vled = verbled
		self.txled = txled
		
		GPIO.setmode(GPIO.BOARD)
		if not self.bled is None:
			GPIO.setup(self.bled, GPIO.OUT)
		if not self.vled is None:
			GPIO.setup(self.vled, GPIO.OUT)
		if not self.txled is None:
			GPIO.setup(self.txled, GPIO.OUT)
		
		self.ws = websocket.create_connection(url)
		
		self.setled(self.bled, True)
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.setled(self.bled, False)
		self.ws.close()
	
	def setled(self, led, status):
		if led == None:
			print("Led not present")
			return
		if led < 0:
			led = -led
			status = not status
		print("Setting led %d to %d" % (led, status))
		GPIO.output(led, status)
	
	def getstatus(self):
		self.ws.send('"GetStatus"')

	def setstatus(self):
		sres = self.ws.recv()
		res = json.loads(sres)
		print("Resp:")
		print(json.dumps(res,indent=4))
		try:
			status = res["Status"]
		except KeyError:
			print("Other message, ignoring")
			return
		self.setled(self.vled, status["connected"])
		self.setled(self.txled, status["transmitting"])
	
	def loop(self):
		self.getstatus()
		while True:
			self.setstatus()
			time.sleep(1)

parser = argparse.ArgumentParser(description='Set status LEDs')
parser.add_argument('--hostname', default='localhost',
                    help='The host running RustPager')
parser.add_argument('--port', default='8055',
                    help='The port RustPager is listening')
parser.add_argument('--gpioRun', dest='betrled', default=None, type=int,
                    help='UniPager running')
parser.add_argument('--gpioConn', dest='verbled', default=None, type=int,
                    help='DAPNET connection ok')
parser.add_argument('--gpioTX', dest='txled', default=None, type=int,
                    help='Transmitting')

args = parser.parse_args()
print(args)

with Statusleds("ws://%s:%s/" %(args.hostname, args.port), args.betrled, args.verbled, args.txled) as setter:
	setter.loop()
