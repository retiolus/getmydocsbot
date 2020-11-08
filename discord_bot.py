import discord
import os
import os.path
from os import path
from pathlib import Path
import subprocess
import config

TOKEN = config.DTOKEN

p_path = config.FPATH #parent directory
b_path = config.BPATH #directory path of the bot

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
        # channel = client.get_channel(762760304186359892)
        await message.channel.send(file=discord.File(doc))

    if message.content.startswith('/doc'):
        c_message = message.content #clean message
        l_c_message = len(c_message) #lenght of c_message
        c_message = c_message[5:l_c_message] #delete "/doc" from c_message

        f_path = subprocess.check_output("find " + p_path + " -type f -name '*" + c_message + "*'", shell=True).splitlines()
        print(f_path)
        p_list = f_path

        if len(p_list)==0: #if no path
            await message.delete(delay=30)
            await message.channel.send("This document does not exist or its name contains invalid characters.", delete_after=30)

        elif len(p_list)==1: #if one path
            f_path = f_path[0].decode('utf-8')
            my_file = Path(f_path)
            print(my_file)
            if my_file.is_file(): #if file exists
                doc = open(f_path, 'rb')
                file_name = os.path.split(f_path)
                await message.channel.send(file=discord.File(doc, filename=str(file_name[1])))

            else:
                await message.delete(delay=30)
                await message.channel.send("This document does not exist, its name contains invalid characters or two documents have the same name.", delete_after=30)

        else: #if more than one file
            await message.delete(delay=60)
            await message.channel.send("Choose one of these documents. :arrow_heading_down:", delete_after=60)
            for i in p_list:
                ic = os.path.split(i)
                await message.channel.send(ic[1].decode('utf-8'), delete_after=60)
            await message.channel.send("Choose one of these documents. :arrow_heading_up:", delete_after=60)

client.run(TOKEN)
