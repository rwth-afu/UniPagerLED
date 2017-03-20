#!/usr/bin/env python3

import websocket
import json

ws = websocket.create_connection("ws://c9000.db0sda.ampr.org:8055/")
print("Sending version request")
ws.send('"GetVersion"')
print("Sent")
print("Recieving")
res = ws.recv()
print("Recieved: %s" % res)
jres = json.loads(res)
print("Version: %s" % jres["Version"])
ws.close()
