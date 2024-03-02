# Import Telegram bot library - this lets us build a bot 
import telebot
from cludflare_configuration import create_cname
# Import Google Sheets library - this lets us edit spreadsheets
import gspread
from googleapiclient.errors import HttpError
from googleapiclient.errors import HttpError   
# Import ReplyKeyboardMarkup from Telebot - this lets us make message buttons
from telebot import types
from excel_integration import *
import requests
import json
from datetime import timedelta,datetime
import requests # We need the requests module to make API calls
import time # We need time to generate timestamps for hostnames
from butts import *
import schedule
import time
api_key = 'ir7aS9vMheiAFK9aK2flJTJzQHezYd8dXpc2Bcg8'
configs = {}
authenticated_users = {}
# API endpoint for Cloudflare 
CF_API_URL = 'https://api.cloudflare.com/client/v4/zones/'  
command_options = ["Create Config","remaining Tokens","get expired","sirejeffishere"]

# A dictionary that maps domain names to their API keys
# This allows looking up the right key for each domain

# Create an instance of the Telegram bot with our access token
# testcenter api
bot = telebot.TeleBot('7055187634:AAHPc4WbxQF0epQ6gIndWd3DPZC1qomLDo0')



# Your existing code for bot setup and other functions...

@bot.message_handler(commands=['start'], func=lambda message: message.text)
def handle_start_primary(message):
    bot.send_message(message.chat.id, "Please enter your username.")
    bot.register_next_step_handler(message, handle_username_input)

def handle_username_input(message):
    # Save the username
    username = message.text
    
    bot.send_message(message.chat.id, "Please enter your password.")
    bot.register_next_step_handler(message, lambda m: handle_password_input(m, username))

def handle_password_input(message, username):
    # Save the password
    password = message.text
    
    # Authenticate user
    user_data = authenticate_user(username, password,message.chat.id)
    
    if user_data:
        # Authentication successful, you can use the user_data dictionary
        authenticated_users[user_data['username']] = user_data['chatid']
        bot.send_message(message.chat.id, "Authentication successful!")
        configs[message.chat.id]={}
        handle_start(message)
    else:
        bot.send_message(message.chat.id, "Authentication failed. Try again.")
        handle_start_primary(message)


def handle_start(message):
    flag=False
    print(authenticated_users.keys())
    print(authenticated_users)
    for i in authenticated_users.keys():
        if str(authenticated_users[i])==str(message.chat.id):
            configs[authenticated_users[i]]={}
            flag=True
    if  flag==False:
        return handle_start_primary(message)
        
    bot.clear_step_handler(message)
    configs[message.chat.id].clear()
    bot.send_message(message.chat.id, f"select an option.", reply_markup=command_kb)
    bot.register_next_step_handler(message,handle_message)

@bot.message_handler(func=lambda message: message.text)
def handle_message(message):
    user_id = message.chat.id
    text = message.text

    if text in command_options:
        # Handle the selected command
        bot.send_message(message.chat.id, f"You selected {text}.")
        if text == "Create Config":
            try:
                bot.send_message(message.chat.id, 'Enter the user\'s first and last name:', reply_markup=back_kb)
                bot.register_next_step_handler(message, handle_name)
            except Exception as e:
                bot.send_message(message.chat.id, f"fatal error occured:{e} \n at {text}")
                handle_start(message)
        elif text == "remaining Tokens":
            try:
                remainingtokens(message)
            except Exception as e:
                bot.send_message(message.chat.id, f"fatal error occured:{e} \n at {text}")
                handle_start(message)
        elif text == "get expired":
            try:
                get_and_send_expired_users(message)
            except Exception as e:
                bot.send_message(message.chat.id, f"fatal error occured:{e} \n at {text}")
                handle_start(message)
        elif text == "sirejeffishere":
            try:
                delete_expired_users(message)
            except Exception as e:
                bot.send_message(message.chat.id, f"fatal error occured:{e} \n at {text}")
                handle_start(message)
        
    else:
        bot.send_message(message.chat.id,"invalid choice , going back to the main menu")
        handle_start(message)


# Handle incoming message
@bot.message_handler(func=lambda message: message.text)
def handle_name(message):
  if message.text =="Menu":
    handle_start(message)