import discord
import asyncio
import re
from discord.ext import commands
from .utils import checks

TIMESPEC_TRANSLATE = {'s': 1, 'm': 60, 'h': 60*60, 'd': 60*60*24}


class Mute:
    def __init__(self, bot):
        self.bot = bot
        self.role_name = "Mute"

    @commands.command(no_pm=True)
    @checks.admin_or_permissions(kick_members=True)
    async def mute(self, user: discord.Member, time, *, reason: str=None):
        """Mutes a user for a specified time period, with an optional reason.
        Time specification is any combination of number with the units s,m,h,d.
        Example: !mute @idiot 1.1h10m Enough bitching already!
        WARNING: if the bot is restarted, the user will have to be unmuted manually."""
        role = discord.utils.get(user.server.roles, name=self.role_name)
        if role:
            try:
                await self.bot.add_roles(user, role)
                time = _parse_time(time)
                await asyncio.sleep(time)
                await self.bot.remove_roles(user, role)
                msg = user.mention + " is no longer muted."
                if reason:
                    msg += " Reason for muting was: " + reason
                else:
                    msg += " Try to behave from now on."
                await self.bot.say(msg)
            except discord.errors.Forbidden:
                await self.bot.reply("I don't have permissions to modify roles.")
        else:
            await self.bot.reply("The {} role doesn't exist; I can't do anything.".format(self.role_name))


def _parse_time(time):
    if any(u in time for u in TIMESPEC_TRANSLATE.keys()):
        delim = '([0-9.]*[{}])'.format(''.join(TIMESPEC_TRANSLATE.keys()))
        time = re.split(delim, time)
        time = sum([_timespec_sec(t) for t in time if t != ''])
    return int(time)


def _timespec_sec(t):
    timespec = t[-1]
    if timespec.lower() not in TIMESPEC_TRANSLATE:
        raise ValueError('Unknown time unit "%c"' % timespec)
    timeint = float(t[:-1])
    return timeint * TIMESPEC_TRANSLATE[timespec]


def setup(bot):
    n = Mute(bot)
    bot.add_cog(n)
