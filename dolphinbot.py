#!/usr/bin/env python3
import discord, random, os, re, json
from os import path
from shutil import copyfile

client = discord.Client()

directory = os.path.dirname(os.path.realpath(__file__))

clockfile = directory + "/clocks.json"

if not path.isfile(clockfile):
    copyfile(directory+"/sample clocks.json",clockfile)



with open(directory + "/bot.key","r") as file:
    key = file.read()


rulings = ["Obi-wan importantly told Anakin he had the High Ground! In light of this, and the game state, clearly your opponent's position is correct",
           "You can re-roll all failed hit rolls for this unit if, before rolling the dice, you hold aloft a grail or goblet and shout 'For the Lady' in a heroic voice.",
           "You can re-roll any failed hit rolls when attacking with the Runefang so long as you have a bigger and more impressive moustache than your opponent.",
           "If you actually talk to your imaginary horse you can re-roll failed wound rolls as well.",
           "You can add 1 to these dice rolls if, between the time you declare the target of the attack and time you roll the dice, your opponent looks you directly in the eye.",
           "Active Player Chooses.",
           "Has anyone told you the story of Darth Plagueis the wise? It's not a story the Jedi would tell you. I too, cannot give you a ruling here. Please ask dyno to flip a coin.",
           "Inactive Player Chooses.",
           "Electro leap will not remove from play.",
           "You can not use opening the gate to bring a companion model in.",
           "After you determine if it was a successful slam, meaning the model ended its slam movement within its slam range (.5'' for most models), it then can cast telekinesis and slam from its new location. As stated assuming it still has the model being slammed in its slam range.",
           "Because it is intended that with blood bound that no souls or corpses are able to be gained. We will look further at the wording and see what can be done, but for now there is no need for further discussion."]

scenarios = ["King of the Hill","Bunkers","Spread the Net","Invasion","Anarchy","Recon II"]

