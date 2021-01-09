#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from enum import Enum


SERVER_NAME = '@mRadioStation'
SERVER_VERSION = '0.1.1'

PORT = 1212

config = {
    '/': {'link': ''},
    '/info': {'command':'mocp -i'},
    '/357': {'link': 'http://n09a-eu.rcs.revma.com/ye5kghkgcm0uv'},
    '/muzo': {'link': 'http://n05a-eu.rcs.revma.com/1nnezw8qz7zuv'},
    '/ns': {'link': 'http://stream.rcs.revma.com/ypqt40u0x1zuv'},
    '/stop': {'command': 'mocp -s'},
    '/shutdown': {'command': 'sudo poweroff'}
}


class Response(Enum):
    OK = dict(code=200, msg='-> Hello world!\n----------------------------\nAvailable URIs: \n{0}'.format(
        ' \n'.join(sorted(config.keys(), reverse=False))))
    FAIL = dict(code=404, msg='Something is wrong here.')


class RadioStationHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        self.server_version = SERVER_NAME
        self.sys_version = SERVER_VERSION
        output = ''

        if self.path in config.keys():
            response = Response.OK
            x = config.get(self.path)
            if 'command' in x:
                output = run_command(x.get('command'))
            if 'link' in x:
                play_link(x.get('link'))
        else:
            response = Response.FAIL

        self.send_response(response.value['code'])
        self.send_header("Content-type", "text/plain; charset=utf-8")

        self.end_headers()
        o = response.value['msg'] + '\n----------------------------\n' + output
        self.wfile.write(o.encode())
        return


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def run_command(command):
    if command.strip():
        if 'mocp -i' in command:
            return subprocess.getoutput(command)
        else:
            os.system(command)
        return ""


def play_link(link):
    if link.strip():
        os.system('mocp -l {}'.format(link))
    pass


def check_moc_is_running():
    r = os.system('pidof mocp >> /dev/null')
    if r > 0:
        print('Moc is not installed or server is not running...\nExiting...')
        sys.exit(0)
    pass


def main(argv):
    check_moc_is_running()
    run(HTTPServer, RadioStationHandler)


if __name__ == "__main__":
    main(sys.argv)
