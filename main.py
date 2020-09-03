#!/usr/bin/env python3
from pyrogram import Client, Filters
from selenium import webdriver, common
from random import randint
from time import strftime, localtime
from sys import argv
import protocol
import os

# TODO:
# Better user interaction
# Parallel processing

# DONE:
# Tor support
# I2P support
# Built-in FTP checked out
# Base error handling
# Archiving

app = Client(
        session_name='neoimager',
        bot_token='',
        api_hash='',
        api_id=''
        )

@app.on_message(Filters.text)
def linkProcessing(client, message):

    def modulePick(link):
        domain = link.split('/')[2].split('.')[-1]

        if domain == 'onion':
            profile = protocol.tor()
        elif domain == 'i2p':
            profile = protocol.i2p()
        else:
            profile = None

        return profile

    def archive(data, unix_time):

        randomScreenShotName = lambda len: ''.join([chr(randint(65, 122)) for i in range(0, len)]) + '.png'
        fileName = randomScreenShotName(10)
        unix_time = localtime(unix_time)

        YEAR = strftime('%Y', unix_time)
        MONTH = strftime('%m', unix_time)
        DAY = strftime('%d', unix_time)

        for ent in ('archive', YEAR, MONTH, DAY): # Creating missing folders
            if not os.path.exists(ent): os.mkdir(ent)
            os.chdir(ent)

        with open(fileName, 'wb') as file:
            file.write(data)

        out = os.path.abspath(fileName)

        os.chdir('../../../../')

        return out

    links = []
    file_name = 'screenshot.png'

    if message.entities:
        for entity in message.entities:
            if entity.type == 'url':
                links.append(message.text[entity.offset : entity.offset + entity.length])
            elif entity.type == 'text_link':
                links.append(entity.url)
            #break #Add later if needed.
    
    for link in links:
        
        browser = webdriver.Firefox(firefox_profile=modulePick(link), executable_path='./geckodriver')
        err = ''

        try:
            browser.get(link)
        except common.exceptions.TimeoutException:
            err = '{}: Connection to the resource is timed out.\nTry again later.'.format(link)
        except common.exceptions.WebDriverException:
            err = '{}: Given resource does not exist.'.format(link)

        if err:
            message.reply(err, quote=True)
            browser.quit()
            continue

        screenshot = archive(browser.get_screenshot_as_png(), message.date)

        message.reply_photo(
            screenshot,
            caption="Here's the {}.".format(link),
            quote=True,
            )
        browser.quit()
    
app.run()
