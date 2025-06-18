import os
import json
import secrets

import discord
from discord import app_commands
import asyncio

# https://discordpy.readthedocs.io/en/stable/api.html

if "DISCORD_GUILD_ID" in os.environ:
    MY_GUILD = discord.Object(id=int(os.environ["DISCORD_GUILD_ID"].strip()))
else:
    MY_GUILD = discord.Object(id=int(open("guild.secret").read().strip()))
TYPING_BOT = int(os.environ.get("TYPING_BOT", "0"))
DISCORD_REACTION_MSGID = int(os.environ.get("DISCORD_REACTION_MSGID", "978574978914082836"))

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
        self.load_reaction_counts()
        print(f'Logged on as {self.user}!')

    """
    async def on_reaction_add(reaction, user):
        if reaction.message.id == DISCORD_REACTION_MSGID:
            print(reaction)
            print(user)
    """
    async def on_raw_reaction_add(self, payload):
        #message = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if payload.message_id == DISCORD_REACTION_MSGID:
            guild = self.get_guild(payload.guild_id)
            member = payload.member # only available if reaction add & inside guild...
            try:
                if payload.emoji.name == "💻":
                    #await member.add_roles(guild.get_role(389678983605911554))
                    pass
                elif payload.emoji.name == "👀":
                    #await member.add_roles(guild.get_role(911464059830927401))
                    pass
                elif payload.emoji.name == "⚡":
                    await member.add_roles(guild.get_role(1061715448531525732))
                #elif payload.emoji.name == "😔":
                #    await member.add_roles(guild.get_role(1230232895671500901))
            except Exception as e:
                print(payload, flush=True)
                print(e, flush=True)
    async def on_raw_reaction_remove(self, payload):
        #message = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if payload.message_id == DISCORD_REACTION_MSGID:
            guild = self.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if member is None:
                return
            try:
                if payload.emoji.name == "💻":
                    #await member.remove_roles(guild.get_role(389678983605911554))
                    pass
                elif payload.emoji.name == "👀":
                    #await member.remove_roles(guild.get_role(911464059830927401))
                    pass
                elif payload.emoji.name == "⚡":
                    await member.remove_roles(guild.get_role(1061715448531525732))
                #elif payload.emoji.name == "😔":
                #    await member.remove_roles(guild.get_role(1230232895671500901))
            except Exception as e:
                print(payload, flush=True)
                print(e, flush=True)

    async def send_typing(self, user, channel):
        if not TYPING_BOT or user.id == self.user.id:
            return
        #if not channel.permissions_for(self.user).send_messages:
        #    return
        try:
            async with channel.typing():
                await asyncio.sleep(3.5)
        except:
            pass

    def load_reaction_counts(self):
        with open("reaction_counts.json", "r", encoding="utf-8") as f:
            self.reaction_counts = json.load(f)
    def save_reaction_counts(self):
        with open("reaction_counts.json", "w", encoding="utf-8") as f:
            json.dump(self.reaction_counts, f)
    def inc_reaction_counts(self, user_id, emoji):
        user_id = str(user_id)
        if not user_id in self.reaction_counts:
            self.reaction_counts[user_id] = {}
        if not emoji in self.reaction_counts[user_id]:
            self.reaction_counts[user_id][emoji] = 0
        self.reaction_counts[user_id][emoji] += 1
        self.save_reaction_counts()
    async def do_reaction_counts(self, message, emoji):
        await message.add_reaction(emoji)
        self.inc_reaction_counts(message.author.id, emoji)

    async def destroy_user(self, message):
        for role in message.author.roles:
            if role.id != 911464059830927401 and role.id != 1061715448531525732:
                return False
        for attachment in message.attachments:
            if "test2" in attachment.filename or "pstrafing" in attachment.filename:
                await message.author.ban(reason=f"posting sussy {attachment.filename}")
                await message.channel.send(content=f"banned {message.author.mention}")
                return True
        return False

    async def on_message(self, message):
        if not message.author.bot and not (message.guild is None):
            if await self.destroy_user(message):
                return
            await asyncio.sleep(1.0)
            if secrets.randbelow(100) == 0:
                await self.do_reaction_counts(message, "🦇")
            if secrets.randbelow(1000) == 0:
                await self.do_reaction_counts(message, ":goldbat:663437353787850763")
            if secrets.randbelow(100) == 0:
                await self.do_reaction_counts(message, ":corgi:702360708641194005")
            if secrets.randbelow(1000) == 0:
                await self.do_reaction_counts(message, ":corgibutt:788514694691553300")
        await self.send_typing(message.author, message.channel)

    async def on_typing(self, channel, user, when):
        await self.send_typing(user, channel)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
intents.typing = True

client = MyClient(intents=intents)

@client.tree.command()
async def owowhatisthis(interaction: discord.Interaction):
    await interaction.response.send_message(f'you just lost the game', ephemeral=True)

@client.tree.command()
async def top15(interaction: discord.Interaction):
    embed = discord.Embed(colour=0x7289DA)
    total_reactions = 0
    total_reactions_by_user = {}
    for (user_id, user) in client.reaction_counts.items():
        total_reactions_by_user[user_id] = 0
        for (emoji, emoji_count) in user.items():
            total_reactions += emoji_count
            total_reactions_by_user[user_id] += emoji_count
    embed.add_field(name="Total reactions:", value=str(total_reactions))
    sorted_users = [(k, total_reactions_by_user[k]) for k in sorted(total_reactions_by_user, key=total_reactions_by_user.get, reverse=True)]
    sorted_users = sorted_users[:15]
    top15_embed = ''
    for user in sorted_users:
        top15_embed += f"**\u2022** {user[1]} <@{user[0]}>"
        for (emoji, emoji_count) in client.reaction_counts[user[0]].items():
            if ":" in emoji:
                top15_embed += f" | {emoji_count}<{emoji}>"
            else:
                top15_embed += f" | {emoji_count}{emoji}"
        top15_embed += '\n'
    embed.add_field(name="Top 15 users reacted to:", value=top15_embed)
    await interaction.response.send_message(embed=embed)

@client.tree.command()
async def eyes(interaction: discord.Interaction):
    if interaction.guild is None:
        return
    if not interaction.user.guild_permissions.administrator:
        return
    asyncio.create_task(
        give_role_to_everyone(
            interaction.guild.members,
            interaction.guild.get_role(911464059830927401)
        )
    )
    await interaction.response.send_message(content="giving eyes...")

async def give_role_to_everyone(members, role):
    for member in members:
        if member.get_role(role.id) is not None:
            continue
        print(f"{role.name} {member}", flush=True)
        await member.add_roles(role)
        await asyncio.sleep(0.5)

if "DISCORD_TOKEN" in os.environ:
    client.run(os.environ["DISCORD_TOKEN"].strip())
else:
    client.run(open("token.secret").read().strip())
