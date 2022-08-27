import nextcord as nc
import os, sys, json
import time, datetime
import subprocess
from datetime import datetime
from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound
from nextcord.ext.commands import NSFWChannelRequired

intents = nc.Intents.default()
intents.message_content = True
intents.members = True

closeindic = 0
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

with open("src/config.json") as f:
    cdata = json.load(f)
token = cdata["token"]
prefix = cdata["prefix"]
rootids = [
    #your discord id here
]
supportedformats = [
    'py'
]

bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Bot started in {current_time}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        em = nc.Embed(
            title='Fatal error occured.',
            description='Code: `COMM-1`',
            color = nc.Colour.from_rgb(255, 82, 82)
        )
        await ctx.send(embed=em)
    elif isinstance(error, NSFWChannelRequired):
        em = nc.Embed(
            title='Fatal error occured.',
            description='Code: `COMM-2`',
            color = nc.Colour.from_rgb(255, 82, 82)
        )
        await ctx.send(embed=em)

@bot.command(aliases = ['help', 'info'])
async def information(ctx):
    em = nc.Embed(
        title='Infornation',
        description='**Command list**\n`errorcodes`, `execute`'+
        '\n\n**Supported file formats**\n`py`',
        color = nc.Color.from_rgb(71, 255, 123)
    )
    await ctx.send(embed=em)

@bot.command(aliases=['errcodes'])
async def errorcodes(ctx):
    em = nc.Embed(
        title='Error codes',
        description='**COMM class**\n1 - Command not found.\n2 - NSFW Mark Required.\n3 - Missing access'+
        '\n\n**FILE class**\n1 - No files attached to message\n2 - Console name not set\n3 - Unsupported file format',
        color = nc.Color.from_rgb(71, 255, 123)
    )
    await ctx.send(embed=em)

@bot.command(aliases=['exec', 'launch'])
async def execute(ctx, *, cmdname=None):
    if not ctx.message.attachments:
        em = nc.Embed(
            title='Fatal error occured.',
            description='Code: `FILE-1`',
            color = nc.Colour.from_rgb(255, 82, 82)
        )
        await ctx.send(embed=em)
    elif not cmdname:
        em = nc.Embed(
            title='Fatal error occured.',
            description='Code: `FILE-2`',
            color = nc.Colour.from_rgb(255, 82, 82)
        )
        await ctx.send(embed=em)
    else:
        for attach in ctx.message.attachments:
            await attach.save(f'src/execfiles/{attach.filename}')
            url = f'src/execfiles/{attach.filename}'
            file_extension = url.split('.')[-1]
            if not file_extension in supportedformats:
                em = nc.Embed(
                title='Fatal error occured.',
                    description='Code: `FILE-3`',
                    color = nc.Colour.from_rgb(255, 82, 82)
                )
                await ctx.send(embed=em)
                os.remove(f'qsrc/execfiles/{attach.filename}')
            elif file_extension == 'py':
                p = subprocess.Popen(["start", "cmd", "/k", f"title {cmdname} & cd path-to-bot-folder/src/execfiles/ & py {attach.filename}"], shell = True)
                p.wait()
                emb = nc.Embed(
                    title='File successfully executed',
                    description=f'Console name: {cmdname}\nFile name: {attach.filename}',
                    color = nc.Color.from_rgb(41, 242, 81)
                )
                await ctx.send(embed=emb)

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)
@bot.command(aliases = ['restart', 'rs', 'rb'])
async def reboot(ctx):
    if ctx.author.id in rootids:
        await ctx.send('Bot is restarting')
        restart_bot()
    else:
        em = nc.Embed(
            title='Fatal error occured.',
            description='Code: `COMM-3`',
            color = nc.Colour.from_rgb(255, 82, 82)
        )
        await ctx.send(embed=em)


bot.run(token)