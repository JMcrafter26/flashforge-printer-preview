# Flashforge Printer Preview
# Author: JMcrafter26
# URL: https://github.com/JMcrafter26/flashforge-printer-preview.git



import re
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

#! packets.py
request_control_message = '~M601 S1\r\n'
request_info_message = '~M115\r\n'
request_head_position = '~M114\r\n'
request_temp = '~M105\r\n'
request_progress = '~M27\r\n'
request_status = '~M119\r\n'

#! protocol.py



def get_info(printer_address):
    """ Returns an object with basic printer information such as name etc."""

    send_and_receive(printer_address, request_control_message)
    info_result = send_and_receive(printer_address, request_info_message)

    printer_info = {}
    info_fields = ['Type', 'Name', 'Firmware', 'SN', 'X', 'Tool Count']
    for field in info_fields:
        regex_string = regex_for_field(field)
        printer_info[field] = re.search(regex_string, info_result).groups()[0]

    return printer_info

def get_head_position(printer_address):
    """ Returns the current x/y/z coordinates of the printer head. """

    send_and_receive(printer_address, request_control_message)
    info_result = send_and_receive(printer_address, request_head_position)

    printer_info = {}
    printer_info_fields = ['X', 'Y', 'Z']
    for field in printer_info_fields:
        regex_string = regex_for_coordinates(field)
        printer_info[field] = re.search(regex_string, info_result).groups()[0]

    return printer_info

def get_temp(printer_address):
    """ Returns printer temp. Both targeted and current. """

    send_and_receive(printer_address, request_control_message)
    info_result = send_and_receive(printer_address, request_temp)

    regex_temp = regex_for_current_temperature()
    regex_target_temp = regex_for_target_temperature()
    temp = re.search(regex_temp, info_result).groups()[0]
    target_temp = re.search(regex_target_temp, info_result).groups()[0]

    return {'Temperature': temp, 'TargetTemperature': target_temp}

def get_progress(printer_address):
    send_and_receive(printer_address, request_control_message)
    info_result = send_and_receive(printer_address, request_progress)

    regex_groups = re.search(regex_for_progress(), info_result).groups()
    printed = int(regex_groups[0])
    total = int(regex_groups[1])

    if total == 0:
        percentage = 0
    else:
        percentage = int(float(printed) / total * 100)

    return {'BytesPrinted': printed,
            'BytesTotal': total,
            'PercentageCompleted': percentage}

def get_status(printer_address):
    """ Returns the current printer status. """

    send_and_receive(printer_address, request_control_message)
    info_result = send_and_receive(printer_address, request_status)

    printer_info = {}
    printer_info_fields = ['Status', 'MachineStatus', 'MoveMode', 'Endstop']
    for field in printer_info_fields:
        regex_string = regex_for_field(field)
        printer_info[field] = re.search(regex_string, info_result).groups()[0]

    return printer_info

#! regex_patterns.py
def regex_for_field(field_name):
    """Machine Type: Flashforge Finder"""

    return field_name + ': ?(.+?)\\r\\n'

def regex_for_coordinates(field_name):
    """ X:-19.19 Y:6 Z:7.3 A:846.11 B:0 """
    return field_name + ':(.+?) '

def regex_for_current_temperature():
    """T0:210 /210 B:0 /0"""

    return 'T0:(-?[0-9].*?) '

def regex_for_target_temperature():
    """ T0:210 /210 B:0 /0 """

    return '\/(-?[0-9].*?) '

def regex_for_progress():
    """ T0:210 /210 B:0 /0 """

    return '([0-9].*)\/([0-9].*?)\\r'

#! socket_handler.py

BUFFER_SIZE = 1024
TIMEOUT_SECONDS = 5

def send_and_receive(printer_adress, message_data):
    """Sends and receives data"""

    printer_socket = socket.socket()
    printer_socket.settimeout(TIMEOUT_SECONDS)
    printer_socket.connect((printer_adress['ip'], printer_adress['port']))
    printer_socket.send(message_data.encode())
    data = printer_socket.recv(BUFFER_SIZE)
    printer_socket.close()

    return data.decode()


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
    exit()

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


def get_command(path):
    result = re.search(r'/(\w+)', path)
    if result == None:
        return None
    return result.group(1)

def get_ip_and_port(path):
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
        command = get_command(self.path)
        ip, port = get_ip_and_port(self.path)
        print(f'Command: {command} | IP: {ip} | Port: {port}')
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

def run():
    server_address = ('localhost', 8899)
    try:
        httpd = HTTPServer(server_address, RequestHandler)
    except OSError:
        print('Server already running, stopping it ...')
    httpd.allow_reuse_address = True

    print('Starting http server on http://localhost:8899')

    httpd.serve_forever()

run()