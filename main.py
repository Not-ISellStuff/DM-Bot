"""

This tool was made to send a message to every person in your friends list

You can use this for things like advertising

If you found this tool helpful consider leaving a star on this repo

btw if you didn't know this isn't a discord bot it's just a script to dm your friends list

"""

import os
import time
import requests
import json
import fade
from colorama import Fore

# ---------------------------------------- #

mag = Fore.MAGENTA
yellow = Fore.YELLOW
red = Fore.RED
green = Fore.GREEN

class Data:
    tosend = 0

data = Data()

class Bot:
    def __init__(self, token, message):
        self.token = token
        self.message = message
    
    def loadtk(self):
        with open('settings.json', 'r') as f:
            data = json.load(f)
        
        self.token = str(data['token'])

    def loadlst(self):
        r = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={'Authorization': self.token})
        if r.status_code == 401:
            print(red + "\n[!] Token Is Invalid")
            time.sleep(3)
            exit()
        elif r.status_code == 429:
            print(yellow + "\n[!] Failed To Get Friends List.")
            time.sleep(3)
            main()
        
        if "[]" in r.text:
            print(yellow + "\n[!] You Have 0 Friends Lol")
            time.sleep(3)
            main()
        else:
            return r.json()

    def loadchannels(self, friends):
        channels = []

        for i in friends:
            d = {
                'recipient_id': i
            }
            r = requests.post('https://discord.com/api/v10/users/@me/channels',headers={'Authorization': self.token},json=d)
            channel = r.json()['id']
            channels.append(channel)
        
        return channels

    def send(self, channel):
        api = f'https://discord.com/api/v9/channels/{channel}/messages'
        h = {'Authorization': self.token}
        j = {'content': self.message}

        r = requests.post(api, headers=h, json=j)
        if r.status_code == 401:
            print(red + "\n[!] Token Is Invalid")
            exit()
        elif r.status_code == 429:
            print(yellow + "[!] You are being ratelimited")
        elif r.status_code == 200:
            print(green + f"[+] Sent Message | Messages To Send --> {data.tosend}")
            data.tosend -= 1
        else:
            print(yellow + "[!] You are being ratelimited")

    # ------------------------------------ #

    def start(self):

        """

        So first the loadlst function gets your friend's user id and puts it in a list THEN with the loadchannels function it
        gets the channel id of the dm then with the send function it sends the actual message to your friend

        """

        friends = self.loadlst()
        print(green + "[+] Loaded Friends List")

        userzid = []

        for i in friends:
            uzerid = i['id']
            userzid.append(uzerid)
        print(green + "[+] Loaded User IDs")

        channels = self.loadchannels(userzid)
        data.tosend = len(channels)
        print(green + "[+] Loaded DM Channel IDs")
        r = input(red + f"NOTE: This will take {len(channels) * 2.5} seconds due to discord ratelimits and being limited. Are you sure you want to continue? y/n > ")
        if r == 'n':
            print(yellow + "\n[*] Closing..")
            time.sleep(1.5)
            exit()

        print(green + "[+] Starting...\n")

        for c in channels:
            self.send(c)
            time.sleep(2.5)
    
# ---------------------------------------- #

def main():
    os.system("cls")
    print(fade.purplepink("""
  ___        ___      _   
 |   \ _ __ | _ ) ___| |_  [Version 1.0]
 | |) | '  \| _ \/ _ \  _| Dev --> [ISellStuff]
 |___/|_|_|_|___/\___/\__| Exit --> [x]
                        
    [1] Start
    """))

    options = ['x', '1']
    op = input(mag + "> ")

    if op in options:
        if op == 'x':
            print(yellow + "\n[*] Closing..")
            time.sleep(1.5)
            exit()
    else:
        print(red + "\n[!] Invalid Option")
        time.sleep(1.5)
        main()
    os.system("cls")

    bot = Bot("", "")
    bot.loadtk()

    message = input("Message: ")
    os.system("cls")
    print(green + "[+] Loaded Token")
    print(green + f"[+] Set Message To --> {message}")

    bot.message = message
    bot.start()

    r = input(mag + "\nDo You Want To Go Back To The Menu? y/n > ")
    if r == 'y':
        main()
    
    print(yellow + "[*] Closing..")
    time.sleep(1.5)
    exit()

if __name__ == "__main__":
    main()
