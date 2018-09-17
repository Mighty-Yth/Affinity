import discord
import os
import uhr
import math
import traceback
import sys
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio

ans = 0

accounts ={}


class Exp:
    def __init__(self,client):
        self.client = client
        
    def create_dictionary(self):
        infile =  open('explist.txt', 'r', encoding= 'UTF-8')
        for line in infile:
            [UserId,name,EXP] = line.strip().split(':')
            acct = uhr.Uhr(UserId,name,float(EXP))
            accounts[UserId] = acct
        infile.close()

    def update_data(self):
        key_list = list(accounts.keys())
        outfile = open('explist.txt', 'w', encoding= 'UTF-8')
        for key in key_list:
            outfile.write(str(accounts[key])+"\n")
        outfile.close()

    async def checking_memberID(self, ctx):
        result = ctx.message.author.id
        if result not in accounts:
            accounts[result]["EXP"] = 0

            await self.client.say("ping Mighty to check on the status of your portfolio")
        else:
            return result

    @commands.command(pass_context=True)
    async def points(self, ctx, args1): # this sets up the points for the final a!done command 
        global ans
        author = ctx.message.author
        exp_role = "exp"
        if args1 !='':
            if discord.utils.get(author.roles, name=exp_role):
                ans = int(args1)*15
                await self.client.say(ans)
               
            else:
                embed = discord.Embed(
                title = '⚠WARNING⚠',
                description = 'You do not have the exp role',
                colour = discord.Colour.red()
                )
                await self.client.say(embed=embed)
        else:
            await self.client.say("provide a number of targets")
      
    async def add_exp(self,account,members):  # this function adds the exp to ta persons acc
        await asyncio.sleep(5)
        done_role ="done"
        role = discord.utils.get(members.server.roles, name = 'done')
        if discord.utils.get(members.roles, name = done_role):
            if ans == 0:
                self.client.say("there is no points to be added for today")
            else:
                accountid = accounts.get(account)
                accountid.deposit(ans)
                self.update_data()
                await self.client.say("thank you")
                await self.client.remove_roles(members,role)     
        else:
            await self.client.say("you havent finished yet cuck")
     
    @commands.command(pass_context=True) 
    async def pay(self,ctx,account, args2 ):  #this removes the exp from a person's  acc (pay to rank up system)
        author = ctx.message.author
        exp_role = "exp"
        if args2 != "":
            if discord.utils.get(author.roles,name = exp_role):
                args2.split("|")    #args2[0] is the id  args2[1] is the amount to remove
                if args2[0] not in accounts:
                     account = accounts.get(args2[0])
                     account.remove(args2[1])
                     self.update_data()
                    
                else:
                    await self.client.say("this user is not on the list ")
            else:
                await self.client.say("you can not remove exp")               
        else:
            await self.client.say("do this <userID | amount to remove> do not include the <>")
        
    
    @commands.command(pass_context= True)
    async def check(self,ctx):
        check_member = ctx.message.author.id
        check_members = ctx.message.author
        message = ctx.message.channel       
        self.create_dictionary()
        if check_member in accounts: 
            acc =  accounts.get(check_member)
            total = format(acc.EXP, '.2f')
            embed = discord.Embed(
            colour = discord.Colour.blue()
            )
            embed.set_author(name =  "this is " + check_members.name + "'s Total EXP points ")
            embed.set_thumbnail(url = check_members.avatar_url)
            embed.add_field(name = "Total EXP: ", value = total  , inline = False)
            await self.client.send_message(message, embed = embed)    
        else:
            await self.client.say("there is no nothing to show ")

    @commands.command(pass_context = True)
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def done(self,ctx):
        self.create_dictionary()
        member = ctx.message.author
        members = ctx.message.author.id       
        role = discord.utils.get(member.server.roles, name = 'done')
        await self.client.add_roles(member,role)
        if members in accounts:
            await self.add_exp(members,member)       
        else:
            await self.client.say("sorry youre not on the list please tell Mighty about it ")
    @commands.command(pass_context = True)
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def dailies(self,ctx):
        author_ID = ctx.message.author.id
        message = ctx.message
        self.create_dictionary()
        if author_ID in accounts: 
            acc = accounts.get(author_ID)
            acc.deposit(10)
            self.update_data()
            await self.client.add_reaction(message,":mightyssealofapproval:380491610263126018")    
        else:
            await self.client.say("sorry youre not on the list please tell Mighty about it ")      
    @commands.command()
    async def on_member_join(self,member):
        self.create_dictionary()       
        await self.update_data () 

    async def on_command_error(self,error,ctx):
        message = ctx.message.channel
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            return


        if isinstance(error, commands.CommandOnCooldown):
            await self.client.send_message(message, " i see what youre trying to do , please retry in {}s.".format(math.ceil(error.retry_after)))
            return
            
def setup(client):
    client.add_cog(Exp(client))