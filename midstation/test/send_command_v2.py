#!/usr/bin/env python

"""
This command will send a command message to the backend, which can be polled by
gateways
"""

import argparse
import requests
import json

def send_command(username, password, target_gateway_id, target_node_id, payload_hex, needs_ack=False):
    """
    Sends a message to a node through a specified gateway
    The gateway and node ids must be strings
    Returns the command id, or None if the send was unsuccessful
    """
    command_url = 'https://ingest.link-labs.com/api/command/Gateway/' + target_gateway_id
    command_headers = {'content-type': 'application/json', 'Accept': 'application/json'}

    target_node_id_hex = '{0:x}'.format(target_node_id & int('1' * 36, 2))
    cmd_data = {'commandType': target_node_id_hex + ':' + ('Ack' if needs_ack else 'NoAck'),
                'payloadHex': payload_hex}
    auth = requests.auth.HTTPBasicAuth(username, password)
    response = requests.post(command_url, json.dumps(cmd_data), verify=False,
                             headers=command_headers, auth=auth)
    if response.status_code == requests.codes['created']:
        return json.loads(response.text)['commandId']
    else:
        raise RuntimeError(response.reason)


def validate_hex_payload(x):
    hex(int(x, 16))
    return x


def main():
    parser = argparse.ArgumentParser(description='Send a message to a specific node through\
                                     a specific gateway')
    parser.add_argument('gateway_id', help='the 5-part hex gateway id shown in the configuration page')
    parser.add_argument('node_id', help='The 36-bit node id, in hex form, or `broadcast` to send to\
                        all nodes with a gateway',
                        type=lambda x: int('1' * 36, 2) if x == 'broadcast' else int(x, 16))
    parser.add_argument('payload', help='the payload, in hex', type=validate_hex_payload)
    parser.add_argument('username', help='Your dataaccess username')
    parser.add_argument('password', help='Your dataaccess password')
    parser.add_argument('--ack', help='request an ACK from the node', action='store_true')
    args = parser.parse_args()

    command_id = send_command(args.username, args.password, args.gateway_id,
                              args.node_id, args.payload, args.ack)

    print (command_id)

if __name__ == '__main__':
    main()
