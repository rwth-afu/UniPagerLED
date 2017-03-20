#!/usr/bin/env python3

import websocket
import json
import time
import argparse

class Statusleds:
	def __init__(self, url, betrled, verbled, txled):
		self.bled = betrled
		self.vled = verbled
		self.txled = txled
		self.ws = websocket.create_connection(url)
		self.setled(self.bled, True)
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.setled(self.bled, False)
		self.ws.close()
	
	def setled(self, led, status):
		if led == -1:
			print("Led -1 not present")
		print("Setting led %d to %d" % (led, status))

	def setstatus(self):
		self.ws.send('"GetStatus"')
		sres = self.ws.recv()
		res = json.loads(sres)
		print("Resp:")
		print(json.dumps(res,indent=4))
		status = res["Status"]
		self.setled(self.vled, status["connected"])
		self.setled(self.txled, status["transmitting"])
	
	def loop(self):
		while True:
			self.setstatus()
			time.sleep(1)

parser = argparse.ArgumentParser(description='Set status LEDs')
parser.add_argument('--host', default='localhost',
                    help='The host running RustPager')
parser.add_argument('--port', '-p', default='8055',
                    help='The port RustPager is listening')
parser.add_argument('--betrieb', '-b', dest='betrled', default=-1, type=int,
                    help='The led number of the "Betrieb" led')
parser.add_argument('--verbindung', '-v', dest='verbled', default=-1, type=int,
                    help='The led number of the "Verbindung" led')
parser.add_argument('--tx', '-t', dest='txled', default=-1, type=int,
                    help='The led number of the "TX" led')

args = parser.parse_args()
print(args)

with Statusleds("ws://%s:%s/" %(args.host, args.port), args.betrled, args.verbled, args.txled) as setter:
	setter.loop()
