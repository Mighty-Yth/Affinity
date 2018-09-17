import discord
from discord.ext import commands
class Uhr:
    def __init__(self, identity,user,EXP):
        self.identity = identity
        self.user= user
        self.EXP = EXP
        

    def __str__(self):
        return self.identity + ':' + self.user+':'  + str(self.EXP)

    def deposit(self,amount):
        if amount >= 0:
            self.EXP += amount
    
    def remove(self,amount):
        if amount >= 0 and amount<= self.EXP:
            self.EXP -= amount