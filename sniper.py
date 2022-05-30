from pystyle import Colorate as Fade
from pystyle import Colors
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from colorama import Fore
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import os
from time import sleep
import threading
import requests
import random
import string

import datetime
now = datetime.datetime.now()
try:
    open('stuff/Hits.txt','w')
except:
    pass

class main():
    def __init__(self):
        self.Tries = 0
        self.sniped = 0
        config = json.load(open('config.json'))
        self.letters = config['letters_to_snipe']

    def Banner(self):
        config = json.load(open('config.json'))
        os.system('cls')
        input(Fade.Vertical(Colors.cyan_to_blue,f'''
            ╔═╗┬┌┬┐┬ ┬┬ ┬┌┐   ╔═╗┌┐┌┬┌─┐┌─┐┬─┐
            ║ ╦│ │ ├─┤│ │├┴┐  ╚═╗││││├─┘├┤ ├┬┘
            ╚═╝┴ ┴ ┴ ┴└─┘└─┘  ╚═╝┘└┘┴┴  └─┘┴└─
         ══╦═════════════════════════════════╦══
 ╔═════════╩═════════════════════════════════╩═════════╗
 ║              Running for {self.letters} letter names             ║
 ╚═════════════════════════════════════════════════════╝

Press Enter to start
-->
'''))


    def genUsername(self, length):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def snipe(self):
        os.system(f'title Github username sniper ^| tries: {self.Tries} ^| sniped: {self.sniped} 🎉 ^| running for: {self.letters}letter names')
        already_used = []
        with open('stuff/registered.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                already_used.append(line.replace('\n', ''))

        while True:
            username_to_try = self.genUsername(length={self.letters})
            if username_to_try in already_used:
                pass
            else:
                break

        r = requests.get(f'https://github.com/{username_to_try}')
        self.Tries += 1
        if r.status_code == 200:
            print(f'{Fore.RESET}[{Fore.LIGHTRED_EX}-{Fore.RESET}] {Fore.LIGHTRED_EX}Checked: {username_to_try}')
            with open(f'stuff/registered.txt','a+') as file:
                file.write(f'{username_to_try}\n')

        if r.status_code == 400:
            config = json.load(open('config.json'))

            print(f'{Fore.RESET}[{Fore.LIGHTGREEN_EX}+{Fore.RESET}]{Fore.LIGHTGREEN_EX}🎉 Got a Hit: {username_to_try} 🎉')

            notify = config['notify']
            if notify != 'true':
                pass
            else:
                pygame.mixer.init()
                pygame.mixer.music.load('sounds/Hit.mp3')
                pygame.mixer.music.play()

            webhook = DiscordWebhook(url=f'{config["webhook"]}')
            embed = DiscordEmbed(title=':dollar: Sniped :dollar:',description=f'\n:satellite_orbital: ',color='03b2f8')
            embed.set_author(name='github.com Sniper',url='https://media.giphy.com/media/KBxyo8FDKE33qnj3KB/giphy.gif',icon_url='https://cdn.discordapp.com/emojis/667742302755749908.webp?size=48&quality=lossless')
            # embed.set_image(url='https://ibb.co/1MypvKy')
            embed.set_thumbnail(url='https://media.giphy.com/media/Dndpiai0soTUk/giphy.gif')
            embed.set_footer(text='github.com Sniper',icon_url='https://cdn.discordapp.com/emojis/667742302755749908.webp?size=48&quality=lossless')
            embed.set_timestamp()
            webhook.add_embed(embed)
            response = webhook.execute()

            with open(f'stuff/registered.txt','a+') as file:
                file.write(f'{username_to_try}\n')


            with open('stuff/Hits.txt','a+') as file:
                file.write(f'{username_to_try}\n')

        if r.status_code == 429:
            print(f'{Fore.RESET}[{Fore.LIGHTYELLOW_EX}~{Fore.RESET}] {Fore.LIGHTYELLOW_EX}Got ratelimited sleeping for 5 seconds...')
            sleep(5)

        self.snipe()

main = main()
main.Banner()
for i in range(5):
    t = threading.Thread(target=main.snipe).start()


