import os
import sys
import socket

from bottle import default_app, post, response, request, route

LIVESTATUS_HOST = '127.0.0.1'
LIVESTATUS_PORT = 6557

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = ""
    while True:
        part = sock.recv(BUFF_SIZE)
        if part:
            data += part
        else:
            break
    return data

def get_data(query):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((LIVESTATUS_HOST, LIVESTATUS_PORT))

    print "Sending query to Livestatus socket..."
    print
    print query # this goes to Apache log file only, not to client

    s.send(query)

    answer = recvall(s)

    return answer

@route('/', method='POST')
def bridge_lql():

    print "Receiving query from client..."
    print

    postdata = request.body.readlines()

    print postdata # this goes to Apache log file only, not to client

    found_output_format = False

    _query = []

    for line in postdata:

        if not 'outputformat' in line.lower():
            _query.append(line.replace('\n', ' ').replace('\r', ''))
            continue

        if 'outputformat' in line.lower() and not found_output_format:
            _query.append(line.replace('\n', ' ').replace('\r', ''))
            found_output_format = True
            continue

    if not found_output_format:
        _query.append('OutputFormat: json')
        response.headers['Content-Type'] = 'application/json'
    else:
        response.headers['Content-Type'] = 'text/plain'

    _query.append('')
    _query.append('')

    query = "\n".join(_query)


    answer = get_data(query)

    return answer

sys.path = [os.path.dirname(__file__)] + sys.path

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

application = default_app()

