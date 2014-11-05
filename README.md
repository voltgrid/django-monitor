django-monitor
==============

Reusable Django app that provides event monitoring via HTTP REST API.

The basic premise is that events return the response to the app via a restful HTTP API call. The app then can use that
information as necessary.

## Status

This is a partially completed prototype / proof-of-concept.
 
## Example

To send a result to the app using the `requests` HTTP library:

    import socket
    import json

    def notify_monitor(status, description):
        data = {'host': socket.gethostname(), 'event': 'Example Event', 'status': str(status), 'description': str(description)}
        headers = {'Content-type': 'application/json'}
        try:
            r = requests.post('%s/monitor/v1/result/' % API_HOST, data=json.dumps(data), headers=headers, auth=(API_USER, API_PASS))
            assert r.status_code == 201
        except requests.ConnectionError, e:
            print("Error: %s" % str(e))