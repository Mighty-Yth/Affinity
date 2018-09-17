import discord
from discord.ext import commands
import asyncio
from itertools import cycle


Token = 'NDIzNTk4MTUwODA5NTUwODUw.DZDISA.cIzWFeIPXcKxNmpnAujmQYtrnm8'

client = commands.Bot(command_prefix = 'a!')
client.remove_command('help')

extensions = ['music','mod','exp','CommandErrorHandler','test']
status = ['a!help', ' with a noose ', 'with used needles','with a loaded gun', 'with bofa']

@client.event 
async def on_ready():
    print('affinity is ready')


async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game =discord.Game(name= current_status))
        await asyncio.sleep(60)

@client.command(pass_context = True)
async def load(ctx,extension):
    if ctx.message.author.server_permissions.manage_server:
         try:
              client.load_extension(extension)
              print("loaded {}".format(extension))
         except Exception as error:
             print('{} cannot be loaded [{}]'.format(extension, error))
    else:
        print("you dont have the perms to manage the server")


@client.command(pass_context = True)
async def unload(ctx,extension):
    if ctx.message.author.server_permissions.manage_server:
         try:
              client.unload_extension(extension)
              print("unloaded {}".format(extension))
         except Exception as error:
             print('{} cannot be unloaded [{}]'.format(extension, error))
    else:
        print("you dont have the perms to manage the server")
        
         
@client.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.red()
        )
    embed.set_author(name = "help")
    embed.add_field(name = "a!ping", value ="the bot responds", inline = False)
    embed.add_field(name = "a!unload ", value ="unloads categories", inline = False)
    embed.add_field(name = "a!load", value = "loads categories", inline = False)
    embed.add_field(name = "a!leave", value = "makes the bot leave vc", inline = False)
    embed.add_field(name = "a!done", value = "gives you the given points for the days raid", inline = False)
    embed.add_field(name = "a!dailies", value = "gives you a dailiy 10 points every 24hrs", inline = False)
    embed.add_field(name = "a!check", value = "it allows you to check your balance", inline = False)

    await client.send_message(author, embed = embed)
    



if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded [{}]'.format(extension, error))
    




client.loop.create_task(change_status())
client.run(Token)

