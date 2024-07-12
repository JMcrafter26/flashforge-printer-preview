# Flashforge Finder Api
# Author: 01F0
# URL: https://github.com/01F0/flashforge-finder-api

# This code was minified to save space. If you want to read the code, please read the original files.


_B='port'
_A='ip'
import re,socket,sys
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
def send_and_receive(printer_adress,message_data):B=printer_adress;A=socket.socket();A.settimeout(TIMEOUT_SECONDS);A.connect((B[_A],B[_B]));A.send(message_data.encode());C=A.recv(BUFFER_SIZE);A.close();return C.decode()
def jsonify(printer_info):return printer_info
def info(ip_address,PORT):A=get_info({_A:ip_address,_B:PORT});return jsonify(A)
def head_location(ip_address,PORT):A=get_head_position({_A:ip_address,_B:PORT});return jsonify(A)
def temp(ip_address,PORT):A=get_temp({_A:ip_address,_B:PORT});return jsonify(A)
def progress(ip_address,PORT):A=get_progress({_A:ip_address,_B:PORT});return jsonify(A)
def status(ip_address,PORT):A=get_status({_A:ip_address,_B:PORT});return jsonify(A)
ip='0.0.0.0'
port=8899
if len(sys.argv)<2:print('Available commands: info, head-location, temp, progress, status');print('Use -ip and -port flags to specify the printer IP and port');sys.exit(1)
command=sys.argv[1]
if'-ip'in sys.argv:ip=sys.argv[sys.argv.index('-ip')+1]
if'-port'in sys.argv:port=int(sys.argv[sys.argv.index('-port')+1])
commands={'info':info,'head-location':head_location,'temp':temp,'progress':progress,'status':status}
print(commands[command](ip,port))