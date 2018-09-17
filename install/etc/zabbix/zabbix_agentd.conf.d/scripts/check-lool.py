#!/usr/bin/python3

import requests
from websocket import create_connection,WebSocket
import ssl
import sys
import os

requests.packages.urllib3.disable_warnings()

def get_token_value(url,username,password):
	r = requests.get(url,auth=(username,password),verify=False)
	token_value = r.cookies['jwt']
	return token_value

def get_doc_info(socket_url,token_value):
	data = {}
	ws = create_connection(socket_url,sslopt={"cert_reqs": ssl.CERT_NONE})
	"""Authenticating with Server  """
	ws.send('auth '+'jwt='+token_value)
	"""Now fetching information """
	word = ['active_users_count', 'active_docs_count', 'mem_consumed', 'sent_bytes', 'recv_bytes']
	for i in word:
		ws.send(i)
		result = ws.recv()
		result = result.split()
		data[result[0]] = result[1]
	ws.close()
	return data

if __name__ == '__main__':
	url = "https://localhost:9980/loleaflet/dist/admin/admin.html"
	username = os.getenv('ADMIN_USER')
	password = os.getenv('ADMIN_PASS')
	token_value = get_token_value(url,username,password)
	socket_url = "wss://localhost:9980/lool/adminws"
	data = get_doc_info(socket_url,token_value)
	for key,value in data.items() :
                print("lool."+key , value)

