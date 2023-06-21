# load ptyhon .dotenv pacgae
from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from discord.ext import commands, tasks
import requests

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
intents.typing = False
intents.presences = False
client = ChatClient(intents=intents)

webhook_url = 'https://discord.com/api/webhooks/1121197210055487488/ZeFBn5SDLXiybvaEzhBLA78IvCivMqQg33aSeybx1A3TxCJr-PoMXd_ypk43ycXgZMjg'


@tasks.loop(minutes=1)  # run this task every 1 minute
async def check_github_update():
    repo = 'AntonOsika/gpt-engineer'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    url = f'https://api.github.com/repos/{repo}/commits'

    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Get the latest commit
    latest_commit = data[0]['sha']
    
    try:
        with open('last_commit.txt', 'r') as file:
            last_commit = file.read()
    except FileNotFoundError:
        with open('last_commit.txt', 'w') as file:
            file.write(latest_commit)
        return

    if latest_commit != last_commit:
        data = {
            "content": f"The repository {repo} has been updated! The latest commit is {latest_commit}."
        }
        requests.post(webhook_url, json=data)
        with open('last_commit.txt', 'w') as file:
            file.write(latest_commit)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    check_github_update.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(GPT_ENGINEER_GUILD)