from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
import os
import os.path
from os import path
from pathlib import Path
import time
import logging
import config
import subprocess

TOKEN = config.TTOKEN

fpath = config.FPATH #Files directory
bpath = config.BPATH #directory path of the bot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="<Your welcome message.>")

# def error(update, context):
#     logger.warning('Update "%s" caused error "%s"', update, context.error)

def find(update, context):
    os.system ("tree " + fpath + " > " + bpath + "/tree.txt") #create txt file with tree structure
    doc = open(bpath + '/tree.txt', 'rb')
    chat_id = str(update.effective_chat.id)
    context.bot.send_document(chat_id, document=doc)

def doc(update, context):

    if not context.args:
        context.bot.send_message(chat_id=update.effective_chat.id, text="And the document?")

    else:
        c_message = str(context.args[0])
        print(c_message)

        f_path = subprocess.check_output("find " + fpath + " -type f -name '*" + c_message + "*'", shell=True).splitlines()
        print(f_path)
        p_list = f_path

        if len(p_list)==0: #if no path
            context.bot.send_message(chat_id=update.effective_chat.id, text="This document does not exist or its name contains invalid characters.")

        elif len(p_list)==1: #if one path
            f_path = f_path[0].decode('utf-8')
            my_file = Path(f_path)
            if my_file.is_file(): #if path exists
                doc = open(f_path, 'rb')
                chat_id = str(update.effective_chat.id)
                context.bot.send_document(chat_id, document=doc)

            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="This document does not exist or its name contains invalid characters.")

        else: #if more than one path
            keyboard=[]
            for i in p_list:
                ic = os.path.split(i)
                itembtn = KeyboardButton("/doc " + ic[1].decode('utf-8'))
                keyboard.append([itembtn])

            print(keyboard)

            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            update.message.reply_text("Choisissez votre document: ", reply_markup=reply_markup)

def main():
    updater = Updater(token=TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('find', find))
    updater.dispatcher.add_handler(CommandHandler('doc', doc, pass_args=True))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
