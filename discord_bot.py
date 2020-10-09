import discord
import os
import os.path
from os import path
from pathlib import Path

TOKEN = '<TOKEN>'

p_path = "</parent/path>" #parent directory
b_path = "</bot/path>" #directory path of the bot

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/find'):
        os.system ("tree " + p_path + " > " + b_path + "/tree.txt") #create txt file with tree structure
        doc = open(b_path + '/tree.txt')
        channel = client.get_channel(762760304186359892)
        await message.channel.send(file=discord.File(doc))

    if message.content.startswith('/doc'):
        c_message = message.content #clean message
        l_c_message = len(c_message) #lenght of c_message
        c_message = c_message[5:l_c_message] #delete "/doc" from c_message

        f_path = os.popen("find " + p_path + " -type f -name '*" + c_message + "*'").read() #full path
        l_f_path = len(f_path) #lenght of full path
        f_path = f_path[0 : l_f_path-1]
        p_list = f_path.split("\n") #create a list of paths

        if len(p_list)==0: #if no path
            await message.channel.send("This document does not exist or its name contains invalid characters.", delete_after=30)

        elif len(p_list)==1: #if one path
            my_file = Path(f_path)
            if my_file.is_file(): #if file exists
                doc = open(f_path, 'rb')
                await message.channel.send(file=discord.File(doc))

            else:
                await message.channel.send("This document does not exist or its name contains invalid characters.", delete_after=30)

        else: #if more than one file
            await message.channel.send("Choose one of these documents. :arrow_heading_down:", delete_after=30)
            for i in p_list:
                ic = os.path.split(i)
                await message.channel.send(ic[1], delete_after=30)
            await message.channel.send("Choose one of these documents. :arrow_heading_up:", delete_after=30)

client.run(TOKEN)
