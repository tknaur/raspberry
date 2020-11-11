#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from enum import Enum

SERVER_NAME = '@mRadioStation'
SERVER_VERSION = '0.1'

PORT = 1212

config = {
    '/': {'link': ''},
    '/muzo': {'link': 'http://n05a-eu.rcs.revma.com/1nnezw8qz7zuv'},
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

        if self.path in config.keys():
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
    if command.strip():
        os.system(command)
    pass


def play_link(link):
    if link.strip():
        os.system('mocp -l {}'.format(link))
    pass


def check_moc_is_running():
    r = os.system('pidof mocp >> /dev/null')
    if r > 0:
        print('Moc is not installed or the server is not running...\nExiting...')
        sys.exit(0)
    pass


def main(argv):
    check_moc_is_running()
    run(HTTPServer, RadioStationHandler)


if __name__ == "__main__":
    main(sys.argv)
