import nextcord as nc
import os, sys, json
import time, datetime
import subprocess
import shutil
from datetime import datetime
from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound
from nextcord.ext.commands import NSFWChannelRequired
from zipfile import ZipFile

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
    'py',
    'zip'
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
        title='ZipCut',
        description='**Command List**\n`information`, `aliases`, `errorcodes`, `zipexecute`, `execute`, `breakprocess`, `zipbreakprocess`'+
        '\n\n**Root Command list**\n`reboot`'+
        '\n\n**Supported File Formats**\n`.py`\n`.json`\n`.txt`\n`.zip`', 
        color = nc.Color.from_rgb(71, 255, 123)
    )
    await ctx.send(embed=em)

@bot.command(aliases=['commandaliases'])
async def aliases(ctx):
    em = nc.Embed(
        title='Commands\' Aliases',
        description='`information`/`info`/`help`\n`aliases`/`commandaliases`\n`errorcodes`/`errcodes`\n`zipexecute`/`zipexec`/`ziplaunch`\n'+
        '`execute`/`exec`/`launch`\n`zipbreakprocess`/`zipbreakexec`/`zipbreak`/`zipstop`\n`breakprocess`/`breakexec`/`break`/`stop`\n`reboot`/`restart`/`rb`/`rs`',
        color = nc.Color.from_rgb(71, 255, 123)
    )
    await ctx.send(embed=em)

@bot.command(aliases=['errcodes'])
async def errorcodes(ctx):
    em = nc.Embed(
        title='Error codes',
        description='**COMM class**\n1 - Command not found.\n2 - NSFW Mark Required.\n3 - Missing access'+
        '\n\n**FILE class**\n1 - No files attached to message\n2 - processName Variable not set\n3 - Unsupported file format',
        color = nc.Color.from_rgb(71, 255, 123)
    )
    await ctx.send(embed=em)

@bot.command(aliases=['exec', 'launch'])
async def execute(ctx):
    if not ctx.message.attachments:
        em = nc.Embed(
            title='Fatal error occured.',
            description='Code: `FILE-1`',
            color = nc.Colour.from_rgb(255, 82, 82)
        )
        await ctx.send(embed=em)
    else:
        for attach in ctx.message.attachments:
            await attach.save(f'src/execfiles/singlFiles/{attach.filename}')
            url = f'src/execfiles/singlFiles/{attach.filename}'
            file_extension = url.split('.')[-1]
            if not file_extension in supportedformats:
                em = nc.Embed(
                title='Fatal error occured.',
                    description='Code: `FILE-3`',
                    color = nc.Colour.from_rgb(255, 82, 82)
                )
                await ctx.send(embed=em)
                os.remove(f'src/execfiles/singlFiles/{attach.filename}')
            elif file_extension == 'py':
                p = subprocess.Popen(["start", "cmd", "/k", f"cd src/execfiles/singlFiles/ & py {attach.filename}"], shell = True)
                p.wait
                emb = nc.Embed(
                    title='Your file was successfully executed!',
                    description=f'processName Variable = {attach.filename}\nTo end proccess, type `,break {attach.filename}`',
                    color = nc.Color.from_rgb(41, 242, 81)
                )
                await ctx.send(embed=emb)

@bot.command(aliases=['breakexec', 'break', 'stop'])
async def breakprocess(ctx, processName=None):
    if not processName:
        em = nc.Embed(
            title='Fatal error occured.',
            description='Code: `FILE-2`',
            color = nc.Colour.from_rgb(255, 82, 82)
        )
        await ctx.send(embed=em)
    else:
        subprocess.call(f"taskkill /fi \"WINDOWTITLE eq py  {processName}\"", shell=True)
        os.remove(path=f'src/execfiles/singlFiles/{processName}')
        emb = nc.Embed(
            title='Process successfully ended.',
            description=f'Execution stopped and files were deleted.',
            color = nc.Color.from_rgb(41, 242, 81)
        )
        await ctx.send(embed=emb)

@bot.command(aliases=['zipexec', 'ziplaunch'])
async def zipexecute(ctx, *, beginFile):
    if not ctx.message.attachments:
        em = nc.Embed(
            title='Fatal error occured.',
            description='Code: `FILE-1`',
            color = nc.Colour.from_rgb(255, 82, 82)
        )
        await ctx.send(embed=em)
    else:
        for attach in ctx.message.attachments:
            await attach.save(f'src/execfiles/ziparch/{attach.filename}')
            url = f'src/execfiles/ziparch/{attach.filename}'
            file_extension = url.split('.')[-1]
            if not file_extension in supportedformats:
                em = nc.Embed(
                title='Fatal error occured.',
                    description='Code: `FILE-3`',
                    color = nc.Colour.from_rgb(255, 82, 82)
                )
                await ctx.send(embed=em)
                os.remove(f'src/execfiles/ziparch/{attach.filename}')
            elif file_extension == 'zip':
                with ZipFile(f'src/execfiles/ziparch/{attach.filename}', 'r') as zip:
                    NewfolderName = f'{attach.filename}'.replace(".zip", "")
                    parentDir = 'src/execfiles/ziparch/'
                    NewFolderpath = os.path.join(parentDir, NewfolderName)
                    os.mkdir(NewFolderpath)
                    zip.extractall(path=f'{NewFolderpath}')
                    zip.close()
                msg1 = await ctx.send('Extracting files...')
                os.remove(f'src/execfiles/ziparch/{attach.filename}')
                await msg1.edit('Deleting original .zip file...')
                p = subprocess.Popen(["start", "cmd", "/k", f"cd src/execfiles/ziparch/{NewfolderName}/ & py {beginFile}"], shell = True)
                p.wait
                emb = nc.Embed(
                    title='Your files were successfully executed!',
                    description=f'processName1 Variable = {beginFile}\nprocessName2 Variable = {NewfolderName}\nTo end proccess, type `,zipbreak "{beginFile}" "{NewfolderName}"`',
                    color = nc.Color.from_rgb(41, 242, 81)
                )
                await msg1.edit(content="", embed=emb)

@bot.command(aliases=['zipbreakexec', 'zipbreak', 'zipstop'])
async def zipbreakprocess(ctx, processName1, processName2):
    if not processName1:
        em = nc.Embed(
            title='Fatal error occured.',
            description='Code: `FILE-2`',
            color = nc.Colour.from_rgb(255, 82, 82)
        )
        await ctx.send(embed=em)
    elif not processName2:
        em = nc.Embed(
            title='Fatal error occured.',
            description='Code: `FILE-2`',
            color = nc.Colour.from_rgb(255, 82, 82)
        )
        await ctx.send(embed=em)
    else:
        msg1 = await ctx.send('Stopping execution...')
        subprocess.call(f'taskkill /fi \"WINDOWTITLE eq py  {processName1}\"', shell=True)
        await msg1.edit('Deleting directory with files...')
        shutil.rmtree(f'src/execfiles/ziparch/{processName2}')
        emb = nc.Embed(
            title='Process successfully ended.',
            description=f'Execution stopped and files were deleted.',
            color = nc.Color.from_rgb(41, 242, 81)
        )
        await msg1.edit(content="", embed=emb)

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)
@bot.command(aliases = ['restart', 'rs', 'rb'])
async def reboot(ctx):
    if ctx.author.id in rootids:
        await ctx.send('*Bot is restarting...*')
        restart_bot()
    else:
        em = nc.Embed(
            title='Fatal error occured.',
            description='Code: `COMM-3`',
            color = nc.Colour.from_rgb(255, 82, 82)
        )
        await ctx.send(embed=em)


bot.run(token)