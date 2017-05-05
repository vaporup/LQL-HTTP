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

    output_format = 'json'

    _query = []

    for line in postdata:

        if 'outputformat' in line.lower() and 'csv' in line.lower():
            output_format = 'csv'
            continue
        if 'outputformat' in line.lower() and 'python' in line.lower():
            output_format = 'python'
            continue
        if 'outputformat' in line.lower() and 'json' in line.lower():
            continue
        if 'outputformat' in line.lower():
            continue

        _query.append(line.replace('\n', ' ').replace('\r', ''))

    _query.append('OutputFormat: ' + output_format)
    _query.append('')
    _query.append('')

    query = "\n".join(_query)

    response.headers['Content-Type'] = 'application/json'

    answer = get_data(query)

    return answer

sys.path = [os.path.dirname(__file__)] + sys.path

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

application = default_app()

