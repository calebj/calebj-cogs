import asyncio
import discord
from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks
import re

JSON = 'data/purgepins.json'
MAX_PINS = 50
UNIT_TABLE = {'s': 1, 'm': 60, 'h': 60 * 60}


def _parse_time(time):
    if any(u in time for u in UNIT_TABLE.keys()):
        delim = '([0-9.]*[{}])'.format(''.join(UNIT_TABLE.keys()))
        time = re.split(delim, time)
        time = sum([_timespec_sec(t) for t in time if t != ''])
    return int(time)


def _timespec_sec(t):
    timespec = t[-1]
    if timespec.lower() not in UNIT_TABLE:
        raise ValueError('Unknown time unit "%c"' % timespec)
    timeint = float(t[:-1])
    return timeint * UNIT_TABLE[timespec]


class PurgePins:
    def __init__(self, bot):
        self.bot = bot
        self.handles = {}

        self.settings = dataIO.load_json(JSON)
        if any(type(x) is not list for x in self.settings.values()):
            self.upgrade_settings(self.settings)
            dataIO.save_json(JSON, self.settings)

        self.task_handle = self.bot.loop.create_task(self.start_task())

    def __unload(self):
        self.task_handle.cancel()

    async def start_task(self):
        await self.bot.wait_until_ready()
        for cid in self.settings:
            channel = self.bot.get_channel(cid)
            print('channel_id ' + cid)
            if channel:
                await self.do_pin_rotate(channel)

    def upgrade_settings(self, settings):
        for k, v in settings.items():
            if type(v) is not dict:
                settings[k] = {'PURGE_DELAY': v}

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_messages=True)
    async def purgepins(self, ctx, wait: str = None):
        """Set delay for deletion of pin messages, or disable it.

        Accepted time units are s(econds), m(inutes), h(ours).
        Example: !purgepins 1h30m
        To disable purepins, run !purgepins off"""
        channel = ctx.message.channel
        if wait is not None:
            if wait.strip().lower() in ['none', 'off']:
                wait = False
            else:
                try:
                    wait = _parse_time(wait)
                except ValueError:
                    await self.bot.send_cmd_help(ctx)
                    return
            if channel.id not in self.settings:
                self.settings[channel.id] = {}
            self.settings[channel.id]['PURGE_DELAY'] = wait

            dataIO.save_json(JSON, self.settings)
        else:
            wait = self.settings.get(channel.id, {}).get('PURGE_DELAY', False)

        if wait is False:
            msg = ('Pin notifications in this channel will not be '
                   'automatically deleted.')
        else:
            msg = 'Pin notifications in this channel are set to be deleted '
            if wait > 0:
                msg += 'after %s seconds.' % wait
            else:
                msg += 'immediately.'

        if not channel.permissions_for(channel.server.me).manage_messages:
            msg += ("\n**Warning:** I don't have permissions to delete "
                    "messages in this channel!")

        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_messages=True)
    async def rotatepins(self, ctx, on_off: bool = None):
        "Sets whether the oldest pin is automatically removed at 50."
        channel = ctx.message.channel
        msg = 'Pin auto-rotation %s in this channel.'

        if on_off is None:
            on_off = self.settings.get(channel.id, {}).get('ROTATE_PINS')
            status = 'is currently '
        elif on_off == self.settings.get(channel.id, {}).get('ROTATE_PINS'):
            status = 'was already '
        else:
            if channel.id not in self.settings:
                self.settings[channel.id] = {}
            self.settings[channel.id]['ROTATE_PINS'] = on_off
            dataIO.save_json(JSON, self.settings)
            status = 'is now '
            await self.do_pin_rotate(channel)

        if not channel.permissions_for(channel.server.me).manage_messages:
            msg += ("\n**Warning:** I don't have permissions to manage "
                    "messages in this channel!")

        status += 'enabled' if on_off else 'disabled'
        await self.bot.say(msg % status)

    async def on_message(self, message):
        channel = message.channel

        if channel.is_private or channel.id not in self.settings:
            return
        if not channel.permissions_for(channel.server.me).manage_messages:
            return

        settings = self.settings[channel.id]
        if message.type is discord.MessageType.pins_add:
            timeout = settings.get('PURGE_DELAY', False)
            if timeout is not False:
                task = self.delete_task(message, timeout)
                self.handles[message.id] = self.bot.loop.create_task(task)

    async def on_message_delete(self, message):
        if message.id in self.handles:
            self.handles[message.id].cancel()
            del self.handles[message.id]

    async def on_message_edit(self, before, after):
        channel = after.channel
        if channel.is_private or channel.id not in self.settings:
            return
        if after.pinned and not before.pinned:
            await self.do_pin_rotate(channel)

    async def do_pin_rotate(self, channel):
        if not channel.permissions_for(channel.server.me).manage_messages:
            return
        settings = self.settings[channel.id]
        if settings.get('ROTATE_PINS', False):
            pins = await self.bot.pins_from(channel)
            if len(pins) >= MAX_PINS:
                await self.bot.unpin_message(pins[-1])

    async def delete_task(self, message, timeout):
        await asyncio.sleep(timeout)
        try:
            await self.bot.delete_message(message)
        except:
            pass

        if message.id in self.handles:
            self.handles.pop(message.id)


def check_files(bot):
    if not dataIO.is_valid_json(JSON):
        print("Creating default purgepins json...")
        dataIO.save_json(JSON, {})


def setup(bot):
    check_files(bot)
    n = PurgePins(bot)
    bot.add_cog(n)
