import discord
import asyncio

# https://discordpy.readthedocs.io/en/stable/api.html

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        #if not message.channel.permissions_for(self.user).send_messages:
        #    return
        try:
            async with message.channel.typing():
                await asyncio.sleep(3.5)
        except:
            pass

    async def on_typing(self, channel, user, when):
        if user.id == self.user.id:
            return
        #if not channel.permissions_for(self.user).send_messages:
        #    return
        try:
            async with channel.typing():
                await asyncio.sleep(3.5)
        except:
            pass

intents = discord.Intents.default()
intents.message_content = True
intents.typing = True

client = MyClient(intents=intents)
client.run(open("token.secret").read().strip())
