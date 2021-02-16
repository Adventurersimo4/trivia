#import requests
#from bs4 import BeautifulSoup
import discord
from discord.utils import get 
import random
import json
from io import BytesIO
from PIL import Image, ImageFilter
from datetime import date
import time
import asyncio
from discord_handler.helper import yes_no


TOKEN = "TOKEN"

client = discord.Client()

points_dict = {'0️⃣':0,'1️⃣':1,'2️⃣':2,'3️⃣':3}

@client.event
async def on_message(message):

    if not message.author.bot:

        if message.content.startswith("!att"):
            print(str(message.attachments[0]).split(" ")[3][5:-2])

        if not message.guild:
            with open("travail_info/channels.json") as f:
                data = json.load(f)
                running = data["running"]
                if time.time()-10 <= data["last_q_time"]:
                    if running == "gtp":
                        if message.author.mention not in data["answered"]:
                            checking = data["checking"]
                            checking = client.get_channel(int(checking[2:-1]))
                            question = data[running][str(data["current_question"][running])][0]
                            check_msg = await checking.send("User "+message.author.mention+" has answered ```"+message.content+"```\nTo the question about player ```"+question+"```\nHow many points do you want to give him ?")
                            await check_msg.add_reaction('0️⃣')
                            await check_msg.add_reaction('1️⃣')
                            await check_msg.add_reaction('2️⃣')
                            await check_msg.add_reaction('3️⃣')
                            def check(reaction, user):
                                return user == message.author and str(reaction.emoji) in ['0️⃣','1️⃣','2️⃣','3️⃣']
                            try:
                                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                                try:
                                    data["points"][message.author.mention] += points_dict[reaction.emoji]
                                except KeyError:
                                    data["points"][message.author.mention] = points_dict[reaction.emoji]
                                await checking.send("`"+str(points_dict[reaction.emoji])+"` point(s) have been awarded to user "+message.author.mention)
                            except asyncio.TimeoutError:
                                await message.channel.send('You timed out. If you want to compensate the user, run !addpoints @mention <points>.')
                            
                            data["answered"].append(message.author.mention)
                            with open("travail_info/channels.json","w") as f:
                                json.dump(data, f, indent=6)
                        else:
                            await message.channel.send("You already answered.")
                    elif running == "general":
                        if message.author.mention not in data["answered"]:
                            checking = data["checking"]
                            checking = client.get_channel(int(checking[2:-1]))
                            question = data[running][str(data["current_question"][running])][0]
                            check_msg = await checking.send("User "+message.author.mention+" has answered ```"+message.content+"```\nTo the question ```"+question+"```\nHow many points do you want to give him ?")
                            await check_msg.add_reaction('0️⃣')
                            await check_msg.add_reaction('1️⃣')
                            await check_msg.add_reaction('2️⃣')
                            await check_msg.add_reaction('3️⃣')
                            def check(reaction, user):
                                return user == message.author and str(reaction.emoji) in ['0️⃣','1️⃣','2️⃣','3️⃣']
                            try:
                                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                                try:
                                    data["points"][message.author.mention] += points_dict[reaction.emoji]
                                except KeyError:
                                    data["points"][message.author.mention] = points_dict[reaction.emoji]
                                await checking.send("`"+str(points_dict[reaction.emoji])+"` point(s) have been awarded to user "+message.author.mention)
                            except asyncio.TimeoutError:
                                await message.channel.send('You timed out. If you want to compensate the user, run !addpoints @mention <points>.')
                            
                            data["answered"].append(message.author.mention)
                            with open("travail_info/channels.json","w") as f:
                                json.dump(data, f, indent=6)
                        else:
                            await message.channel.send("You already answered.")
                    elif running == "blurred":
                        if message.author.mention not in data["answered"]:
                            checking = data["checking"]
                            checking = client.get_channel(int(checking[2:-1]))
                            check_msg = await checking.send("User "+message.author.mention+" has answered ```"+message.content+"```\nTo the currently exposed blurred badge in "+data["departure"]+"\nHow many points do you want to give him ?")
                            await check_msg.add_reaction('0️⃣')
                            await check_msg.add_reaction('1️⃣')
                            await check_msg.add_reaction('2️⃣')
                            await check_msg.add_reaction('3️⃣')
                            def check(reaction, user):
                                return user == message.author and str(reaction.emoji) in ['0️⃣','1️⃣','2️⃣','3️⃣']
                            try:
                                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                                try:
                                    data["points"][message.author.mention] += points_dict[reaction.emoji]
                                except KeyError:
                                    data["points"][message.author.mention] = points_dict[reaction.emoji]
                                await checking.send("`"+str(points_dict[reaction.emoji])+"` point(s) have been awarded to user "+message.author.mention)
                            except asyncio.TimeoutError:
                                await message.channel.send('You timed out. If you want to compensate the user, run !addpoints @mention <points>.')
                            
                            data["answered"].append(message.author.mention)
                            with open("travail_info/channels.json","w") as f:
                                json.dump(data, f, indent=6)
                        else:
                            await message.channel.send("You already answered.")

        if message.content.startswith("!definechannel"):
            if message.content.split(" ")[1] == "arrival":
                channel_name = message.content.split(" ")[2]
                with open("travail_info/channels.json") as f:
                    data = json.load(f)
                    data["arrival"] = channel_name
                with open("travail_info/channels.json","w") as f:
                    json.dump(data,f, indent=6)
                await message.channel.send("The arrival channel has been successfully set.")
            elif message.content.split(" ")[1] == "departure":
                channel_name = message.content.split(" ")[2]
                with open("travail_info/channels.json") as f:
                    data = json.load(f)
                    data["departure"] = channel_name
                with open("travail_info/channels.json","w") as f:
                    json.dump(data,f, indent=6)
                    await message.channel.send("The departure channel has been successfully set.")
            elif message.content.split(" ")[1] == "checking":
                channel_name = message.content.split(" ")[2]
                with open("travail_info/channels.json") as f:
                    data = json.load(f)
                    data["checking"] = channel_name
                with open("travail_info/channels.json","w") as f:
                    json.dump(data,f, indent=6)
                    await message.channel.send("The checking channel has been successfully set.")

        if message.content.startswith("!ask"):
            if message.content.split(" ")[1] == "blurred":
                with open("travail_info/channels.json") as f:
                    data = json.load(f)
                    if "<#"+str(message.channel.id)+">" == data["arrival"]:
                        reaction_m = await message.channel.send('React with ✅ to confirm your input.')
                        """await reaction_m.add_reaction("✅")
                        def check(reaction, user):
                            return user == message.author and str(reaction.emoji) == '✅'
                        try:
                            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                        except asyncio.TimeoutError:"""
                        if not yes_no(text=reaction_m, ctx=client.get_channel(int(data["arrival"][2:-1])), timeout=60):
                            await message.channel.send('Questions must be sent in less than 60 seconds, in the following format : !ask <questions> | answer ; answer ; answer.')
                        else:
                            with open("travail_info/channels.json") as f:
                                data = json.load(f)
                                next_nb = max([int(key) for key in data["blurred"].keys()])+1
                                im = Image.open(BytesIO(requests.get(str(message.attachments[0]).split(" ")[3][5:-2]).content))
                                blurred_img = im.filter(ImageFilter.BoxBlur(20))
                                blurred_img = blurred_img.convert("RGB")
                                blurred_img.save("travail_info/trivia/blurred/img"+str(next_nb)+".jpg")
                            with open("travail_info/channels.json",'w') as f:
                                json.dump(data, f, indent=6)
                            await message.channel.send('Question has been registered.')
                    else:
                        await message.channel.send("Hmm, you can't use that here.")

            elif message.content.split(" ")[1] == "general":
                with open("travail_info/channels.json") as f:
                    data = json.load(f)
                    if "<#"+str(message.channel.id)+">" == data["arrival"]:
                        question = " ".join(message.content.split(" ")[2:]).split("|")[0].strip()
                        reaction_m = await message.channel.send('React with ✅ to confirm your input.')
                        await reaction_m.add_reaction("✅")
                        def check(reaction, user):
                            return user == message.author and str(reaction.emoji) == '✅'
                        try:
                            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                        except asyncio.TimeoutError:
                            await message.channel.send('You timed out. Questions must be sent in less than 60 seconds, in the following format : !ask <questions> | answer ; answer ; answer.')
                        else:
                            with open("travail_info/channels.json") as f:
                                data = json.load(f)
                                next_nb = max([int(key) for key in data["general"].keys()])+1
                                data["general"][str(next_nb)] = question
                            with open("travail_info/channels.json",'w') as f:
                                json.dump(data, f, indent=6)
                            await message.channel.send('Question has been registered.')
                    else:
                        await message.channel.send("Hmm, you can't use that here.")

            elif message.content.split(" ")[1] == "gtp":
                with open("travail_info/channels.json") as f:
                    data = json.load(f)
                    if "<#"+str(message.channel.id)+">" == data["arrival"]:
                        question = " ".join(message.content.split(" ")[2:]).split("|")[0].strip()
                        hints = [answer.strip().lower() for answer in " ".join(message.content.split(" ")[2:]).split("|")[1].split(";")]
                        if len(hints) == 3:
                            reaction_m = await message.channel.send('React with ✅ to confirm your input.')
                            await reaction_m.add_reaction("✅")
                            def check(reaction, user):
                                return user == message.author and str(reaction.emoji) == '✅'
                            try:
                                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                            except asyncio.TimeoutError:
                                await message.channel.send('You timed out. Questions must be sent in less than 60 seconds, in the following format : !ask <question> |hint ; hint ; hint')
                            else:
                                with open("travail_info/channels.json") as f:
                                    data = json.load(f)
                                    next_nb = max([int(key) for key in data["gtp"].keys()])+1
                                    data["gtp"][str(next_nb)] = [question, hints]
                                with open("travail_info/channels.json",'w') as f:
                                    json.dump(data, f, indent=6)
                                await message.channel.send('Question has been registered.')
                        else:
                            await message.channel.send("You have to provide exactly 3 hints !")
                    else:
                        await message.channel.send("Hmm, you can't use that here.")
        
        if message.content.startswith("!showquestions"):
            low, high = int(message.content.split(" ")[1]), int(message.content.split(" ")[2])
            embed = discord.Embed(title="Questions from "+str(low)+" to "+str(high))
            with open("travail_info/channels.json") as f:
                data = json.load(f)
                for nb in data["general"].keys():
                    embed.add_field(name=str(nb)+" : "+data["general"][nb][0], value=data["general"][nb][1], inline=False)
            await message.channel.send(embed=embed)

        if message.content.startswith("!editquestion"):
            nb = message.content.split(" ")[1]
            with open("travail_info/channels.json") as f:
                data = json.load(f)
                if "<#"+str(message.channel.id)+">" == data["arrival"]:
                    question = " ".join(message.content.split(" ")[2:]).split("|")[0].strip()
                    answers = [answer.strip().lower() for answer in " ".join(message.content.split(" ")[2:]).split("|")[1].split(";")]
                    reaction_m = await message.channel.send('React with ✅ to confirm your input.')
                    await reaction_m.add_reaction("✅")
                    def check(reaction, user):
                        return user == message.author and str(reaction.emoji) == '✅'
                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        await message.channel.send('You timed out. Questions must be sent in less than 60 seconds, in the following format : !ask <questions> | answer ; answer ; answer.')
                    else:
                        with open("travail_info/channels.json") as f:
                            data = json.load(f)
                            data["general"][str(nb)] = [question, answers]
                        with open("travail_info/channels.json",'w') as f:
                            json.dump(data, f, indent=6)
                        await message.channel.send('Question has been registered.')
                else:
                    await message.channel.send("Hmm, you can't use that here.")

        if message.content.startswith("!sendnext"):
            with open("travail_info/channels.json") as f:
                data = json.load(f)
            if int(data["arrival"][2:-1]) == message.channel.id:
                if message.content.split(" ")[1] == "blurred":
                    with open("travail_info/channels.json") as f:
                        data = json.load(f)
                        data["current_question"]["blurred"] += 1
                        file = discord.File("travail_info/trivia/blurred/img"+str(data["current_question"]["blurred"])+".jpg")
                        departure = data["departure"]
                        departure = client.get_channel(int(departure[2:-1]))
                        await departure.send(file=file)
                        await departure.send("You have 10 seconds to answer.")
                        data["running"] = "blurred"
                        data["last_q_time"] = time.time()
                        with open("travail_info/channels.json","w") as f:
                            json.dump(data, f, indent=6)
                        def check(reaction, user):
                            return False
                        try:
                            reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
                        except asyncio.TimeoutError:
                            await departure.send('**STOP**')
                            data["answered"] = []
                    with open("travail_info/channels.json","w") as f:
                        json.dump(data, f, indent=6)
                
                elif message.content.split(" ")[1] == "general":
                    with open("travail_info/channels.json") as f:
                        data = json.load(f)
                        data["current_question"]["general"] += 1
                        question = data["general"][str(data["current_question"]["general"])][0]
                        departure = data["departure"]
                        departure = client.get_channel(int(departure[2:-1]))
                        await departure.send(question)
                        await departure.send("You have 10 seconds to answer.")
                        data["running"] = "general"
                        data["last_q_time"] = time.time()
                        with open("travail_info/channels.json","w") as f:
                            json.dump(data, f, indent=6)
                        def check(reaction, user):
                            return False
                        try:
                            reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
                        except asyncio.TimeoutError:
                            await departure.send('**STOP**')
                            #await departure.send("The possible answers were : "+", ".join(data["general"][str(data["current_question"]["general"])]))
                            data["answered"] = []
                    with open("travail_info/channels.json","w") as f:
                        json.dump(data, f, indent=6)

                elif message.content.split(" ")[1] == "gtp":
                    with open("travail_info/channels.json") as f:
                        data = json.load(f)
                        data["current_question"]["gtp"] += 1
                        question = data["gtp"][str(data["current_question"]["gtp"])][0]
                        hints = data["gtp"][str(data["current_question"]["gtp"])][1]
                        departure = data["departure"]
                        departure = client.get_channel(int(departure[2:-1]))
                        await departure.send("**HINT 1**")
                        await departure.send(hints[0])
                        #await departure.send("You have 10 seconds to answer.")
                        data["running"] = "gtp"
                        data["last_q_time"] = time.time()
                        with open("travail_info/channels.json","w") as f:
                            json.dump(data, f, indent=6)
                        def check(reaction, user):
                            return False
                        try:
                            reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
                        except asyncio.TimeoutError:
                            await departure.send('**HINT 2**')
                            await departure.send(hints[1])
                            try:
                                reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
                            except asyncio.TimeoutError:
                                await departure.send('**HINT 3**')
                                await departure.send(hints[2])
                                try:
                                    reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
                                except asyncio.TimeoutError:
                                    await departure.send('**STOP**')
                                    await departure.send("The player was **"+question+"**")
                            #await departure.send("The possible answers were : "+", ".join(data["general"][str(data["current_question"]["general"])]))
                            data["answered"] = []
                    with open("travail_info/channels.json","w") as f:
                        json.dump(data, f, indent=6)


        if message.content.startswith("!help"):
            with open("travail_info/trivia/help.txt") as f:
                await message.channel.send(f.read())

        
                
                

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)