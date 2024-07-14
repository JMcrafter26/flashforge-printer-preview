from protocol import get_info
from protocol import get_head_position
from protocol import get_temp
from protocol import get_progress
from protocol import get_status

from socket import getaddrinfo, gethostname
import ipaddress
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re


def jsonify(printer_info):
    return printer_info


def info(ip_address, PORT):
    printer_info = get_info({'ip': ip_address, 'port': PORT})
    return jsonify(printer_info)


def head_location(ip_address, PORT):
    printer_info = get_head_position({'ip': ip_address, 'port': PORT})
    return jsonify(printer_info)


def temp(ip_address, PORT):
    printer_info = get_temp({'ip': ip_address, 'port': PORT})
    return jsonify(printer_info)


def progress(ip_address, PORT):
    printer_info = get_progress({'ip': ip_address, 'port': PORT})
    return jsonify(printer_info)


def status(ip_address, PORT):
    printer_info = get_status({'ip': ip_address, 'port': PORT})
    return jsonify(printer_info)

def stopProgram(ip_address, PORT):
    print('Stopping the program ...')
    # shut down the server
    # os._exit(0)
    exit()

# get the ip and port from the arguments
ip = '0.0.0.0'
port = 8899


commands = {
    'info': info,
    'head-location': head_location,
    'temp': temp,
    'progress': progress,
    'status': status,
    'stop': stopProgram
}

# start a http server that listens for requests


# get the command from the request path
# structure: localhost:8899/command?ip=0.0.0.0&port=(optional)8899
def get_command(path):
    result = re.search(r'/(\w+)', path)
    if result == None:
        return None
    return result.group(1)

def get_ip_and_port(path):
    # get the ip and port from the request path
    result = re.search(r'ip=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', path)
    if result is None:
        return None, None
    ip = result.group(1)
    result = re.search(r'port=(\d{1,5})', path)
    if result is None:
        port = 8899
    else:
        port = result.group(1)
    return ip, port

def getResponse(command, ip, port):
    if command in commands:
        return commands[command](ip, port)
    return None


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # get the command from the path
        command = get_command(self.path)
        ip, port = get_ip_and_port(self.path)
        print(f'Command: {command} | IP: {ip} | Port: {port}')
        # call the function that corresponds to the command
        if command in commands:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = getResponse(command, ip, port)
            if response is None:
                self.wfile.write(json.dumps({'error': 'Invalid IP or port'}).encode())
            else:
                try:
                    self.wfile.write(json.dumps(response).encode())
                except:
                    self.wfile.write(json.dumps({'error': 'Invalid IP or port'}).encode())



        elif command is None:
            # serve index.html
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with open('index.html', 'r') as file:
                self.wfile.write(file.read().encode())
                
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Command not found'}).encode())



def get_ip(ip_addr_proto="ipv4", ignore_local_ips=True):
    # By default, this method only returns non-local IPv4 addresses
    # To return IPv6 only, call get_ip('ipv6')
    # To return both IPv4 and IPv6, call get_ip('both')
    # To return local IPs, call get_ip(None, False)
    # Can combine options like so get_ip('both', False)

    af_inet = 2
    if ip_addr_proto == "ipv6":
        af_inet = 30
    elif ip_addr_proto == "both":
        af_inet = 0

    system_ip_list = getaddrinfo(gethostname(), None, af_inet, 1, 0)
    ip_list = []

    for ip in system_ip_list:
        ip = ip[4][0]

        try:
            ipaddress.ip_address(str(ip))
            ip_address_valid = True
        except ValueError:
            ip_address_valid = False
        else:
            if ipaddress.ip_address(ip).is_loopback and ignore_local_ips or ipaddress.ip_address(ip).is_link_local and ignore_local_ips:
                pass
            elif ip_address_valid:
                ip_list.append(ip)

    return ip_list


def run():
    
    # get the ip address of the machine
    ip = get_ip()
    if len(ip) == 0:
        print('No valid ip address found, exiting ...')
        exit()
    # if first ip ends with .1, use the second one
    if ip[0].endswith('.1'):
        ip = ip[1]
    else:
        ip = ip[0]
    # server_address = str(ip) + ':' + str(port)
    # convert the ip to tuple
    server_address = (ip, port)
    print('Server address: ' + str(server_address))

    try:
        httpd = HTTPServer(server_address, RequestHandler)
    except OSError:
        print('Server already running, stopping it ...')
    # no cors
    httpd.allow_reuse_address = True

    print('Starting http server on http://' + str(ip) + ':' + str(port))

    httpd.serve_forever()

run()