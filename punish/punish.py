import discord
from discord.ext import commands
from .utils import checks
# import asyncio
# from __main__ import send_cmd_help
import logging
from cogs.utils.dataIO import dataIO
import os
import time
import re

UserInputError = commands.UserInputError

log = logging.getLogger('red.punish')

TIMESPEC_TRANSLATE = {'s': 1, 'm': 60, 'h': 60 * 60, 'd': 60 * 60 * 24}
DEFAULT_TIMEOUT = '30m'


def _parse_time(time):
    if any(u in time for u in TIMESPEC_TRANSLATE.keys()):
        delim = '([0-9.]*[{}])'.format(''.join(TIMESPEC_TRANSLATE.keys()))
        time = re.split(delim, time)
        time = sum([_timespec_sec(t) for t in time if t != ''])
    return int(time)


def _timespec_sec(t):
    timespec = t[-1]
    if timespec.lower() not in TIMESPEC_TRANSLATE:
        raise UserInputError('Unknown time unit "%c"' % timespec)
    timeint = float(t[:-1])
    return timeint * TIMESPEC_TRANSLATE[timespec]


class Punish:
    """Adds the ability to punish users."""

    # --- Format
    # {
    # serverid : {
    #   memberid : {
    #       until : timestamp
    #       by : memberid
    #       reason: str
    #       }
    #    }
    # }
    # ---

    def __init__(self, bot):
        self.bot = bot
        self.location = 'data/punish/settings.json'
        self.json = dataIO.load_json(self.location)
        self.handles = {}
        self.role_name = 'Punished'
        bot.loop.create_task(self.on_load())

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def punish(self, ctx, user: discord.Member, duration: str=None, *, reason: str=None):
        """Puts a user into timeout for a specified time period, with an optional reason.
        Time specification is any combination of number with the units s,m,h,d.
        Example: !punish @idiot 1.1h10m Enough bitching already!"""

        server = ctx.message.server

        # --- CREATING ROLE ---
        server = user.server
        role = discord.utils.get(user.server.roles, name=self.role_name)
        if not role:
            if not (any(r.permissions.manage_roles for r in server.me.roles) and
                    any(r.permissions.manage_channels for r in server.me.roles)):
                await self.bot.say("The Manage Roles and Manage Channels permissions are required to use this command.")
                return
            else:
                msg = "The %s role doesn't exist; Creating it now... " % self.role_name
                msgobj = await self.bot.reply(msg)
                log.debug('Creating punish role')
                perms = discord.Permissions.none()
                role = await self.bot.create_role(server, name=self.role_name, permissions=perms)
                await self.bot.edit_message(msgobj, msgobj.content + 'configuring channels... ')
                for c in server.channels:
                    await self.on_channel_create(c, role)
                await self.bot.edit_message(msgobj, msgobj.content + 'done.')

        self.json = dataIO.load_json(self.location)
        if server.id not in self.json:
            self.json[server.id] = {}

        if user.id in self.json[server.id]:
            msg = 'User was already punished; resetting their timer...'
        elif role in user.roles:
            msg = 'User was punished but had no timer, adding it now...'
        else:
            msg = 'Done.'

        if not duration:
            duration = DEFAULT_TIMEOUT
            msg += ' Using default duration of ' + duration
        duration = _parse_time(duration)
        timestamp = time.time() + duration

        if server.id not in self.json:
            self.json[server.id] = {}

        self.json[server.id][user.id] = {'until': timestamp}
        self.json[server.id][user.id]['by'] = ctx.message.author.id
        if reason:
            self.json[server.id][user.id]['reason'] = reason

        await self.bot.add_roles(user, role)
        dataIO.save_json(self.location, self.json)

        # schedule callback for role removal
        self.schedule_unpunish(duration, user, reason)

        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def unpunish(self, ctx, user: discord.Member):
        """Removes punishment from a user"""
        await self._unpunish(user)

    async def on_load(self):
        """Called when bot is ready and each time cog is (re)loaded"""
        await self.bot.wait_until_ready()
        for server, members in self.json.items():
            server = discord.utils.get(self.bot.servers, id=server)
            role = discord.utils.get(server.roles, name=self.role_name)
            for member, data in members.items():
                duration = data['until'] - time.time()
                member = discord.utils.get(server.members, id=member)
                if duration < 0:
                    await self.bot.remove_roles(member, role)
                    self._unpunish_data(member)
                else:
                    await self.bot.add_roles(member, role)
                    self.schedule_unpunish(duration, member)

    # Functions related to unpunishing

    def schedule_unpunish(self, delay, member, reason=None):
        """Schedules role removal, canceling and removing existing tasks if present"""
        handle = self.bot.loop.call_later(delay, self._unpunish_cb, member, reason)
        sid = member.server.id
        if sid not in self.handles:
            self.handles[sid] = {}
        if member.id in self.handles[sid]:
            self.handles[sid][member.id].cancel()
        self.handles[sid][member.id] = handle

    def _unpunish_cb(self, member, reason):
        """Regular function to be used as unpunish callback"""
        def wrap(member, reason):
            return self._unpunish(member, reason)
        self.bot.loop.create_task(wrap(member, reason))

    async def _unpunish(self, member, reason):
        """Remove punish role, delete record and task handle"""
        role = discord.utils.get(member.server.roles, name=self.role_name)
        if role:
            await self.bot.remove_roles(member, role)
            msg = "Your punishiment in %s has ended." % member.server.name
            if reason:
                msg += "\nReason was: %s" % reason
            await self.bot.send_message(member, msg)
        self._unpunish_data(member)

    def _unpunish_data(self, member):
        """Removes punish data entry and cancels any present callback"""
        self.json = dataIO.load_json(self.location)
        sid = member.server.id
        if sid in self.json and member.id in self.json[sid]:
            del(self.json[member.server.id][member.id])
            dataIO.save_json(self.location, self.json)

        if sid in self.handles and member.id in self.handles[sid]:
            self.handles[sid][member.id].cancel()
            del(self.handles[member.server.id][member.id])

    # Listeners

    async def on_channel_create(self, c, role=None):
        """Run when new channels are created and set up role permissions"""
        perms = discord.PermissionOverwrite()
        if c.type == discord.ChannelType.text:
            perms.send_messages = False
            perms.send_tts_messages = False
        elif c.type == discord.ChannelType.voice:
            perms.speak = False
        if not role:
            role = discord.utils.get(c.server.roles, name=self.role_name)
        await self.bot.edit_channel_permissions(c, role, perms)

    async def on_member_update(self, before, after):
        """Remove scheduled unpunish when manually removed"""
        role = discord.utils.get(before.server.roles, name=self.role_name)
        if role and role in before.roles and role not in after.roles:
            self._unpunish_data(after)

    async def on_member_join(self, member):
        """Restore punishment if user leaves/rejoins"""
        sid = member.server.id
        role = discord.utils.get(member.server.roles, name=self.role_name)
        if role:
            self.json = dataIO.load_json(self.location)
            if sid not in self.json:
                return
            duration = self.json[sid][member.id]['until'] - time.time()
            if duration > 0:
                await self.bot.add_roles(member, role)
                reason = 'punishment re-added on rejoin. '
                if 'reason' in self.json[sid][member.id]:
                    reason += self.json[sid][member.id]['reason']
                if member.id not in self.handles[sid]:
                    self.schedule_unpunish(duration, member, reason)


def check_folder():
    if not os.path.exists('data/punish'):
        log.debug('Creating folder: data/punish')
        os.makedirs('data/punish')


def check_file():
    f = 'data/punish/settings.json'
    if dataIO.is_valid_json(f) is False:
        log.debug('Creating json: settings.json')
        dataIO.save_json(f, {})


def setup(bot):
    check_folder()
    check_file()
    n = Punish(bot)
    bot.add_cog(n)
