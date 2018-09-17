import discord
from discord.ext import commands

class Mod:
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context = True)
    async def join(self,ctx):
        channel = ctx.message.author.voice.voice_channel
        try:
            await self.client.join_voice_channel(channel)
        except discord.ClientException:
            await self.client.say("im in voice chat leave me alone")
        else:
            await self.client.say("im ready to speak in "+ channel.name)

    @commands.command(pass_context = True)
    async def leave(self,ctx):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server)
        await voice_client.disconnect()
        self.client.say("alright later homos")
    @commands.command()
    async def ping(self):
        await self.client.say("hello")


    

def setup(client):
    client.add_cog(Mod(client))
        
