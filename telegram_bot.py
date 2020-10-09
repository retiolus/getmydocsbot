import telebot
from telebot import types
import os
import os.path
from os import path
from pathlib import Path

TOKEN = '<TOKEN>'

p_path = "</parent/path>" #parent directory
b_path = "</bot/path>" #directory path of the bot
gifs = "gifs/" #gifs directory path

tb = telebot.TeleBot(TOKEN)	#create a new Telegram Bot object

@tb.message_handler(commands=['start'])
def start(message):
    tb.reply_to(message, "<Your welcome message.>")

#send a tree structure of parent directory when user send /find
@tb.message_handler(commands=['find'])
def find(message):
   os.system ("tree " + p_path + " > " + b_path + "/tree.txt") #create txt file with tree structure
   doc = open(b_path + '/tree.txt')
   tb.send_document(message.chat.id, doc)

#send document
@tb.message_handler(commands=['doc'])
def doc(message):
    c_message = message.text #clean message
    l_c_message = len(c_message) #lenght of c_message
    c_message = c_message[5:l_c_message] #delete "/doc" from c_message

    f_path = os.popen("find " + p_path + " -type f -name '*" + c_message + "*'").read() #full path
    l_f_path = len(f_path) #lenght of full path
    f_path = f_path[0 : l_f_path-1]
    p_list = f_path.split("\n") #create a list of paths

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True) #create the image selection keyboard

    if len(p_list)==0: #if no path
#        gif_p = os.popen("find gifs/ -type f | shuf -n 1").read()
#        l_gif_p = len(gif_p)
#        gif_p = gif_p[0 : l_gif_p-1]
#        gif = open(gif_p, 'rb')
#        tb.send_document(message.chat.id, gif, timeout=1000)
        tb.reply_to(message, "This document does not exist or its name contains invalid characters.")

    elif len(p_list)==1: #if one path
        my_file = Path(f_path)
        if my_file.is_file(): #if path exists
            doc = open(f_path, 'rb')
            tb.send_document(message.chat.id, doc, timeout=1000)
#            tb.delete_message(message.chat.id, message.message_id,timeout=1000)
        else:
#            gif_p = os.popen("find gifs/ -type f | shuf -n 1").read()
#            l_gif_p = len(gif_p)
#            gif_p = gif_p[0 : l_gif_p-1]
#            gif = open(gif_p, 'rb')
#            tb.send_document(message.chat.id, gif, timeout=1000)
            tb.reply_to(message, "This document does not exist or its name contains invalid characters.")

    else: #if more than one path
#        tb.delete_message(message.chat.id, message.message_id,timeout=1000)
        for i in p_list: #create the image selection keyboard
            ic = os.path.split(i)
            itembtn = types.KeyboardButton("/doc " + ic[1])
            markup.row(itembtn)

        bot_msg = tb.send_message(message.chat.id, "Document to be sent :", reply_markup=markup)

tb.polling(none_stop=True)