help = """Currently the commands available are:
> !help: Displays this help message.
> !stream: Get the link the the Knight Twitch Stream.
> !judge: Ask for a (meme worthy) Judgement call from Dolphin.
> !timer: Set a countdown timer. Syntax `!timer {hh:mm} ({reason}). Use `!timer` for more details.
> !heret: Set a countdown timer that pings here on completion. Syntax `!heret {hh:mm} {reason}. Use `!timer` for more details.
> !chessclock: Creates a chess clock between 2 players. Use `!chessclock` and `!chessclock help` for more details.
> !scenario: Provides a random Stream Roller 2019 Scenario.
> !github: Provides a link to the bot's GitHub page for reporting issues.

`{}` denote parameters. Parameters wrapped in `()` are optional."""

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        game = discord.Game("Judge | !help")
        await client.change_presence(status=discord.Status.online, activity=game)

    async def on_message(self, message):
        #print('Message from {0.author}: {0.content}'.format(message))
        import time, uuid
        from datetime import datetime, timedelta

        if message.author == client.user:
            return

        if message.content.lower() == ("!help"):
            await message.channel.send(help)
            return

        if message.content.lower().startswith("hello"):
            image = directory + "/Images/hello.gif"
            print(image)
            await message.channel.send("Hello there!")
            await message.channel.send(file=discord.File(image))
            return

        if message.content.lower() == ("!judge"):
            if str(message.channel).startswith("vassal"):
                #response = "I haven't been trained to give Judge calls yet, sorry {0.author.mention}. :(".format(message)
                response = "Thanks for asking for a Judgement call {0.author.mention}.".format(message)
                await message.channel.send(response)
                r = len(rulings)
                i = random.randint(0,r)
                response = rulings[i].format(message)
                await message.channel.send(response)
                return
            else:
                response = "We're not in a game channel, {0.author.mention}. Please get my attention in the correct Vassal Game Channel. Thanks! :)".format(message)
                await message.channel.send(response)
                return

        if message.content.lower() == "!stream":
            await message.channel.send("You can watch the Knight's Stream here: https://www.twitch.tv/knightsmachine")
            return

        if message.content.lower() == "!scenario":
            s = len(scenarios)
            i = random.randint(0,s)
            response = scenarios[i].format(message)
            await message.channel.send(response)
            map = directory + "/Images/" + scenarios[i].replace(" ","") + "-2019.png"
            await message.channel.send(file=discord.File(map))
            return
        
        if message.content.lower() == "!timer":
            await message.channel.send("The !timer command must be followed by a time period, and optionally a reason. For example: `!timer 03:00` will set a timer for 3 hours. If you wish, you can include a reason afterwards. For example: `!timer 01:30 Ryan and Thom's game` will set a timer for 1 hour 30 minutes with the reason *\"Ryan and Thom's game\"*.")
            return

        if message.content.lower().startswith("!timer "):
            timer = message.content[7:12]
            hours = message.content[7:9]
            minutes = message.content[10:12]
            seconds = "00"
            reason = message.content[13:]
            if re.match("[0-9][0-9]:[0-5][0-9]",timer):
                response = "Setting timer for " + str(int(hours)) + " hour(s) and " + str(int(minutes)) + " minute(s). Let the count down begin!"
                await message.channel.send(response.format(message))
                
                duration = int(seconds) + (int(minutes) * 60) + (int(hours) * 60 *60)
                
                embed = discord.Embed(title="Timer", description=reason, color=0x4444dd)
                embed.add_field(name="Duration", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                embed.add_field(name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                timermsg = await message.channel.send(embed=embed)
                
                #Start counting down
                start = datetime.now()
                end = start + timedelta(seconds=duration)
                while datetime.now() < end:
                    time.sleep(0.5)
                    remaining = int((end - datetime.now()).total_seconds())
                    hours = str(int(remaining / 3600))
                    minutes = str(int((remaining % 3600)/60))
                    seconds = str(remaining % 60)
                    embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                    await timermsg.edit(embed=embed)
                
                #timer complete!
                embed.set_field_at(1,name="Remaining", value="`00:00:00` ", inline=True) 
                await timermsg.edit(embed=embed)
                response = "Your timer has finished {0.author.mention}!".format(message)
                await message.channel.send(response)
            else:
                await message.channel.send("That isn't a valid time!")
            return
        
        #I have been lazy with this name for now.
        if message.content.lower().startswith("!heret "):
            timer = message.content[7:12]
            hours = message.content[7:9]
            minutes = message.content[10:12]
            seconds = "00"
            reason = message.content[13:]
            if reason == "":
                await message.channel.send("Here timers must have a reason.")
                return
            roles =  message.author.roles
            isJudge = False
            for role in roles:
                if role.name == "Judge":
                    isJudge = True
            if isJudge == False:
                await message.channel.send("You must be a Judge to use Here Timers.")
            elif re.match("[0-9][0-9]:[0-5][0-9]",timer):
                response = "Setting timer for " + str(int(hours)) + " hour(s) and " + str(int(minutes)) + " minute(s). Let the count down begin!"
                await message.channel.send(response.format(message))
                
                duration = int(seconds) + (int(minutes) * 60) + (int(hours) * 60 *60)
                
                embed = discord.Embed(title="Here Timer", description=reason, color=0x4444dd)
                embed.add_field(name="Duration", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                embed.add_field(name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                timermsg = await message.channel.send(embed=embed)
                
                #Start counting down
                start = datetime.now()
                end = start + timedelta(seconds=duration)
                while datetime.now() < end:
                    time.sleep(0.5)
                    remaining = int((end - datetime.now()).total_seconds())
                    hours = str(int(remaining / 3600))
                    minutes = str(int((remaining % 3600)/60))
                    seconds = str(remaining % 60)
                    embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                    await timermsg.edit(embed=embed)
                
                #timer complete!
                embed.set_field_at(1,name="Remaining", value="`00:00:00` ", inline=True) 
                await timermsg.edit(embed=embed)
                response = "".join(["@here , the timer, ", reason, ", has finished!"]).format(message)
                await message.channel.send(response)
            else:
                await message.channel.send("That isn't a valid time!")
            return

        if message.content.lower() == "!github":
            await message.channel.send("Please report any issues with the bot on GitHub: <https://github.com/LarnuUK/dolphinbot>".format(message))
            return

        #######################################
        # Here start the Chess Clock Commands #
        #######################################

        if message.content.lower() == "!chessclock":
            await message.channel.send("The !chessclock command must be followed by a time period and a mentioned opponent. For example: `!chessclock 01:00 @Thom` will set a timer for 1 hour for each player. For a list of Chess Clock commands, use `!chessclock help`.")
            return            

        if message.content.lower() == "!chessclock help":
            response = """The chessclock commands are as follows:
> !start - Starts/unpauses the chessclock.
> !update - Provides an update with the current times on the Chessclock.
> !switch - Switches the active opponent.
> !pause - Pauses your chessclock
> !end - Ends your chessclock. The chessclock **cannot** be restarted once it has ended.

All commands can be optionally followed by an ID, which allows a Judge to interact with another player's clock."""

            await message.channel.send(response.format(message))
            return           

        if message.content.lower().startswith("!chessclock "):
            with open(clockfile,"r") as clocks_file:
                clocks = json.load(clocks_file)
                for (id,clock) in clocks.items():
                    player1 = clock["Player1"]
                    player2 = clock["Player2"]
                    if clock["Status"] != "Finished" and int(clock["Channel ID"]) == message.channel.id and (int(player1["ID"]) == message.author.id or int(player2["ID"]) == message.author.id):
                        await message.channel.send("You already have an active clock in this channel. Please !end your active clock before starting a new one.".format(message))
                        return                    
            clockid = uuid.uuid4()
            timer = message.content[12:17]
            if len(message.mentions) == 0:
                await message.channel.send("Chess clocks require an opponent!")
            elif re.match("[0-9][0-9]:[0-5][0-9]",timer):
                hours = message.content[12:14]
                minutes = message.content[15:17]
                seconds = "00"
                duration = int(seconds) + (int(minutes) * 60) + (int(hours) * 60 *60)
                description = "".join([message.author.name, " vs ", message.mentions[0].name])
                time = '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds)
                embed = discord.Embed(title="Chess Clock", description=description, color=0xdddddd)
                embed.add_field(name="ID", value=clockid, inline=False) 
                embed.add_field(name="__**" + message.author.name+ "**__", value="`" + time + "`", inline=True) 
                embed.add_field(name=message.mentions[0].name, value="`" + time + "` ", inline=True) 
                embed.add_field(name="Status", value="Not Started", inline=False)
                embed.add_field(name="Pauses", value="0(0)", inline=True)
                clockmsg = await message.channel.send(embed=embed)
                with open(clockfile,"w") as clocks_file:
                    newclock = {str(clockid): { "Status": "Not Started", "Status Time": str(datetime.now()), "Channel ID": message.channel.id, "Active Player": "1", "Message ID" : str(clockmsg.id), "Pauses": 0, "Judge Pauses": 0, "Player1": {"Name": message.author.name, "ID": message.author.id, "Remaining": duration},"Player2": {"Name": message.mentions[0].name, "ID": message.mentions[0].id, "Remaining": duration}}}
                    clocks.update(newclock)
                    #print(clocks)
                    json.dump(clocks, clocks_file, indent=4)
            else:
                await message.channel.send("That isn't a valid time!")
            return

        if message.content.lower().startswith("!start"):
            if message.content.lower() == "!start":
                clockfound = False
                with open(clockfile,"r") as clocks_file:
                    clocks = json.load(clocks_file)
                    for (id,clock) in clocks.items():
                        if clockfound == False:
                            player1 = clock["Player1"]
                            player2 = clock["Player2"]
                            if clock["Status"] != "Finished" and int(clock["Channel ID"]) == message.channel.id and (int(player1["ID"]) == message.author.id or int(player2["ID"]) == message.author.id):
                                clockfound = True
                                break
                if clockfound == False:
                    await message.channel.send("You do not currently have an active clock to end in this channel!".format(message))
                elif clock["Status"] == "Running":
                    await message.channel.send("Your clock is already running.".format(message))
                else:
                    if int(clock["Active Player"]) == 1:
                        colour = 0xaa3333
                        playerone = "__**" + player1["Name"] + "**__"
                        playertwo = player2["Name"]
                    else:
                        colour = 0x3333aa
                        playerone = player1["Name"]
                        playertwo = "__**" + player2["Name"] + "**__"                        
                    #await message.channel.delete(clockmsg)
                    #await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")

                    p1hours = str(int(player1["Remaining"] / 3600))
                    p1minutes = str(int((player1["Remaining"] % 3600)/60))
                    p1seconds = str(player1["Remaining"] % 60)
                    p2hours = str(int(player2["Remaining"] / 3600))
                    p2minutes = str(int((player2["Remaining"] % 3600)/60))
                    p2seconds = str(player2["Remaining"] % 60)
                    #embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                    p1remaining = '%02d' % int(p1hours) + ":" + '%02d' % int(p1minutes) + ":" + '%02d' % int(p1seconds)
                    p2remaining = '%02d' % int(p2hours) + ":" + '%02d' % int(p2minutes) + ":" + '%02d' % int(p2seconds)
                    description = "".join([player1["Name"], " vs ", player2["Name"]])
                    embed = discord.Embed(title="Chess Clock", description=description, color=colour)
                    embed.add_field(name="ID", value=id, inline=False)
                    embed.add_field(name=playerone, value="`" + p1remaining + "`", inline=True) 
                    embed.add_field(name=playertwo, value="`" + p2remaining + "` ", inline=True) 
                    embed.add_field(name="Status", value="Running", inline=False)
                    embed.add_field(name="Pauses", value="".join([str(clock["Pauses"]),"(",str(clock["Judge Pauses"]),")"]), inline=True)
                    clockmsg = await message.channel.send(embed=embed)
                    with open(clockfile,"w") as clocks_file:
                        clocks[id]["Status"] = "Running"
                        clocks[id]["Status Time"] = str(datetime.now())
                        clocks[id]["Message ID"] = clockmsg.id
                        json.dump(clocks, clocks_file, indent=4)

            else:
                roles = message.author.roles
                isJudge = False
                for role in roles:
                    if role.name == "Judge":
                        isJudge = True
                if isJudge == False:
                    await message.channel.send("You must be a Judge to effect Chess Clocks with an ID.")
                else:
                    id = message.content.lower()[7:]
                    with open(clockfile,"r") as clocks_file:
                        clocks = json.load(clocks_file)
                    try:
                        clock = clocks[id]
                    except:
                        await message.channel.send("That clock does not exist!".format(message))
                        return
                    player1 = clock["Player1"]
                    player2 = clock["Player2"]
                    if clock["Status"] == "Running":
                        await message.channel.send("That clock is already running!".format(message))
                    elif clock["Status"] == "Finished":
                        response = "That clock is already finished!"
                        await message.channel.send(response.format(message))      
                    else:
                        if int(clock["Active Player"]) == 1:
                            colour = 0xaa3333
                            playerone = "__**" + player1["Name"] + "**__"
                            playertwo = player2["Name"]
                        else:
                            colour = 0x3333aa
                            playerone = player1["Name"]
                            playertwo = "__**" + player2["Name"] + "**__"             
                        #await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                        p1hours = str(int(player1["Remaining"] / 3600))
                        p1minutes = str(int((player1["Remaining"] % 3600)/60))
                        p1seconds = str(player1["Remaining"] % 60)
                        p2hours = str(int(player2["Remaining"] / 3600))
                        p2minutes = str(int((player2["Remaining"] % 3600)/60))
                        p2seconds = str(player2["Remaining"] % 60)
                        #embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                        p1remaining = '%02d' % int(p1hours) + ":" + '%02d' % int(p1minutes) + ":" + '%02d' % int(p1seconds)
                        p2remaining = '%02d' % int(p2hours) + ":" + '%02d' % int(p2minutes) + ":" + '%02d' % int(p2seconds)
                        description = "".join([player1["Name"], " vs ", player2["Name"]])
                        embed = discord.Embed(title="Chess Clock", description=description, color=colour)
                        embed.add_field(name="ID", value=id, inline=False)
                        embed.add_field(name=playerone, value="`" + p1remaining + "`", inline=True) 
                        embed.add_field(name=playertwo, value="`" + p2remaining + "` ", inline=True) 
                        embed.add_field(name="Status", value="Running", inline=False)
                        embed.add_field(name="Pauses", value="".join([str(clock["Pauses"]),"(",str(clock["Judge Pauses"]),")"]), inline=True)
                        clockmsg = await message.channel.send(embed=embed)
                        with open(clockfile,"w") as clocks_file:
                            clocks[id]["Status"] = "Running"
                            clocks[id]["Status Time"] = str(datetime.now())
                            clocks[id]["Message ID"] = clockmsg.id
                            json.dump(clocks, clocks_file, indent=4)
                    
            return

        if message.content.lower().startswith("!update"):
            if message.content.lower() == "!update":
                clockfound = False
                with open(clockfile,"r") as clocks_file:
                    clocks = json.load(clocks_file)
                    for (id,clock) in clocks.items():
                        if clockfound == False:
                            player1 = clock["Player1"]
                            player2 = clock["Player2"]
                            if clock["Status"] != "Finished" and int(clock["Channel ID"]) == message.channel.id and (int(player1["ID"]) == message.author.id or int(player2["ID"]) == message.author.id):
                                clockfound = True
                                break
                if clockfound == False:
                    await message.channel.send("You do not currently have an active clock to update in this channel!".format(message))
                elif clock["Status"] == "Paused" or clock["Status"] == "Not Started":
                    await message.channel.send("Your clock is currently not running. You need to !start your clock.".format(message))
                else:
                    laststatus = datetime.strptime(clock["Status Time"],"%Y-%m-%d %H:%M:%S.%f")
                    if int(clock["Active Player"]) == 1:
                        remaining = player1["Remaining"]
                        activeplayer = player1["ID"]
                    else: 
                        remaining = player2["Remaining"]
                        activeplayer = player2["ID"]
                    timepassed = int((datetime.now() - laststatus).total_seconds())
                    newremaining = remaining - timepassed
                    if newremaining <= 0:
                        newremaining = 0
                    if int(clock["Active Player"]) == 1:
                        colour = 0xaa3333
                        playerone = "__**" + player1["Name"] + "**__"
                        playertwo = player2["Name"]
                        p1hours = str(int(newremaining / 3600))
                        p1minutes = str(int(newremaining / 60))
                        p1seconds = str(int(newremaining % 60))
                        p2hours = str(int(player2["Remaining"] / 3600))
                        p2minutes = str(int((player2["Remaining"] % 3600)/60))
                        p2seconds = str(player2["Remaining"] % 60)
                    else:
                        colour = 0x3333aa
                        playerone = player1["Name"]
                        playertwo = "__**" + player2["Name"] + "**__"
                        p1hours = str(int(player1["Remaining"] / 3600))
                        p1minutes = str(int((player1["Remaining"] % 3600)/60))
                        p1seconds = str(player1["Remaining"] % 60)           
                        p2hours = str(int(newremaining / 3600))
                        p2minutes = str(int(newremaining / 60))
                        p2seconds = str(int(newremaining % 60))       
                    if newremaining == 0:
                        colour = 0x000000                               
                    #await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                    #embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                    p1remaining = '%02d' % int(p1hours) + ":" + '%02d' % int(p1minutes) + ":" + '%02d' % int(p1seconds)
                    p2remaining = '%02d' % int(p2hours) + ":" + '%02d' % int(p2minutes) + ":" + '%02d' % int(p2seconds)
                    description = "".join([player1["Name"], " vs ", player2["Name"]])
                    embed = discord.Embed(title="Chess Clock", description=description, color=colour)
                    embed.add_field(name="ID", value=id, inline=False)
                    embed.add_field(name=playerone, value="`" + p1remaining + "`", inline=True) 
                    embed.add_field(name=playertwo, value="`" + p2remaining + "` ", inline=True) 
                    if newremaining > 0:
                        embed.add_field(name="Status", value="Running", inline=False)
                    else:
                        embed.add_field(name="Status", value="Finished", inline=False)
                        response = "".join(["Your clock has expired, <@", str(activeplayer), ">!"])
                        await message.channel.send(response.format(message))
                    embed.add_field(name="Pauses", value="".join([str(clock["Pauses"]),"(",str(clock["Judge Pauses"]),")"]), inline=True)
                    clockmsg = await message.channel.send(embed=embed)
                    with open(clockfile,"w") as clocks_file:
                        clocks[id]["Status Time"] = str(datetime.now())
                        clocks[id]["Message ID"] = clockmsg.id
                        if int(clock["Active Player"]) == 1:
                            clocks[id]["Player1"]["Remaining"] = newremaining
                        else:
                            clocks[id]["Player2"]["Remaining"] = newremaining
                        if newremaining == 0:
                            clocks[id]["Status"] = "Finished"
                        json.dump(clocks, clocks_file, indent=4)
            else:
                roles = message.author.roles
                isJudge = False
                for role in roles:
                    if role.name == "Judge":
                        isJudge = True
                if isJudge == False:
                    await message.channel.send("You must be a Judge to effect Chess Clocks with an ID.")
                elif message.content.lower() == "!update all":
                    await message.channel.send("I haven't written the `!update all` command yet. Give me a break. Please? @Judge !".format(message))
                else:
                    id = message.content.lower()[8:]
                    with open(clockfile,"r") as clocks_file:
                        clocks = json.load(clocks_file)
                        try:
                            clock = clocks[id]
                        except:
                            response = "That clock doesn't exist!"
                            await message.channel.send(response.format(message))             
                            return
                        player1 = clock["Player1"]
                        player2 = clock["Player2"]
                    if clock["Status"] == "Finished":
                        response = "That clock is already finished!"
                        await message.channel.send(response.format(message))
                    elif clock["Status"] != "Running":
                        response = "That clock not running. Please use the !start command."
                        await message.channel.send(response.format(message))
                    else:
                        laststatus = datetime.strptime(clock["Status Time"],"%Y-%m-%d %H:%M:%S.%f")
                        if int(clock["Active Player"]) == 1:
                            remaining = player1["Remaining"]
                            activeplayer = player1["ID"]
                        else: 
                            remaining = player2["Remaining"]
                            activeplayer = player2["ID"]
                        timepassed = int((datetime.now() - laststatus).total_seconds())
                        newremaining = remaining - timepassed
                        if newremaining <= 0:
                            newremaining = 0
                        if int(clock["Active Player"]) == 1:
                            colour = 0xaa3333
                            playerone = "__**" + player1["Name"] + "**__"
                            playertwo = player2["Name"]
                            p1hours = str(int(newremaining / 3600))
                            p1minutes = str(int(newremaining / 60))
                            p1seconds = str(int(newremaining % 60))
                            p2hours = str(int(player2["Remaining"] / 3600))
                            p2minutes = str(int((player2["Remaining"] % 3600)/60))
                            p2seconds = str(player2["Remaining"] % 60)
                        else:
                            colour = 0x3333aa
                            playerone = player1["Name"]
                            playertwo = "__**" + player2["Name"] + "**__"
                            p1hours = str(int(player1["Remaining"] / 3600))
                            p1minutes = str(int((player1["Remaining"] % 3600)/60))
                            p1seconds = str(player1["Remaining"] % 60)           
                            p2hours = str(int(newremaining / 3600))
                            p2minutes = str(int(newremaining / 60))
                            p2seconds = str(int(newremaining % 60))       
                        if newremaining == 0:
                            colour = 0x000000                               
                        #await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                        #embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                        p1remaining = '%02d' % int(p1hours) + ":" + '%02d' % int(p1minutes) + ":" + '%02d' % int(p1seconds)
                        p2remaining = '%02d' % int(p2hours) + ":" + '%02d' % int(p2minutes) + ":" + '%02d' % int(p2seconds)
                        description = "".join([player1["Name"], " vs ", player2["Name"]])
                        embed = discord.Embed(title="Chess Clock", description=description, color=colour)
                        embed.add_field(name="ID", value=id, inline=False)
                        embed.add_field(name=playerone, value="`" + p1remaining + "`", inline=True) 
                        embed.add_field(name=playertwo, value="`" + p2remaining + "` ", inline=True) 
                        if newremaining > 0:
                            embed.add_field(name="Status", value="Running", inline=False)
                        else:
                            embed.add_field(name="Status", value="Finished", inline=False)
                            response = "".join(["Your clock has expired, <@", str(activeplayer), ">!"])
                            await message.channel.send(response.format(message))
                        embed.add_field(name="Pauses", value="".join([str(clock["Pauses"]),"(",str(clock["Judge Pauses"]),")"]), inline=True)
                        clockmsg = await message.channel.send(embed=embed)
                        with open(clockfile,"w") as clocks_file:
                            clocks[id]["Status Time"] = str(datetime.now())
                            clocks[id]["Message ID"] = clockmsg.id
                            if int(clock["Active Player"]) == 1:
                                clocks[id]["Player1"]["Remaining"] = newremaining
                            else:
                                clocks[id]["Player2"]["Remaining"] = newremaining
                            if newremaining == 0:
                                clocks[id]["Status"] = "Finished"
                            json.dump(clocks, clocks_file, indent=4)
                    
            return

        if message.content.lower().startswith("!switch"):
            if message.content.lower() == "!switch":
                clockfound = False
                with open(clockfile,"r") as clocks_file:
                    clocks = json.load(clocks_file)
                    for (id,clock) in clocks.items():
                        if clockfound == False:
                            player1 = clock["Player1"]
                            player2 = clock["Player2"]
                            if clock["Status"] != "Finished" and int(clock["Channel ID"]) == message.channel.id and (int(player1["ID"]) == message.author.id or int(player2["ID"]) == message.author.id):
                                clockfound = True
                                break
                if clockfound == False:
                    await message.channel.send("You do not currently have an active clock to update in this channel!".format(message))
                elif clock["Status"] == "Paused" or clock["Status"] == "Not Started":
                    if int(clock["Active Player"]) == 2: #reversed logic. it's intentional
                        playerone = "__**" + player1["Name"] + "**__"
                        playertwo = player2["Name"]
                        newplayer = 1
                    else:
                        playerone = player1["Name"]
                        playertwo = "__**" + player2["Name"] + "**__"   
                        newplayer = 2
                    if clock["Status"] == "Paused":
                        colour = 0x33aa33
                    else:
                        colour = 0xdddddd
                    p1hours = str(int(player1["Remaining"] / 3600))
                    p1minutes = str(int((player1["Remaining"] % 3600)/60))
                    p1seconds = str(player1["Remaining"] % 60)
                    p2hours = str(int(player2["Remaining"] / 3600))
                    p2minutes = str(int((player2["Remaining"] % 3600)/60))
                    p2seconds = str(player2["Remaining"] % 60)
                    p1remaining = '%02d' % int(p1hours) + ":" + '%02d' % int(p1minutes) + ":" + '%02d' % int(p1seconds)
                    p2remaining = '%02d' % int(p2hours) + ":" + '%02d' % int(p2minutes) + ":" + '%02d' % int(p2seconds)

                    description = "".join([player1["Name"], " vs ", player2["Name"]])
                    embed = discord.Embed(title="Chess Clock", description=description, color=colour)
                    embed.add_field(name="ID", value=id, inline=False)
                    embed.add_field(name=playerone, value="`" + p1remaining + "`", inline=True) 
                    embed.add_field(name=playertwo, value="`" + p2remaining + "` ", inline=True) 
                    embed.add_field(name="Status", value="Running", inline=False)
                    embed.add_field(name="Pauses", value="".join([str(clock["Pauses"]),"(",str(clock["Judge Pauses"]),")"]), inline=True)
                    clockmsg = await message.channel.send(embed=embed)
                    with open(clockfile,"w") as clocks_file:
                        clocks[id]["Status Time"] = str(datetime.now())
                        clocks[id]["Message ID"] = clockmsg.id
                        clocks[id]["Active Player"] = newplayer
                        json.dump(clocks, clocks_file, indent=4)
                else:
                    laststatus = datetime.strptime(clock["Status Time"],"%Y-%m-%d %H:%M:%S.%f")
                    if int(clock["Active Player"]) == 1:
                        remaining = player1["Remaining"]
                        activeplayer = player1["ID"]
                    else: 
                        remaining = player2["Remaining"]
                        activeplayer = player2["ID"]
                    timepassed = int((datetime.now() - laststatus).total_seconds())
                    newremaining = remaining - timepassed
                    if newremaining <= 0:
                        newremaining = 0
                    if int(clock["Active Player"]) == 1:
                        colour = 0x3333aa
                        playerone = player1["Name"]
                        playertwo = "__**" + player2["Name"] + "**__"
                        p1hours = str(int(newremaining / 3600))
                        p1minutes = str(int(newremaining / 60))
                        p1seconds = str(int(newremaining % 60))
                        p2hours = str(int(player2["Remaining"] / 3600))
                        p2minutes = str(int((player2["Remaining"] % 3600)/60))
                        p2seconds = str(player2["Remaining"] % 60)
                    else:
                        colour = 0xaa3333
                        playerone = "__**" +player1["Name"] + "**__"
                        playertwo = player2["Name"]
                        p1hours = str(int(player1["Remaining"] / 3600))
                        p1minutes = str(int((player1["Remaining"] % 3600)/60))
                        p1seconds = str(player1["Remaining"] % 60)           
                        p2hours = str(int(newremaining / 3600))
                        p2minutes = str(int(newremaining / 60))
                        p2seconds = str(int(newremaining % 60))       
                    if newremaining == 0:
                        colour = 0x000000                               
                    #await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                    #embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                    p1remaining = '%02d' % int(p1hours) + ":" + '%02d' % int(p1minutes) + ":" + '%02d' % int(p1seconds)
                    p2remaining = '%02d' % int(p2hours) + ":" + '%02d' % int(p2minutes) + ":" + '%02d' % int(p2seconds)
                    description = "".join([player1["Name"], " vs ", player2["Name"]])
                    embed = discord.Embed(title="Chess Clock", description=description, color=colour)
                    embed.add_field(name="ID", value=id, inline=False)
                    embed.add_field(name=playerone, value="`" + p1remaining + "`", inline=True) 
                    embed.add_field(name=playertwo, value="`" + p2remaining + "` ", inline=True) 
                    if newremaining > 0:
                        embed.add_field(name="Status", value="Running", inline=False)
                    else:
                        embed.add_field(name="Status", value="Finished", inline=False)
                        response = "".join(["Your clock has expired, <@", str(activeplayer), ">!"])
                        await message.channel.send(response.format(message))
                    embed.add_field(name="Pauses", value="".join([str(clock["Pauses"]),"(",str(clock["Judge Pauses"]),")"]), inline=True)
                    clockmsg = await message.channel.send(embed=embed)
                    with open(clockfile,"w") as clocks_file:
                        clocks[id]["Status Time"] = str(datetime.now())
                        clocks[id]["Message ID"] = clockmsg.id
                        if int(clock["Active Player"]) == 1:
                            clocks[id]["Player1"]["Remaining"] = newremaining
                            clocks[id]["Active Player"] = 2
                        else:
                            clocks[id]["Player2"]["Remaining"] = newremaining
                            clocks[id]["Active Player"] = 1
                        if newremaining == 0:
                            clocks[id]["Status"] = "Finished"
                        json.dump(clocks, clocks_file, indent=4)

            return

        if message.content.lower().startswith("!end"):
            if message.content.lower() == "!end":
                clockfound = False
                with open(clockfile,"r") as clocks_file:
                    clocks = json.load(clocks_file)
                    for (id,clock) in clocks.items():
                        if clockfound == False:
                            player1 = clock["Player1"]
                            player2 = clock["Player2"]
                            if clock["Status"] != "Finished" and int(clock["Channel ID"]) == message.channel.id and (int(player1["ID"]) == message.author.id or int(player2["ID"]) == message.author.id):
                                clockfound = True
                if clockfound == False:
                    await message.channel.send("You do not currently have an active clock to end in this channel!".format(message))
                elif clock["Status"] != "Running":
                    #await message.channel.delete(clockmsg)
                    #await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")

                    p1hours = str(int(player1["Remaining"] / 3600))
                    p1minutes = str(int((player1["Remaining"] % 3600)/60))
                    p1seconds = str(player1["Remaining"] % 60)           
                    p2hours = str(int(player2["Remaining"] / 3600))
                    p2minutes = str(int((player2["Remaining"] % 3600)/60))
                    p2seconds = str(player2["Remaining"] % 60)           
                    p1remaining = '%02d' % int(p1hours) + ":" + '%02d' % int(p1minutes) + ":" + '%02d' % int(p1seconds)
                    p2remaining = '%02d' % int(p2hours) + ":" + '%02d' % int(p2minutes) + ":" + '%02d' % int(p2seconds)

                    description = "".join([player1["Name"], " vs ", player2["Name"]])
                    embed = discord.Embed(title="Chess Clock", description=description, color=0x000000)
                    embed.add_field(name="ID", value=id, inline=False)
                    embed.add_field(name=player1["Name"], value="`" + p1remaining + "`", inline=True) 
                    embed.add_field(name=player2["Name"], value="`" + p2remaining + "` ", inline=True) 
                    embed.add_field(name="Status", value="Finished", inline=False)
                    embed.add_field(name="Pauses", value="".join([str(clock["Pauses"]),"(",str(clock["Judge Pauses"]),")"]), inline=True)
                    clockmsg = await message.channel.send(embed=embed)
                    with open(clockfile,"w") as clocks_file:
                        clocks[id]["Status"] = "Finished"
                        clocks[id]["Message ID"] = clockmsg.id
                        json.dump(clocks, clocks_file, indent=4)
                else:
                    laststatus = datetime.strptime(clock["Status Time"],"%Y-%m-%d %H:%M:%S.%f")
                    if int(clock["Active Player"]) == 1:
                        remaining = player1["Remaining"]
                        activeplayer = player1["ID"]
                    else: 
                        remaining = player2["Remaining"]
                        activeplayer = player2["ID"]
                    timepassed = int((datetime.now() - laststatus).total_seconds())
                    newremaining = remaining - timepassed
                    if newremaining <= 0:
                        newremaining = 0
                    if int(clock["Active Player"]) == 1:
                        playerone = "__**" + player1["Name"] + "**__"
                        playertwo = player2["Name"]
                        p1hours = str(int(newremaining / 3600))
                        p1minutes = str(int(newremaining / 60))
                        p1seconds = str(int(newremaining % 60))
                        p2hours = str(int(player2["Remaining"] / 3600))
                        p2minutes = str(int((player2["Remaining"] % 3600)/60))
                        p2seconds = str(player2["Remaining"] % 60)
                    else:
                        playerone = player1["Name"]
                        playertwo = "__**" + player2["Name"] + "**__"
                        p1hours = str(int(player1["Remaining"] / 3600))
                        p1minutes = str(int((player1["Remaining"] % 3600)/60))
                        p1seconds = str(player1["Remaining"] % 60)           
                        p2hours = str(int(newremaining / 3600))
                        p2minutes = str(int(newremaining / 60))
                        p2seconds = str(int(newremaining % 60))      

                    colour = 0x000000                               
                    #await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                    #embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                    p1remaining = '%02d' % int(p1hours) + ":" + '%02d' % int(p1minutes) + ":" + '%02d' % int(p1seconds)
                    p2remaining = '%02d' % int(p2hours) + ":" + '%02d' % int(p2minutes) + ":" + '%02d' % int(p2seconds)
                    description = "".join([player1["Name"], " vs ", player2["Name"]])
                    embed = discord.Embed(title="Chess Clock", description=description, color=colour)
                    embed.add_field(name="ID", value=id, inline=False)
                    embed.add_field(name=playerone, value="`" + p1remaining + "`", inline=True) 
                    embed.add_field(name=playertwo, value="`" + p2remaining + "` ", inline=True) 
                    if newremaining == 0:
                        response = "".join(["Your clock has expired, <@", str(activeplayer), ">!"])
                        await message.channel.send(response.format(message))
                    embed.add_field(name="Status", value="Finished", inline=False)
                    embed.add_field(name="Pauses", value="".join([str(clock["Pauses"]),"(",str(clock["Judge Pauses"]),")"]), inline=True)
                    clockmsg = await message.channel.send(embed=embed)
                    with open(clockfile,"w") as clocks_file:
                        clocks[id]["Status Time"] = str(datetime.now())
                        clocks[id]["Message ID"] = clockmsg.id
                        if int(clock["Active Player"]) == 1:
                            clocks[id]["Player1"]["Remaining"] = newremaining
                        else:
                            clocks[id]["Player2"]["Remaining"] = newremaining
                        clocks[id]["Status"] = "Finished"
                        json.dump(clocks, clocks_file, indent=4)
            else:
                roles = message.author.roles
                isJudge = False
                for role in roles:
                    if role.name == "Judge":
                        isJudge = True
                if isJudge == False:
                    await message.channel.send("You must be a Judge to effect Chess Clocks with an ID.")
                else:
                    id = message.content.lower()[5:]
                    with open(clockfile,"r") as clocks_file:
                        clocks = json.load(clocks_file)
                        try:
                            clock = clocks[id]
                        except:
                            response = "That clock doesn't exist!"
                            await message.channel.send(response.format(message))             
                            return
                        player1 = clock["Player1"]
                        player2 = clock["Player2"]
                    if clock["Status"] == "Finished":
                        response = "That clock is already finished!"
                        await message.channel.send(response.format(message))     
                        #await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                    if clock["Status"] != "Running":
                        p1hours = str(int(player1["Remaining"] / 3600))
                        p1minutes = str(int((player1["Remaining"] % 3600)/60))
                        p1seconds = str(player1["Remaining"] % 60)           
                        p2hours = str(int(player2["Remaining"] / 3600))
                        p2minutes = str(int((player2["Remaining"] % 3600)/60))
                        p2seconds = str(player2["Remaining"] % 60)           
                        p1remaining = '%02d' % int(p1hours) + ":" + '%02d' % int(p1minutes) + ":" + '%02d' % int(p1seconds)
                        p2remaining = '%02d' % int(p2hours) + ":" + '%02d' % int(p2minutes) + ":" + '%02d' % int(p2seconds)

                        description = "".join([player1["Name"], " vs ", player2["Name"]])
                        embed = discord.Embed(title="Chess Clock", description=description, color=0x000000)
                        embed.add_field(name="ID", value=id, inline=False)
                        embed.add_field(name=player1["Name"], value="`" + p1remaining + "`", inline=True) 
                        embed.add_field(name=player2["Name"], value="`" + p2remaining + "` ", inline=True) 
                        embed.add_field(name="Status", value="Finished", inline=False)
                        embed.add_field(name="Pauses", value="".join([str(clock["Pauses"]),"(",str(clock["Judge Pauses"]),")"]), inline=True)
                        clockmsg = await message.channel.send(embed=embed)
                        with open(clockfile,"w") as clocks_file:
                            clocks[id]["Status"] = "Finished"
                            clocks[id]["Message ID"] = clockmsg.id
                            json.dump(clocks, clocks_file, indent=4)
                    else:
                        laststatus = datetime.strptime(clock["Status Time"],"%Y-%m-%d %H:%M:%S.%f")
                        if int(clock["Active Player"]) == 1:
                            remaining = player1["Remaining"]
                            activeplayer = player1["ID"]
                        else: 
                            remaining = player2["Remaining"]
                            activeplayer = player2["ID"]
                        timepassed = int((datetime.now() - laststatus).total_seconds())
                        newremaining = remaining - timepassed
                        if newremaining <= 0:
                            newremaining = 0
                        if int(clock["Active Player"]) == 1:
                            playerone = "__**" + player1["Name"] + "**__"
                            playertwo = player2["Name"]
                            p1hours = str(int(newremaining / 3600))
                            p1minutes = str(int(newremaining / 60))
                            p1seconds = str(int(newremaining % 60))
                            p2hours = str(int(player2["Remaining"] / 3600))
                            p2minutes = str(int((player2["Remaining"] % 3600)/60))
                            p2seconds = str(player2["Remaining"] % 60)
                        else:
                            playerone = player1["Name"]
                            playertwo = "__**" + player2["Name"] + "**__"
                            p1hours = str(int(player1["Remaining"] / 3600))
                            p1minutes = str(int((player1["Remaining"] % 3600)/60))
                            p1seconds = str(player1["Remaining"] % 60)           
                            p2hours = str(int(newremaining / 3600))
                            p2minutes = str(int(newremaining / 60))
                            p2seconds = str(int(newremaining % 60))      
    
                        colour = 0x000000                               
                        #await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                        #embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                        p1remaining = '%02d' % int(p1hours) + ":" + '%02d' % int(p1minutes) + ":" + '%02d' % int(p1seconds)
                        p2remaining = '%02d' % int(p2hours) + ":" + '%02d' % int(p2minutes) + ":" + '%02d' % int(p2seconds)
                        description = "".join([player1["Name"], " vs ", player2["Name"]])
                        embed = discord.Embed(title="Chess Clock", description=description, color=colour)
                        embed.add_field(name="ID", value=id, inline=False)
                        embed.add_field(name=playerone, value="`" + p1remaining + "`", inline=True) 
                        embed.add_field(name=playertwo, value="`" + p2remaining + "` ", inline=True) 
                        if newremaining == 0:
                            response = "".join(["Your clock has expired, <@", str(activeplayer), ">!"])
                            await message.channel.send(response.format(message))
                        embed.add_field(name="Status", value="Finished", inline=False)
                        embed.add_field(name="Pauses", value="".join([str(clock["Pauses"]),"(",str(clock["Judge Pauses"]),")"]), inline=True)
                        clockmsg = await message.channel.send(embed=embed)
                        with open(clockfile,"w") as clocks_file:
                            clocks[id]["Status Time"] = str(datetime.now())
                            clocks[id]["Message ID"] = clockmsg.id
                            if int(clock["Active Player"]) == 1:
                                clocks[id]["Player1"]["Remaining"] = newremaining
                            else:
                                clocks[id]["Player2"]["Remaining"] = newremaining
                            clocks[id]["Status"] = "Finished"
                            json.dump(clocks, clocks_file, indent=4)
            return

        if message.content.lower().startswith("!pause"):
            if message.content.lower() == "!pause":
                clockfound = False
                with open(clockfile,"r") as clocks_file:
                    clocks = json.load(clocks_file)
                    for (id,clock) in clocks.items():
                        if clockfound == False:
                            player1 = clock["Player1"]
                            player2 = clock["Player2"]
                            if clock["Status"] != "Finished" and int(clock["Channel ID"]) == message.channel.id and (int(player1["ID"]) == message.author.id or int(player2["ID"]) == message.author.id):
                                clockfound = True
                if clockfound == False:
                    await message.channel.send("You do not currently have an active clock to end in this channel!".format(message))
                elif clock["Status"] != "Running":
                    await message.channel.send("Your clock is not currently running. Use the !start command.".format(message))
                else:
                    laststatus = datetime.strptime(clock["Status Time"],"%Y-%m-%d %H:%M:%S.%f")
                    if int(clock["Active Player"]) == 1:
                        remaining = player1["Remaining"]
                        activeplayer = player1["ID"]
                    else: 
                        remaining = player2["Remaining"]
                        activeplayer = player2["ID"]
                    timepassed = int((datetime.now() - laststatus).total_seconds())
                    newremaining = remaining - timepassed
                    if newremaining <= 0:
                        newremaining = 0
                    if int(clock["Active Player"]) == 1:
                        playerone = "__**" + player1["Name"] + "**__"
                        playertwo = player2["Name"]
                        p1hours = str(int(newremaining / 3600))
                        p1minutes = str(int(newremaining / 60))
                        p1seconds = str(int(newremaining % 60))
                        p2hours = str(int(player2["Remaining"] / 3600))
                        p2minutes = str(int((player2["Remaining"] % 3600)/60))
                        p2seconds = str(player2["Remaining"] % 60)
                    else:
                        playerone = player1["Name"]
                        playertwo = "__**" + player2["Name"] + "**__"
                        p1hours = str(int(player1["Remaining"] / 3600))
                        p1minutes = str(int((player1["Remaining"] % 3600)/60))
                        p1seconds = str(player1["Remaining"] % 60)           
                        p2hours = str(int(newremaining / 3600))
                        p2minutes = str(int(newremaining / 60))
                        p2seconds = str(int(newremaining % 60))      

                    colour = 0x33aa33                            
                    #await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                    #embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                    p1remaining = '%02d' % int(p1hours) + ":" + '%02d' % int(p1minutes) + ":" + '%02d' % int(p1seconds)
                    p2remaining = '%02d' % int(p2hours) + ":" + '%02d' % int(p2minutes) + ":" + '%02d' % int(p2seconds)
                    description = "".join([player1["Name"], " vs ", player2["Name"]])
                    embed = discord.Embed(title="Chess Clock", description=description, color=colour)
                    embed.add_field(name="ID", value=id, inline=False)
                    embed.add_field(name=playerone, value="`" + p1remaining + "`", inline=True) 
                    embed.add_field(name=playertwo, value="`" + p2remaining + "` ", inline=True) 
                    if newremaining == 0:
                        response = "".join(["Your clock has expired, <@", str(activeplayer), ">!"])
                        await message.channel.send(response.format(message))
                        embed.add_field(name="Status", value="Finished", inline=False)
                    else:
                        embed.add_field(name="Status", value="Paused", inline=False)
                    embed.add_field(name="Pauses", value="".join([str(int(str(clock["Pauses"]))+1),"(",str(clock["Judge Pauses"]),")"]), inline=True)
                    clockmsg = await message.channel.send(embed=embed)
                    with open(clockfile,"w") as clocks_file:
                        clocks[id]["Status Time"] = str(datetime.now())
                        clocks[id]["Message ID"] = clockmsg.id
                        clocks[id]["Pauses"] = str(int(str(clock["Pauses"]))+1)
                        if int(clock["Active Player"]) == 1:
                            clocks[id]["Player1"]["Remaining"] = newremaining
                        else:
                            clocks[id]["Player2"]["Remaining"] = newremaining
                        if newremaining == 0:
                            clocks[id]["Status"] = "Finished"
                        else:
                            clocks[id]["Status"] = "Paused"
                        json.dump(clocks, clocks_file, indent=4)
            else:
                roles = message.author.roles
                isJudge = False
                for role in roles:
                    if role.name == "Judge":
                        isJudge = True
                if isJudge == False:
                    await message.channel.send("You must be a Judge to effect Chess Clocks with an ID.")
                else:
                    id = message.content.lower()[7:]
                    with open(clockfile,"r") as clocks_file:
                        clocks = json.load(clocks_file)
                        try:
                            clock = clocks[id]
                        except:
                            response = "That clock doesn't exist!"
                            await message.channel.send(response.format(message))             
                            return
                        player1 = clock["Player1"]
                        player2 = clock["Player2"]
                    if clock["Status"] == "Finished":
                        response = "That clock is already finished!"
                        await message.channel.send(response.format(message))     
                        #await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                    if clock["Status"] != "Running":
                        await message.channel.send("That clock is not currently running. Use the !start command.".format(message))
                    else:
                        laststatus = datetime.strptime(clock["Status Time"],"%Y-%m-%d %H:%M:%S.%f")
                        if int(clock["Active Player"]) == 1:
                            remaining = player1["Remaining"]
                            activeplayer = player1["ID"]
                        else: 
                            remaining = player2["Remaining"]
                            activeplayer = player2["ID"]
                        timepassed = int((datetime.now() - laststatus).total_seconds())
                        newremaining = remaining - timepassed
                        if newremaining <= 0:
                            newremaining = 0
                        if int(clock["Active Player"]) == 1:
                            playerone = "__**" + player1["Name"] + "**__"
                            playertwo = player2["Name"]
                            p1hours = str(int(newremaining / 3600))
                            p1minutes = str(int(newremaining / 60))
                            p1seconds = str(int(newremaining % 60))
                            p2hours = str(int(player2["Remaining"] / 3600))
                            p2minutes = str(int((player2["Remaining"] % 3600)/60))
                            p2seconds = str(player2["Remaining"] % 60)
                        else:
                            playerone = player1["Name"]
                            playertwo = "__**" + player2["Name"] + "**__"
                            p1hours = str(int(player1["Remaining"] / 3600))
                            p1minutes = str(int((player1["Remaining"] % 3600)/60))
                            p1seconds = str(player1["Remaining"] % 60)           
                            p2hours = str(int(newremaining / 3600))
                            p2minutes = str(int(newremaining / 60))
                            p2seconds = str(int(newremaining % 60))      
    
                        colour = 0x33aa33                              
                        #await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                        #embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                        p1remaining = '%02d' % int(p1hours) + ":" + '%02d' % int(p1minutes) + ":" + '%02d' % int(p1seconds)
                        p2remaining = '%02d' % int(p2hours) + ":" + '%02d' % int(p2minutes) + ":" + '%02d' % int(p2seconds)
                        description = "".join([player1["Name"], " vs ", player2["Name"]])
                        embed = discord.Embed(title="Chess Clock", description=description, color=colour)
                        embed.add_field(name="ID", value=id, inline=False)
                        embed.add_field(name=playerone, value="`" + p1remaining + "`", inline=True) 
                        embed.add_field(name=playertwo, value="`" + p2remaining + "` ", inline=True) 
                        if newremaining == 0:
                            response = "".join(["Your clock has expired, <@", str(activeplayer), ">!"])
                            await message.channel.send(response.format(message))
                        embed.add_field(name="Status", value="Finished", inline=False)
                        embed.add_field(name="Pauses", value="".join([str(int(str(clock["Pauses"]))+1),"(",str(int(str(clock["Judge Pauses"]))+1),")"]), inline=True)
                        clockmsg = await message.channel.send(embed=embed)
                        with open(clockfile,"w") as clocks_file:
                            clocks[id]["Status Time"] = str(datetime.now())
                            clocks[id]["Message ID"] = clockmsg.id
                            clocks[id]["Pauses"] = str(int(str(clock["Pauses"]))+1)
                            clocks[id]["Judge Pauses"] = str(int(str(clock["Judge Pauses"]))+1)
                            if int(clock["Active Player"]) == 1:
                                clocks[id]["Player1"]["Remaining"] = newremaining
                            else:
                                clocks[id]["Player2"]["Remaining"] = newremaining
                            if newremaining == 0:
                                clocks[id]["Status"] = "Finished"
                            else:
                                clocks[id]["Status"] = "Paused"
                            json.dump(clocks, clocks_file, indent=4)
            return
            

        #####################################
        # Here end the Chess Clock Commands #
        #####################################

        if message.content.lower() == "!test":
            botmsg = await message.channel.send("testing".format(message))
            time.sleep(2)
            await botmsg.edit(content="test complete".format(message))
            return

        if " judge" in message.content.lower() or "judge " in message.content.lower():
            image = directory + "/Images/legal.gif"
            print(image)
            await message.channel.send(file=discord.File(image))

        if " flex" in message.content.lower() or "flex " in message.content.lower():
            image = directory + "/Images/flex.gif"
            print(image)
            await message.channel.send(file=discord.File(image))

        if "infernals" in message.content.lower():
            image = directory + "/Images/scared.gif"
            print(image)
            await message.channel.send(file=discord.File(image))

        if " win" in message.content.lower() or "win " in message.content.lower():
            image = directory + "/Images/collection.gif"
            print(image)
            await message.channel.send(file=discord.File(image))

        if " play" in message.content.lower() or "play " in message.content.lower():
            image = directory + "/Images/duel.gif"
            print(image)
            await message.channel.send(file=discord.File(image))

        if "balance" in message.content.lower():
            image = directory + "/Images/balanced.gif"
            print(image)
            await message.channel.send(file=discord.File(image))

client = MyClient()
client.run(key)