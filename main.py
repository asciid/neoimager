#!/usr/bin/env python3
from pyrogram import Client, Filters
from selenium import webdriver
import os
import re

app = Client(
        session_name='neoimager',
        bot_token='',
        api_hash='',
        api_id=''
        )

@app.on_message(Filters.text)
def linkProcessing(client, message):
    global browser
    links = []
    file_name = 'screenshot.png'
    

    # Getting a link
    if message.entities:
        for entity in message.entities:
            links.append(message.text[entity.offset : entity.offset + entity.length])
            #break #Add later if needed
    
    for link in links:
        browser.get(link)

        with open(file_name, 'wb') as file:
            file.write(browser.get_screenshot_as_png())
        
        message.reply_photo(file_name, quote=True)
        os.remove(file_name)
    
browser = webdriver.Firefox(executable_path='./geckodriver')

app.run()
