#!/usr/bin/env python3
import discord, random, os, re, json

client = discord.Client()

directory = os.path.dirname(os.path.realpath(__file__))

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
> !timer: Set a countdown timer. Syntax `!timer {hh:mm} ({reason}). Use `!timer` for more details.`
> !heret: Set a countdown timer that pings here on completion. Syntax `!heret {hh:mm} {reason}. Use `!timer` for more details.`
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
            with open("clocks.json","r") as clocks_file:
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
                embed = discord.Embed(title="Chess Clock", description=description, color=0xffffff)
                embed.add_field(name="ID", value=clockid, inline=False) 
                embed.add_field(name="__**" + message.author.name+ "**__", value="`" + time + "`", inline=True) 
                embed.add_field(name=message.mentions[0].name, value="`" + time + "` ", inline=True) 
                embed.add_field(name="Status", value="Not Started", inline=False)
                clockmsg = await message.channel.send(embed=embed)
                with open("clocks.json","w") as clocks_file:
                    newclock = {str(clockid): { "Status": "Not Started", "Status Time": str(datetime.now()), "Channel ID": message.channel.id, "Active Player": "1", "Message ID" : str(clockmsg.id), "Player1": {"Name": message.author.name, "ID": message.author.id, "Remaining": time},"Player2": {"Name": message.mentions[0].name, "ID": message.mentions[0].id, "Remaining": time}}}
                    clocks.update(newclock)
                    print(clocks)
                    json.dump(clocks, clocks_file, indent=4)
            else:
                await message.channel.send("That isn't a valid time!")
            return

        if message.content.lower().startswith("!end"):
            if message.content.lower() == "!end":
                clockfound = False
                with open("clocks.json","r") as clocks_file:
                    clocks = json.load(clocks_file)
                    for (id,clock) in clocks.items():
                        if clockfound == False:
                            player1 = clock["Player1"]
                            player2 = clock["Player2"]
                            if clock["Status"] != "Finished" and int(clock["Channel ID"]) == message.channel.id and (int(player1["ID"]) == message.author.id or int(player2["ID"]) == message.author.id):
                                clockfound = True
                                clockid = id
                                clockmsg = clock["Message ID"]
                if clockfound == False:
                    await message.channel.send("You do not currently have an active clock to end in this channel!".format(message))
                else:
                    #await message.channel.delete(clockmsg)
                    await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                    description = "".join([player1["Name"], " vs ", player2["Name"]])
                    embed = discord.Embed(title="Chess Clock", description=description, color=0x000000)
                    embed.add_field(name="ID", value=clockid, inline=False)
                    embed.add_field(name=player1["Name"], value="`" + player1["Remaining"] + "`", inline=True) 
                    embed.add_field(name=player2["Name"], value="`" + player2["Remaining"] + "` ", inline=True) 
                    embed.add_field(name="Status", value="Finished", inline=False)
                    clockmsg = await message.channel.send(embed=embed)
                    with open("clocks.json","w") as clocks_file:
                        clocks[clockid]["Status"] = "Finished"
                        clocks[clockid]["Message ID"] = clockmsg.id
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
                    clockid = message.content.lower()[5:]
                    with open("clocks.json","r") as clocks_file:
                        clocks = json.load(clocks_file)
                        clock = clocks[clockid]
                        player1 = clock["Player1"]
                        player2 = clock["Player2"]
                    if clock["Status"] != "Finished":
                        await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                        description = "".join([player1["Name"], " vs ", player2["Name"]])
                        embed = discord.Embed(title="Chess Clock", description=description, color=0x000000)
                        embed.add_field(name="ID", value=clockid, inline=False)
                        embed.add_field(name=player1["Name"], value="`" + player1["Remaining"] + "`", inline=True) 
                        embed.add_field(name=player2["Name"], value="`" + player2["Remaining"] + "` ", inline=True) 
                        embed.add_field(name="Status", value="Finished", inline=False)
                        clockmsg = await message.channel.send(embed=embed)
                        with open("clocks.json","w") as clocks_file:
                            clocks[clockid]["Status"] = "Finished"
                            clocks[clockid]["Message ID"] = clockmsg.id
                            json.dump(clocks, clocks_file, indent=4)
                    else:
                        response = "That clock is already finished!"
                        await message.channel.send(response.format(message))      
            return

        if message.content.lower().startswith("!start"):
            if message.content.lower() == "!start":
                clockfound = False
                with open("clocks.json","r") as clocks_file:
                    clocks = json.load(clocks_file)
                    for (id,clock) in clocks.items():
                        if clockfound == False:
                            player1 = clock["Player1"]
                            player2 = clock["Player2"]
                            if clock["Status"] != "Finished" and int(clock["Channel ID"]) == message.channel.id and (int(player1["ID"]) == message.author.id or int(player2["ID"]) == message.author.id):
                                clockfound = True
                                clockid = id
                                clockmsg = clock["Message ID"]
                                active = clock["Active Player"]
                if clockfound == False:
                    await message.channel.send("You do not currently have an active clock to end in this channel!".format(message))
                else:
                    if int(active) == 1:
                        colour = 0xdd0000
                        playerone = "__**" + player1["Name"] + "**__"
                        playertwo = player2["Name"]
                    else:
                        colour = 0x0000dd
                        playerone = player1["Name"]
                        playertwo = "__**" + player2["Name"] + "**__"                        
                    #await message.channel.delete(clockmsg)
                    await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                    description = "".join([player1["Name"], " vs ", player2["Name"]])
                    embed = discord.Embed(title="Chess Clock", description=description, color=colour)
                    embed.add_field(name="ID", value=clockid, inline=False)
                    embed.add_field(name=playerone, value="`" + player1["Remaining"] + "`", inline=True) 
                    embed.add_field(name=playertwo, value="`" + player2["Remaining"] + "` ", inline=True) 
                    embed.add_field(name="Status", value="Running", inline=False)
                    clockmsg = await message.channel.send(embed=embed)
                    with open("clocks.json","w") as clocks_file:
                        clocks[clockid]["Status"] = "Running"
                        clocks[clockid]["Status Time"] = str(datetime.now())
                        clocks[clockid]["Message ID"] = clockmsg.id
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
                    clockid = message.content.lower()[7:]
                    with open("clocks.json","r") as clocks_file:
                        clocks = json.load(clocks_file)
                    clock = clocks[clockid]
                    player1 = clock["Player1"]
                    player2 = clock["Player2"]
                    if clock["Status"] != "Finished":
                        if int(clock["Active Player"]) == 1:
                            colour = 0xdd0000
                            playerone = "__**" + player1["Name"] + "**__"
                            playertwo = player2["Name"]
                        else:
                            colour = 0x0000dd
                            playerone = player1["Name"]
                            playertwo = "__**" + player2["Name"] + "**__"             
                        await message.channel.send("I would delete the prior message, with the clock times, but Python or DiscordPy is being dick. If you want to solve the problem, suck it.")
                        description = "".join([player1["Name"], " vs ", player2["Name"]])
                        embed = discord.Embed(title="Chess Clock", description=description, color=colour)
                        embed.add_field(name="ID", value=clockid, inline=False)
                        embed.add_field(name=playerone, value="`" + player1["Remaining"] + "`", inline=True) 
                        embed.add_field(name=playertwo, value="`" + player2["Remaining"] + "` ", inline=True) 
                        embed.add_field(name="Status", value="Running", inline=False)
                        clockmsg = await message.channel.send(embed=embed)
                        with open("clocks.json","w") as clocks_file:
                            clocks[clockid]["Status"] = "Running"
                            clocks[clockid]["Status Time"] = str(datetime.now())
                            clocks[clockid]["Message ID"] = clockmsg.id
                            json.dump(clocks, clocks_file, indent=4)
                    else:
                        response = "That clock is already finished!"
                        await message.channel.send(response.format(message))      
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