#!/usr/bin/env python3

import websocket
import json
import time
import argparse
import signal
import sys
import RPi.GPIO as GPIO

presets = {"c9000": {
	"run": 24,
	"conn": 26,
	"tx": None
}}

presetconfigmap = {"C9000":"c9000"}

class Statusleds:
	def __init__(self, url, runled, connled, txled):
		self.runled = runled
		self.connled = connled
		self.txled = txled
		
		self.ws = websocket.create_connection(url, timeout=10)
		
		if runled == connled == txled == None:
			self.ws.send('"GetConfig"')
			sconfig = self.ws.recv()
			config = json.loads(sconfig)
			print("Config:")
			print(json.dumps(config,indent=4))
			transmitter = config["Config"]["transmitter"]
			if transmitter in presetconfigmap:
				self.runled = presets[presetconfigmap[transmitter]]["run"]
				self.connled = presets[presetconfigmap[transmitter]]["conn"]
				self.txled = presets[presetconfigmap[transmitter]]["tx"]
		
		GPIO.setmode(GPIO.BOARD)
		if not self.runled is None:
			GPIO.setup(abs(self.runled), GPIO.OUT)
		if not self.connled is None:
			GPIO.setup(abs(self.connled), GPIO.OUT)
		if not self.txled is None:
			GPIO.setup(abs(self.txled), GPIO.OUT)
		
		self.setled(self.runled, True)
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.setled(self.runled, False)
		GPIO.cleanup()
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
		self.setled(self.connled, status["connected"])
		self.setled(self.txled, status["transmitting"])
	
	def loop(self):
		self.getstatus()
		while True:
			self.setstatus()

parser = argparse.ArgumentParser(description='Set status LEDs')
parser.add_argument('--hostname', default='localhost',
                    help='The host running RustPager, default localhost')
parser.add_argument('--port', default='8055',
                    help='The port RustPager is listening, default 8055')
parser.add_argument('--gpioRun', dest='runled', default=None, type=int,
                    help='UniPager running')
parser.add_argument('--gpioConn', dest='connled', default=None, type=int,
                    help='DAPNET connection ok')
parser.add_argument('--gpioTX', dest='txled', default=None, type=int,
                    help='Transmitting')
parser.add_argument('--preset', dest='preset', default=None, type=str,
                    help='Preset, help for help')

args = parser.parse_args()

preset = args.preset

if not preset is None:
	if preset == "help":
		print("Presets:")
		for pr in presets:
			print("%s:" %pr)
			for t in ["run","conn","tx"]:
				print("  %s: %s" %(t, presets[pr][t]))
		sys.exit(0)
	elif preset in presets:
		runled = presets[preset]["run"]
		connled = presets[preset]["conn"]
		txled = presets[preset]["tx"]
	else:
		print("Preset %s unknown" %preset)
		sys.exit(1)
else:
	runled = args.runled
	connled = args.connled
	txled = args.txled

while True:
	try:
		with Statusleds("ws://%s:%s/" %(args.hostname, args.port), runled, connled, txled) as setter:

			setter.loop()
	except websocket._exceptions.WebSocketTimeoutException:
		print("Timeout")
	except websocket._exceptions.WebSocketConnectionClosedException:
		print("Websocket closed")
	except ConnectionRefusedError:
		print("Connection Refused")
	except KeyboardInterrupt:
		print("Shutting down")
		sys.exit(0)
	
	print("Waiting 10 seconds")
	try:
		time.sleep(10)
	except KeyboardInterrupt:
		print("Shutting down")
		sys.exit(0)
	print("Trying again")

