from protocol import get_info
from protocol import get_head_position
from protocol import get_temp
from protocol import get_progress
from protocol import get_status

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

# get the ip and port from the arguments
import sys
ip = '0.0.0.0'
port = 8899

# if no command is provided, print an error message
if len(sys.argv) < 2:
    print('Available commands: info, head-location, temp, progress, status')
    print('Use -ip and -port flags to specify the printer IP and port')
    sys.exit(1)


# get the command from the arguments and the -ip and -port flags
command = sys.argv[1]
if '-ip' in sys.argv:
    ip = sys.argv[sys.argv.index('-ip') + 1]
if '-port' in sys.argv:
    port = int(sys.argv[sys.argv.index('-port') + 1])

# call the correct function based on the command
commands = {
    'info': info,
    'head-location': head_location,
    'temp': temp,
    'progress': progress,
    'status': status
}
print(commands[command](ip, port))
