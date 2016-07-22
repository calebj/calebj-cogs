# Original cog by Mash, cleaned up and updated to new economy/dataIO by CalebJ

from .utils.dataIO import dataIO
from .utils import checks
from .economy import NoAccount
import discord
from discord.ext import commands
from __main__ import send_cmd_help
import json
import os

try:
    from PIL import Image, ImageDraw, ImageFont
    pil_available = True
except:
    pil_available = False

try:
    import emoji
    emoji_available = True
except:
    emoji_available = False


DIR_DATA = "data/bartender"
SETTINGS = DIR_DATA+"/settings.json"
BACKUP = DIR_DATA+"/bank_backup.json"
BANK = "data/economy/bank.json"

class Bartender:
    """Buy a drink at the bar with Red's economy currency"""
    def __init__(self,bot):
        self.bot = bot
        self.settings = dataIO.load_json(SETTINGS)
        self.items = [["beer", ":beer:", 2], ["wine", ":wine_glass:", 2], ["cocktail", ":cocktail:", 4], ["tropical", ":tropical_drink:", 5], ["sake", ":sake:", 4], ["champagne", ":champagne:", 30], ["tea", ":tea:", 1], ["coffee", ":coffee:", 1]]
        self.numbers = ["one", "two", "tree", "four", "five", "six", "seven", "eight", "nine", "ten"]

    @commands.group(name="bar", pass_context=True, no_pm=False)
    async def _bar(self, ctx):
        """Bar operations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_bar.command(pass_context=True)
    async def buy(self, ctx, amount : int, drink):
        """Buy a drink with currency from Red's economy"""
        botuser = ctx.message.server.me
        content = ctx.message.content
        mentions = ctx.message.mentions
        author = ctx.message.author

        #Get Economy data
        if self.econ_interlink() != None and self.settings["bar_startus"]:
            econ = self.econ_interlink()
        else:
            await self.bot.reply("Sorry mate, the bar is closed.")
            return

        price = -1
        icon = ""
        available = False
        for i, item in enumerate(self.items):
            #print(i)
            #print(item)
            if drink == self.items[i][0]:
                icon = self.items[i][1]
                price = self.items[i][2]*amount
                available = True
                break
        if not available:
            await self.bot.reply("I'm sorry to dissapoint you, we don't serve {}".format(drink))
            return

        buy_for = []
        for member in mentions:
            buy_for.append(member.mention)
        buy_for = " ".join(buy_for)


        try:
            if econ.bank.can_spend(author, price):
                econ.bank.transfer_credits(author, botuser, price)

                drinks = ""
                for d in range(0,amount):
                    drinks = drinks+icon
                if buy_for == "":
                    msg = "There you go mate {}".format(buy_for, drinks)
                    msg = emoji.emojize(msg, use_aliases=True)
                    await self.bot.say(msg)
                else:
                    if amount > 1:
                        msg = "{0} Have some {1}s from {2}{3}".format(buy_for, drink, author.mention, drinks)
                        msg = emoji.emojize(msg, use_aliases=True)
                        await self.bot.say(msg)
                    else:
                        msg ="{0} Have some {1} from {2}{3}".format(buy_for, drink, author.mention, drinks)
                        msg = emoji.emojize(msg, use_aliases=True)
                        await self.bot.say(msg)
            else:
                try:
                    text_num = self.numbers[amount-1]
                except Exception as e:
                    text_num = str(amount)
                await self.bot.reply("Sorry mate, you don't have enough money for {1} {2}.\n It costs {3}".format(text_num, drink, price))
        except NoAccount:
            await self.bot.reply('You need to open a bank account first.')

    @_bar.command(name='list', pass_context=True)
    async def _list(self, ctx):
        """Lists what we serve at the bar."""
        author = ctx.message.author
        msg = "**We have: **"
        for b in self.items:
            msg = msg + "{} ${}, ".format(b[0], b[2])
        await self.bot.reply(msg)

    #if Economy.py updates, this may break
    @_bar.command(pass_context=True)
    @checks.is_owner()
    async def register(self, ctx):
        """Opens the bar and registers the bot into Red's bank."""
        econ = self.bot.get_cog('Economy')
        bank = econ.bank
        botuser = ctx.message.server.me
        if not bank.account_exists(botuser):
            bank.create_account(botuser)
            await self.bot.say("Account opened for {}. Current balance: {}".format(botuser.mention, bank.get_balance(botuser)))
        else:
            await self.bot.say("{} already has an account at the Twentysix bank.".format(botuser.mention))
        self.settings["bar_startus"] = True
        dataIO.save_json(SETTINGS, self.settings)

    @_bar.command(name='open', pass_context=True)
    @checks.is_owner()
    async def _open(self, ctx):
        """Opens the bar"""
        author = ctx.message.author
        self.settings["bar_startus"] = True
        dataIO.save_json(SETTINGS, self.settings)
        await self.bot.reply("The bar is now open!.")

    @_bar.command(pass_context=True)
    @checks.is_owner()
    async def close(self, ctx):
        """Closes the bar"""
        author = ctx.message.author
        self.settings["bar_startus"] = False
        dataIO.save_json(SETTINGS, self.settings)
        await self.bot.reply("The bar is now closed!.")

    def econ_interlink(self):
        econ = None
        econ = self.bot.get_cog('Economy')
        if econ == None:
            print("--- Error: Was not able to load Economy cog into Bartender. ---")
            return False
        else:
            return econ

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Set-up
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def check_folders():
    if not os.path.exists(DIR_DATA):
        print("Creating data/bartender folder...")
        os.makedirs(DIR_DATA)

def check_files():
    settings = {"bar_status" : False}

    if not dataIO.is_valid_json(SETTINGS):
        print("Creating settings.json")
        dataIO.save_json(SETTINGS, settings)

def setup(bot):
    if not pil_available:
        raise RuntimeError("You don't have Pillow installed, run\n```pip3 install pillow```And try again")
        return
    if not emoji_available:
        raise RuntimeError("emoji is not installed. Do 'pip3 install emoji --upgrade' to use this cog.")
        return
    check_folders()
    check_files()
    bot.add_cog(Bartender(bot))
