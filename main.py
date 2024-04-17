from typing import Optional
import discord
from discord import app_commands
import asyncio

# https://discordpy.readthedocs.io/en/stable/api.html

MY_GUILD = discord.Object(id=int(open("guild.secret").read().strip()))
TYPING_BOT = False

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

    """
    async def on_reaction_add(reaction, user):
        if reaction.message.id == 978574978914082836:
            print(reaction)
            print(user)
    """
    async def on_raw_reaction_add(self, payload):
        #message = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if payload.message_id == 978574978914082836:
            guild = self.get_guild(payload.guild_id)
            member = payload.member # only available if reaction add & inside guild...
            try:
                if payload.emoji.name == "💻":
                    await member.add_roles(guild.get_role(389678983605911554))
                elif payload.emoji.name == "👀":
                    await member.add_roles(guild.get_role(911464059830927401))
                elif payload.emoji.name == "⚡":
                    await member.add_roles(guild.get_role(1061715448531525732))
                #elif payload.emoji.name == "😔":
                #    await member.add_roles(guild.get_role(1230232895671500901))
            except Exception as e:
                print(payload)
                print(e)
    async def on_raw_reaction_remove(self, payload):
        #message = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if payload.message_id == 978574978914082836:
            guild = self.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if member is None:
                return
            try:
                if payload.emoji.name == "💻":
                    await member.remove_roles(guild.get_role(389678983605911554))
                elif payload.emoji.name == "👀":
                    await member.remove_roles(guild.get_role(911464059830927401))
                elif payload.emoji.name == "⚡":
                    await member.remove_roles(guild.get_role(1061715448531525732))
                #elif payload.emoji.name == "😔":
                #    await member.remove_roles(guild.get_role(1230232895671500901))
            except Exception as e:
                print(payload)
                print(e)

    async def on_message(self, message):
        if not TYPING_BOT or message.author.id == self.user.id:
            return
        #if not message.channel.permissions_for(self.user).send_messages:
        #    return
        try:
            async with message.channel.typing():
                await asyncio.sleep(3.5)
        except:
            pass

    async def on_typing(self, channel, user, when):
        if not TYPING_BOT or user.id == self.user.id:
            return
        #if not channel.permissions_for(self.user).send_messages:
        #    return
        try:
            async with channel.typing():
                await asyncio.sleep(3.5)
        except:
            pass

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
intents.typing = True

client = MyClient(intents=intents)

@client.tree.command()
async def owowhatisthis(interaction: discord.Interaction):
    await interaction.response.send_message(f'you just lost the game', ephemeral=True)

client.run(open("token.secret").read().strip())
