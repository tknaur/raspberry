#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from enum import Enum
import os

SERVER_NAME='@mRadioStation'
SERVER_VERSION='0.1'

PORT=1212

config = {
	'/' : {'link': ''},
	'/hello': {'command': ''},
	'/muzo': {'link': 'http://muzo'},
	'/ns': {'link': 'http://stream.rcs.revma.com/ypqt40u0x1zuv'},
	'/stop': {'command': 'mocp -s'},
	'/shutdown': {'command': 'sudo poweroff'}
	}

class Response(Enum):
	OK = {'code': 200, 'msg': 'Hello world!\n\nAvailable URIs: \n' + ' \n'.join(config.keys())}
	FAIL = {'code': 404, 'msg': 'Something is wrong here.'}


class RadioStationHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.server_version = SERVER_NAME
		self.sys_version = SERVER_VERSION

		#print(self.path)

		if (self.path in config.keys()):
			response = Response.OK
			x = config.get(self.path)

			if 'command' in x:
				run_command(x.get('command'))
			if 'link' in x:
				play_link(x.get('link'))	
			
		else:
			response = Response.FAIL
	

		self.send_response(response.value['code'])
		self.send_header("Content-type", "text/plain")

		self.end_headers()
		self.wfile.write(response.value['msg'].encode())

		return


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
	server_address = ('', PORT)
	httpd = server_class(server_address, handler_class)
	httpd.serve_forever()


def run_command(command):
	print ("run command " + str(command))
	pass

def play_link(link):
	print ("play link "  + str(link))
	pass

def check_mocp():
	pass


def main(argv):
	run(HTTPServer, RadioStationHandler)

if __name__ == "__main__":
	main(sys.argv)
