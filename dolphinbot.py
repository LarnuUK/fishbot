#!/usr/bin/env python3

import discord, random, os

client = discord.Client()

directory = os.path.dirname(os.path.realpath(__file__))

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

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='!Judge'))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith("!help"):
        await message.channel.send("I am here to do one thing. Try using !Judge.")

    if message.content.lower() == "hello":
        image = directory + "/hello.gif"
        #print(image)
        await message.channel.send("Hello there!")
        await message.channel.send(file=discord.File(image))

    if message.content.lower().startswith("!judge"):
        if str(message.channel).startswith("vassal"):
            #response = "I haven't been trained to give Judge calls yet, sorry {0.author.mention}. :(".format(message)
            response = "Thanks for asking for a Judgement call {0.author.mention}.".format(message)
            await message.channel.send(response)
            r = len(rulings)
            i = random.randint(0,r)
            response = rulings[i].format(message)
            await message.channel.send(response)
        else:
            response = "We're not in a game channel, {0.author.mention}. Please get my attention in the correct Vassal Game Channel. Thanks! :)".format(message)
            await message.channel.send(response)

    if message.content.lower() == "!stream":
        await message.channel.send("You can watch the Knight's Stream here: https://www.twitch.tv/knightsmachine")


#client = MyClient()
client.run('NzAzNjMyNjg2ODk1MzMzMzk0.XqRbJg.-coCvULGK3S9Q_mvuj0E1XbFU0o')