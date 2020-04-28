#!/usr/bin/env python3
import discord, random, os, re

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
> !scenario: Provides a random Stream Roller 2019 Scenario.

`{}` denote parameters. Parameters wrapped in `()` are optional."""

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        game = discord.Game("Judge | !help")
        await client.change_presence(status=discord.Status.online, activity=game)

    async def on_message(self, message):
        #print('Message from {0.author}: {0.content}'.format(message))
        import time
        from datetime import datetime, timedelta
        if message.author == client.user:
            if message.content.startswith("> Timer:"):
                start = datetime.now()
                hours = message.content[10:12]
                minutes = message.content[13:15]
                seconds = message.content[16:18]
                duration = int(seconds) + (int(minutes) * 60) + (int(hours) * 60 *60)
                reason = message.content[19:]
                end = start + timedelta(seconds=duration)
                while datetime.now() < end:
                    time.sleep(0.5)
                    remaining = int((end - datetime.now()).total_seconds())
                    hours = str(int(remaining / 216000))
                    minutes = str(int((remaining % 3600)/60))
                    seconds = str(remaining % 60)
                    newcontent = "> Timer: `" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` " + reason
                    await message.edit(content=newcontent.format(message))
                newcontent = "> Timer finished! " + reason
                await message.edit(content=newcontent.format(message))        
            return

        if message.content.lower() == ("!help"):
            await message.channel.send(help)
            return

        if message.content.lower().startswith("hello"):
            image = directory + "/Images/hello.gif"
            #print(image)
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
            time = message.content[7:12]
            hours = message.content[7:9]
            minutes = message.content[10:12]
            reason = message.content[13:]
            if re.match("[0-9][0-9]:[0-5][0-9]",time):
                response = "Setting timer for " + str(int(hours)) + " hour(s) and " + str(int(minutes)) + " minute(s). Let the count down begin!"
                await message.channel.send(response.format(message))
                if reason != "":
                    reason = " - " + reason
                response = "> Timer: `" + hours + ":" + minutes + ":00" + "`" + reason
                await message.channel.send(response.format(message))
            else:
                await message.channel.send("That isn't a valid time!")
            return

client = MyClient()
client.run(key)