from typing import Optional
import discord
from discord import app_commands
import asyncio

# https://discordpy.readthedocs.io/en/stable/api.html

MY_GUILD = discord.Object(id=int(open("guild.secret").read().strip()))

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

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

@client.tree.command()
async def owowhatisthis(interaction: discord.Interaction):
    await interaction.response.send_message(f'you just lost the game', ephemeral=True)

client.run(open("token.secret").read().strip())
