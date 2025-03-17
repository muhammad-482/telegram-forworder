import streamlit as st
import pandas as pd

 


import time
import asyncio
from telethon.sync import TelegramClient
from telethon import errors
import json
import os
from handling_file import *

st.write("""
# My first app after add secr and code added
Hello *world!*
""")

api_id = st.secrets["api_id"]
api_hash = st.secrets["api_hash"]
phone_number = st.secrets["phone_number"]

class TelegramForwarder:
    def __init__(self, api_id=api_id, api_hash=api_hash, phone_number=phone_number):
        print(f"api_id: {api_id}, api_hash: {api_hash}, phone_number: {phone_number}")
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('session_' + phone_number, api_id, api_hash)

    async def list_chats(self):
        await self.client.start(phone=self.phone_number)
        # Get a list of all the dialogs (chats)
        # dialogs = await self.client.get_dialogs()
        dialogs = await self.client.get_dialogs(ignore_migrated=True, limit=None)
        
        # Print information about each chat
        for dialog in dialogs:
            print(f"Chat ID: {dialog.id}, Title: {dialog.title}")
            
        print("List of groups printed successfully!")
    
    async def forward_messages_to_channel(self,sources, destination_channel_id, keywords):
        
        await self.client.connect()

        chats = load_data()

        print("Checking for messages and forwarding them...")

        while True:

            for source in sources:

                # # Fetch channel details
                # entity = await self.client.get_entity(source)
                # channel_name = entity.title
                
                # # Fix: Get username safely
                # if hasattr(entity, 'username') and entity.username:
                #     channel_link = f"https://t.me/{entity.username}"
                # else:
                #     channel_link = f"https://t.me/c/{abs(entity.id)}" if hasattr(entity, 'id') else "Private Channel"

                # print(f"Fetching messages from: {channel_name} ({channel_link})")

                # get messages from source one
                # Try to get the last tracked message
                # last_message_id = get_last_message(source)

                # # If no last message is tracked, fetch the most recent one from Telegram
                # if not last_message_id:
                #     last_message = await self.client.get_messages(source, limit=1)
                #     last_message_id = last_message[0].id
                    
                
                if get_last_message(source):
                    last_message_id = get_last_message(source) 
                else:
                    message = (await self.client.get_messages(source,limit=1))[0]
                    add_or_update_chat(source,message.id - 2)
                    last_message_id  = get_last_message(source)
                
                print("0----------last_message_id:  ",last_message_id)
                messages = await self.client.get_messages(source, min_id=last_message_id , limit=None)
                print("1-------------messages: ",messages)

                
                for message in reversed(messages):
                    # Check if the message text includes any of the keywords
                    print("iaam here ")
                    print("iaam here 2--------------Message: ",message)
                    if keywords:
                        print("inside keywords")
                        if message.text and any(keyword in message.text.lower() for keyword in keywords):
                            print(f"Message contains a keyword: {message.text}")

                            # Forward the message to the destination channel
                            await self.client.forward_messages(destination_channel_id, message)

                            print("Message forwarded")
                    else:
                            # Forward the message to the destination channel
                            await self.client.forward_messages(destination_channel_id, message.text)
                            
                            print("Message forwarded")

                    add_or_update_chat(source,message.id)
                    last_message_id = get_last_message(source)
            
        
            print("Waiting for the next check...")
            await asyncio.sleep(5)

async def main():

    api_id = st.secrets["api_id"]
    api_hash = st.secrets["api_hash"]
    phone_number = st.secrets["phone_number"]

    forwarder = TelegramForwarder(api_id, api_hash, phone_number)
    await forwarder.client.start()
    
    print("Choose an option:")
    print("1. List Chats")
    print("2. Forward Messages")
    
    # choice = input("Enter your choice: ")
    
    # if choice == "1":
    #     await forwarder.list_chats()
    # elif choice == "2":

    sources = [int(-4762190522),int(-1001197273212),int(-4745617547)]
    # sources = [int(--1001197273212)]
    
    destination_channel_id = int(-4708671429)
    
    
    # print("Enter keywords if you want to forward messages with specific keywords, or leave blank to forward every message!")
    # keywords = input("Put keywords (comma separated if multiple, or leave blank): ").split(",")

    await forwarder.forward_messages_to_channel(sources,destination_channel_id, keywords=None)


# Start the event loop and run the main function
if __name__ == "__main__":
    asyncio.run(main())





