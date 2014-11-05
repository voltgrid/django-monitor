#!/usr/bin/env python

import argparse
import requests
import json
import socket

from settings import *


def main(args):

    data = {
        'host': str(args.host),
        'event': str(args.event),
        'status': str(args.status),
        'description': str(args.description)
    }
    if args.debug:
        print(data)
    headers = {'Content-type': 'application/json'}
    try:
        r = requests.post('%s/monitor/v1/result/' % API_HOST, data=json.dumps(data), headers=headers, auth=(API_USER, API_PASS))
        if r.status_code != 201:
            raise requests.RequestException('Error: %s' % r.status_code)
    except requests.ConnectionError, e:
        print("Error: %s" % str(e))
        pass


if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(prog='send_result',
                                     description='Send event results to monitor')

    parser.set_defaults(func=main)
    parser.add_argument('--host', type=str, help='Hostname', default=socket.gethostname())
    parser.add_argument('--event', type=str, help='Event', required=True)
    parser.add_argument('--description', type=str, help='Description', required=True)
    parser.add_argument('--status', type=str, help='Status', choices=['O', 'W', 'C'], required=True)
    parser.add_argument('--debug', help='Debug', default=False, action='store_true')
    args = parser.parse_args()
    args.func(args)
