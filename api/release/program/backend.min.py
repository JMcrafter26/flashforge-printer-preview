# Flashforge Printer Preview
# Author: JMcrafter26
# URL: https://github.com/JMcrafter26/flashforge-printer-preview.git

# This code was minified to save space. If you want to read the code, please read the original files.


_C='port'
_B='ip'
_A=None
import re,socket
from socket import getaddrinfo,gethostname
import ipaddress
from http.server import BaseHTTPRequestHandler,HTTPServer
import json
request_control_message='~M601 S1\r\n'
request_info_message='~M115\r\n'
request_head_position='~M114\r\n'
request_temp='~M105\r\n'
request_progress='~M27\r\n'
request_status='~M119\r\n'
def get_info(printer_address):
	A=printer_address;send_and_receive(A,request_control_message);D=send_and_receive(A,request_info_message);B={};E=['Type','Name','Firmware','SN','X','Tool Count']
	for C in E:F=regex_for_field(C);B[C]=re.search(F,D).groups()[0]
	return B
def get_head_position(printer_address):
	A=printer_address;send_and_receive(A,request_control_message);D=send_and_receive(A,request_head_position);B={};E=['X','Y','Z']
	for C in E:F=regex_for_coordinates(C);B[C]=re.search(F,D).groups()[0]
	return B
def get_temp(printer_address):A=printer_address;send_and_receive(A,request_control_message);B=send_and_receive(A,request_temp);C=regex_for_current_temperature();D=regex_for_target_temperature();E=re.search(C,B).groups()[0];F=re.search(D,B).groups()[0];return{'Temperature':E,'TargetTemperature':F}
def get_progress(printer_address):
	B=printer_address;send_and_receive(B,request_control_message);F=send_and_receive(B,request_progress);C=re.search(regex_for_progress(),F).groups();D=int(C[0]);A=int(C[1])
	if A==0:E=0
	else:E=int(float(D)/A*100)
	return{'BytesPrinted':D,'BytesTotal':A,'PercentageCompleted':E}
def get_status(printer_address):
	A=printer_address;send_and_receive(A,request_control_message);D=send_and_receive(A,request_status);B={};E=['Status','MachineStatus','MoveMode','Endstop']
	for C in E:F=regex_for_field(C);B[C]=re.search(F,D).groups()[0]
	return B
def regex_for_field(field_name):return field_name+': ?(.+?)\\r\\n'
def regex_for_coordinates(field_name):return field_name+':(.+?) '
def regex_for_current_temperature():return'T0:(-?[0-9].*?) '
def regex_for_target_temperature():return'\\/(-?[0-9].*?) '
def regex_for_progress():return'([0-9].*)\\/([0-9].*?)\\r'
BUFFER_SIZE=1024
TIMEOUT_SECONDS=5
def send_and_receive(printer_adress,message_data):B=printer_adress;A=socket.socket();A.settimeout(TIMEOUT_SECONDS);A.connect((B[_B],B[_C]));A.send(message_data.encode());C=A.recv(BUFFER_SIZE);A.close();return C.decode()
def jsonify(printer_info):return printer_info
def info(ip_address,PORT):A=get_info({_B:ip_address,_C:PORT});return jsonify(A)
def head_location(ip_address,PORT):A=get_head_position({_B:ip_address,_C:PORT});return jsonify(A)
def temp(ip_address,PORT):A=get_temp({_B:ip_address,_C:PORT});return jsonify(A)
def progress(ip_address,PORT):A=get_progress({_B:ip_address,_C:PORT});return jsonify(A)
def status(ip_address,PORT):A=get_status({_B:ip_address,_C:PORT});return jsonify(A)
def stopProgram(ip_address,PORT):print('Stopping the program ...');exit()
ip='0.0.0.0'
port=8899
commands={'info':info,'head-location':head_location,'temp':temp,'progress':progress,'status':status,'stop':stopProgram}
def get_command(path):
	A=re.search('/(\\w+)',path)
	if A==_A:return
	return A.group(1)
def get_ip_and_port(path):
	A=re.search('ip=(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})',path)
	if A is _A:return _A,_A
	C=A.group(1);A=re.search('port=(\\d{1,5})',path)
	if A is _A:B=8899
	else:B=A.group(1)
	return C,B
def getResponse(command,ip,port):
	A=command
	if A in commands:return commands[A](ip,port)
class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(A):
		G='Invalid IP or port';H='application/json';C='error';D='*';E='Access-Control-Allow-Origin';F='Content-type';B=get_command(A.path);I,J=get_ip_and_port(A.path);print(f"Command: {B} | IP: {I} | Port: {J}")
		if B in commands:
			A.send_response(200);A.send_header(F,H);A.send_header(E,D);A.end_headers();K=getResponse(B,I,J)
			if K is _A:A.wfile.write(json.dumps({C:G}).encode())
			else:
				try:A.wfile.write(json.dumps(K).encode())
				except:A.wfile.write(json.dumps({C:G}).encode())
		elif B is _A:
			A.send_response(200);A.send_header(F,'text/html');A.send_header(E,D);A.end_headers()
			with open('index.html','r')as L:A.wfile.write(L.read().encode())
		else:A.send_response(404);A.send_header(F,H);A.send_header(E,D);A.end_headers();A.wfile.write(json.dumps({C:'Command not found'}).encode())
def get_ip(ip_addr_proto='ipv4',ignore_local_ips=True):
	C=ignore_local_ips;D=ip_addr_proto;B=2
	if D=='ipv6':B=30
	elif D=='both':B=0
	G=getaddrinfo(gethostname(),_A,B,1,0);E=[]
	for A in G:
		A=A[4][0]
		try:ipaddress.ip_address(str(A));F=True
		except ValueError:F=False
		else:
			if ipaddress.ip_address(A).is_loopback and C or ipaddress.ip_address(A).is_link_local and C:0
			elif F:E.append(A)
	return E
def run():
	A=get_ip()
	if len(A)==0:print('No valid ip address found, exiting ...');exit()
	if A[0].endswith('.1'):A=A[1]
	else:A=A[0]
	B=A,port;print('Server address: '+str(B))
	try:C=HTTPServer(B,RequestHandler)
	except OSError:print('Server already running, stopping it ...')
	C.allow_reuse_address=True;print('Starting http server on http://'+str(A)+':'+str(port));C.serve_forever()
run()