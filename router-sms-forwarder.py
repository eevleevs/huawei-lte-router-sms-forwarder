#! /usr/bin/env python3

from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
import time

ADMIN_PASSWORD = 'password'
FORWARD_TO = ['phone_number']

ROUTER_ADDRESS = '192.168.8.1'
ADMIN_USER = 'admin'
CHECK_INTERVAL = 60
DELETE_FORWARDED = True

client = Client(AuthorizedConnection(f'http://{ADMIN_USER}:{ADMIN_PASSWORD}@{ROUTER_ADDRESS}'))

while True:
    sms_list = client.sms.get_sms_list()['Messages']
    if sms_list:
        for message in sms_list['Message'][::-1]:
            if message['Smstat'] == '0':
                client.sms.send_sms(FORWARD_TO, f"[{message['Phone']}] {message['Content']}")
                if DELETE_FORWARDED:
                    client.sms.delete_sms(message['Index'])
    time.sleep(CHECK_INTERVAL)
