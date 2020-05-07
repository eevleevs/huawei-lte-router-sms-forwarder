#! /usr/bin/env python3

from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
import time


ADMIN_PASSWORD = 'password'
FORWARD_TO = ['phone_number']

ROUTER_ADDRESS = '192.168.8.1'
CHECK_INTERVAL = 60
DELETE_FORWARDED = True


client = Client(AuthorizedConnection(f'http://admin:{ADMIN_PASSWORD}@{ROUTER_ADDRESS}'))

while True:
    sms_list = client.sms.get_sms_list()['Messages']
    if sms_list:
        sms_list = sms_list['Message']
        if type(sms_list) != list:
            sms_list = [sms_list]
        else:
            sms_list = sms_list[::-1]
        for sms in sms_list:
            if sms['Smstat'] == '0':
                client.sms.send_sms(FORWARD_TO, f"[{sms['Phone']}] {sms['Content']}")
                if DELETE_FORWARDED:
                    client.sms.delete_sms(sms['Index'])
    time.sleep(CHECK_INTERVAL)

