import discord
import asyncio
import re
from discord.ext import commands
from .utils import checks
import logging
log = logging.getLogger('red.punish')

TIMESPEC_TRANSLATE = {'s': 1, 'm': 60, 'h': 60 * 60, 'd': 60 * 60 * 24}


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
        server = user.server
        role = discord.utils.get(user.server.roles, name=self.role_name)
        if not role:
            msg = "The %s role doesn't exist; Creating it now... " % self.role_name
            msgobj = await self.bot.reply(msg)
            log.debug('Creating mute role')
            try:
                perms = discord.Permissions.none()
                # toggle permissions you want, rest are false
                role = await self.bot.create_role(server, name=self.role_name, permissions=perms)
                try:
                    for c in server.channels:
                        await self.channel_setup(c, role)
                    await self.bot.edit_message(msgobj, msgobj.content + 'done.')
                except discord.Forbidden:
                    await self.bot.say("A error occured while making channel permissions.\nPlease check your channel permissions for the %s role!" % self.role_name)
            except discord.Forbidden:
                await self.bot.say("The Manage Roles permission is required to create the %s role." % self.role_name)
                return
        try:
            await self.bot.add_roles(user, role)
            time = _parse_time(time)
            await asyncio.sleep(time)
            await self.bot.remove_roles(user, role)
            msg = user.mention + " is no longer muted."
            if reason:
                msg += " Reason for mute was: " + reason
            else:
                msg += " Try to behave from now on."
            await self.bot.say(msg)
        except discord.Forbidden:
            await self.bot.reply("I don't have permission to modify roles.")

    async def new_channel(self, c):
        r = discord.utils.get(c.server.roles, name=self.role_name)
        if r:
            await self.channel_setup(c, r)
            log.debug('Timeout role created on channel: {}'.format(c.id))
    
    async def channel_setup(self, c, role):
        perms = discord.PermissionOverwrite()
        if c.type == discord.ChannelType.text:
            perms.send_messages = False
            perms.send_tts_messages = False
        elif c.type == discord.ChannelType.voice:
            perms.speak = False
        await self.bot.edit_channel_permissions(c, role, perms)


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
    bot.add_listener(n.new_channel, 'on_channel_create')
    bot.add_cog(n)
