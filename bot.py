# load ptyhon .dotenv pacgae
from dotenv import load_dotenv
import os
import discord
from discord import app_commands

load_dotenv()

bot_url = "https://discord.com/api/oauth2/authorize?client_id=1121065704091815976&permissions=8&scope=bot"


GPT_ENGINEER_GUILD = os.getenv("DISCORD_APP_ENGINEER_GUILD")

guild_ids = [GPT_ENGINEER_GUILD]

sync_all = True

# Initiate the client and command tree to create slash commands.
class ChatClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        if GPT_ENGINEER_GUILD and not sync_all:
            # When testing the bot it's handy to run in a single server (called a
            # Guide in the API).  This is relatively fast.
            for guild_id in guild_ids:
                guild = discord.Object(id=guild_id)
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()
        print("Ready")
            #This can take up to an hour for the commands to be registered.
        #print("Ready!")

# List the set of intents needed for commands to operate properly.
intents = discord.Intents.default()
intents.message_content = True
client = ChatClient(intents=intents)
sent_buttons = None


# This example requires the 'message_content' intent.

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(GPT_ENGINEER_GUILD)