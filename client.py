#! /usr/bin/env python

# ******************************************************************************
# Copyright (c) 2016 General Electric Company operating through GE Digital LLC
#
# Refer to LICENSE.txt for the terms and conditions of the license
# governing this copyrighted work.  Those terms and conditions are incorporated
# in their entirety herein.
# ******************************************************************************

import os
import json
from websocket import create_connection
import requests
import base64


def get_client_token(uaa, client, secret):
    """
    Given a UAA URL and the client id and secret will
    return the client credentials access token.
    """
    credentials = base64.b64encode(client + ':' + secret)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Authorization': 'Basic ' + credentials
        }
    params = {
        'client_id': client,
        'grant_type': 'client_credentials'
    }
    response = requests.post(uaa, headers=headers, params=params)
    return json.loads(response.text)['access_token']

def get_assets(traffic, headers, bbox, device_type):
    """
    Returns a list of assets given the bounding-box and
    device type parameters.

    Requires the Traffic Planning Endpoint and UAA token
    with zone id for the service.
    """
    url = traffic + '/v1/assets/search'
    params = {
        'q': 'device-type:' + device_type,
        'bbox': bbox,
        }
    response = requests.get(url, headers=headers, params=params)
    return json.loads(response.text)['_embedded']['assets']

def get_asset_live_stream(asset, headers):
    """
    This follows the asset to identify the live stream url that we
    can make a websocket connection and listen for events.
    """
    url = asset['_links']['live-events']['href']
    url = url.replace('http://', 'https://') # SSL
    url = url.replace('{?event-types}', '?event-types=TFEVT') # HATEOAS
    res = requests.get(url, headers=headers)
    return json.loads(res.text)['url']


# Get UAA configuration from environment variables
uaa_url = os.environ.get('UAA_URI', 'https://my-uaa-guid.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token')
uaa_client = os.environ.get('UAA_CLIENT', 'my-client')
uaa_secret = os.environ.get('UAA_CLIENT_SECRET', 'my-secret')

# Get Traffic configuration from environment variables
traffic_url = os.environ.get('TRAFFIC_URI', 'https://ie-traffic.run.aws-usw02-pr.ice.predix.io')
traffic_zone = os.environ.get('TRAFFIC_ZONE', 'abc-123')

# Get access token and headers we'll use from now on
token = get_client_token(uaa_url, uaa_client, uaa_secret)
headers = {
    'Authorization': 'Bearer ' + token,
    'Predix-Zone-Id': traffic_zone
    }

# Get Traffic Asset and Traffic Stream
bbox = '32.715675:-117.161230,32.708498:-117.151681'
assets = get_assets(traffic_url, headers, bbox, 'DATASIM')
wss = get_asset_live_stream(assets[0], headers)

# Listen for the next Event
ws = create_connection(wss, header=headers)
event = ws.recv()
print event
ws.close()

"""
Out[24]:
'{"event-uid":"60527273-bce3-4d38-89ee-88ca7fe7485f","timestamp":1468480686466,"event-type":"TFEVT","device-uid":"HYP1040-75","location-uid":"HYP1040-75-Lane2","properties":{"vehicle-type":"car"},"measures":[{"tag":"vehicleCount","value":4},{"tag":"speed","value":22,"unit":"MPS"},{"tag":"direction","value":263,"unit":"DEGREE"}]}'
"""

