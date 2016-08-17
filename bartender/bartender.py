from discord.ext import commands

class Bartender:
    """Outdated, install bartender from Mash's repo instead."""
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def bar(self):
        """Outdated, install bartender from Mash's repo instead."""
        await self.bot.say("The Bartender cog has returned to Mash's repo.\n"
        "Run `cog repo add mash-cogs https://github.com/Canule/Mash-Cogs`\n"
        "and then `cog install mash-cogs bartender` to overwrite this one.")

def setup(bot):
    bot.add_cog(Bartender(bot))
