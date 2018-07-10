import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils.chat_formatting import box, error, warning

import logging
import os
import re
import asyncio
import time
from datetime import datetime, timezone, timedelta
from random import randint
from math import ceil
from collections import defaultdict

__version__ = '2.0.2'

log = logging.getLogger("red.scheduler")
log.setLevel(logging.INFO)

PATH = 'data/scheduler/'
JSON = PATH + 'events.json'

UNIT_TABLE = (
    (('weeks', 'wks', 'w'), 60 * 60 * 24 * 7),
    (('days', 'dys', 'd'), 60 * 60 * 24),
    (('hours', 'hrs', 'h'), 60 * 60),
    (('minutes', 'mins', 'm'), 60),
    (('seconds', 'secs', 's'), 1),
)


class Event:
    __slots__ = ['name', 'channel', 'server', 'author', 'command',
                 'timedelta', 'repeat', 'starttime']

    def __init__(self, **data):
        self.name = data['name']
        self.channel = data['channel']
        self.server = data['server']
        self.author = data['author']
        self.command = data['command']
        self.timedelta = data['timedelta']
        self.repeat = data['repeat']
        self.starttime = data.get('starttime')

    @staticmethod
    def _key(obj):
        return (obj.timedelta, obj.name, obj.starttime, obj.channel)

    def __hash__(self):
        return hash(self._key(self))

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        for k in self.__slots__:
            if getattr(self, k) != getattr(other, k):
                return False
        return True


class BadTimeExpr(ValueError):
    pass


def _find_unit(unit):
    for names, length in UNIT_TABLE:
        if any(n.startswith(unit) for n in names):
            return names, length
    raise BadTimeExpr("Invalid unit: %s" % unit)


def _parse_time(time):
    time = time.lower()
    if not time.isdigit():
        time = re.split(r'\s*([\d.]+\s*[^\d\s,;]*)(?:[,;\s]|and)*', time)
        time = sum(map(_timespec_sec, filter(None, time)))
    return int(time)


def _timespec_sec(expr):
    atoms = re.split(r'([\d.]+)\s*([^\d\s]*)', expr)
    atoms = list(filter(None, atoms))

    if len(atoms) > 2:  # This shouldn't ever happen
        raise BadTimeExpr("invalid expression: '%s'" % expr)
    elif len(atoms) == 2:
        names, length = _find_unit(atoms[1])
        if atoms[0].count('.') > 1 or \
                not atoms[0].replace('.', '').isdigit():
            raise BadTimeExpr("Not a number: '%s'" % atoms[0])
    else:
        names, length = _find_unit('seconds')

    try:
        return float(atoms[0]) * length
    except ValueError:
        raise BadTimeExpr("invalid value: '%s'" % atoms[0])


def _generate_timespec(sec, short=False, micro=False):
    timespec = []

    for names, length in UNIT_TABLE:
        n, sec = divmod(sec, length)

        if n:
            if micro:
                s = '%d%s' % (n, names[2])
            elif short:
                s = '%d%s' % (n, names[1])
            else:
                s = '%d %s' % (n, names[0])
            if n <= 1:
                s = s.rstrip('s')
            timespec.append(s)

    if len(timespec) > 1:
        if micro:
            return ''.join(timespec)

        segments = timespec[:-1], timespec[-1:]
        return ' and '.join(', '.join(x) for x in segments)

    return timespec[0]


def _convert_iso8601(input_string):
    tsre = r"[:]|([-](?!((\d{2}[:]\d{2})|(\d{4}))$))"
    ts = re.sub(tsre, '', input_string)

    if ts.endswith(('z', 'Z')):
        ts = ts[:-1] + '+0000'

    if '.' in ts:
        fmt = "%Y%m%dT%H%M%S.%f%z"
    else:
        fmt = "%Y%m%dT%H%M%S%z"

    return datetime.strptime(ts, fmt)


class Scheduler:
    """Schedules commands to run every so often.

    Times are formed as follows: 1s, 2m, 3h, 5d, 1w
    """

    def __init__(self, bot):
        self.bot = bot
        self.events = dataIO.load_json(JSON)
        self.queue = asyncio.PriorityQueue(loop=self.bot.loop)
        self.queue_lock = asyncio.Lock()
        self.pending = {}
        self.pending_by_event = defaultdict(lambda: list())
        self._load_events()
        self.task = bot.loop.create_task(self.queue_manager())

    def __unload(self):
        self.task.cancel()

    def save_events(self):
        dataIO.save_json(JSON, self.events)

    def _load_events(self):
        # for entry in the self.events make an Event
        for server in self.events:
            for name, event in self.events[server].items():
                e = Event(server=server, **event)
                self.bot.loop.create_task(self._put_event(e))

    async def _put_event(self, event, fut=None, offset=None):
        if fut is None:
            now = int(time.time())

            if event.repeat:
                diff = max(now - event.starttime, 0)
                fut = ((ceil(diff / event.timedelta) * event.timedelta) +
                       event.starttime)
            else:
                fut = now + event.timedelta

        if offset:
            fut += offset

        await self.queue.put((fut, event))

        log.debug('Added "{}" to the scheduler queue at {}'.format(event.name,
                                                                   fut))

    async def _add_event(self, name, command, dest_server, dest_channel,
                         author, timedelta, repeat=False, start=None):
        if isinstance(dest_server, discord.Server):
            dest_server = dest_server.id

        if isinstance(dest_channel, discord.Channel):
            dest_channel = dest_channel.id

        if isinstance(author, discord.User):
            author = author.id

        if dest_server not in self.events:
            self.events[dest_server] = {}

        if isinstance(start, datetime):
            start = start.timestamp()

        event_dict = {
            'name'      : name,
            'channel'   : dest_channel,
            'author'    : author,
            'command'   : command,
            'timedelta' : timedelta,
            'repeat'    : repeat,
            'starttime' : start or int(time.time())
        }

        log.debug('event dict:\n\t{}'.format(event_dict))

        self.events[dest_server][name] = event_dict
        e = Event(server=dest_server, **event_dict)
        await self._put_event(e)

        self.save_events()

    async def _remove_event(self, name, server):
        events = []
        removed = None

        async with self.queue_lock:

            while not self.queue.empty():
                time, event = self.queue.get_nowait()
                if name == event.name and server.id == event.server:
                    removed = (time, event)
                    break
                else:
                    events.append((time, event))

            for event in events:
                self.queue.put_nowait(event)

        if not removed:
            return None

        time, event = removed
        if self.pending_by_event[event]:
            for ts in self.pending_by_event[event]:
                k = (ts, event)
                self.pending[k].cancel()
                del self.pending[k]
            del self.pending_by_event[event]

        return removed

    @commands.group(no_pm=True, pass_context=True)
    async def scheduler(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            return

    @scheduler.command(pass_context=True, name="add")
    async def _scheduler_add(self, ctx, time_interval, *, command):
        """Add a command to run in [time_interval].

        Intervals are any combination of units: 1s, 2m, 3h, 5d, 1w.
        """
        name = ctx.message.author.id + '-' + command.lower()
        await self._add_centralized(ctx, name, time_interval, command, False)

    @scheduler.command(pass_context=True, name="add_timelast")
    async def _scheduler_add_timelast(self, ctx, command, *, time_interval):
        """Add a command to run in [time_interval].

        Intervals are any combination of units: 1s, 2m, 3h, 5d, 1w.
        """
        name = ctx.message.author.id + '-' + command.lower()
        await self._add_centralized(ctx, name, time_interval, command, False)

    @scheduler.command(pass_context=True, name="add_twostage")
    async def _scheduler_add_twostage(self, ctx, command1, time_interval, *, command2):
        """Add a command to run now, and another in [time_interval].

        Intervals are any combination of units: 1s, 2m, 3h, 5d, 1w.
        """
        name1 = ctx.message.author.id + '-' + command1.lower()
        name2 = ctx.message.author.id + '-' + command2.lower()
        self.dispatch_fake(ctx.message.channel, ctx.message.author.id, name1,
                           command1)
        await self._add_centralized(ctx, name2, time_interval, command2, False)

    @scheduler.command(pass_context=True, name="add_twostage_timelast")
    async def _scheduler_add_twostage_timelast(self, ctx, command1, command2, *, time_interval):
        """Add a command to run now, and another in [time_interval].

        Intervals are any combination of units: 1s, 2m, 3h, 5d, 1w.
        """
        name1 = ctx.message.author.id + '-' + command1.lower()
        name2 = ctx.message.author.id + '-' + command2.lower()
        self.dispatch_fake(ctx.message.channel, ctx.message.author.id, name1,
                           command1)
        await self._add_centralized(ctx, name2, time_interval, command2, False)

    @scheduler.command(pass_context=True, name="repeat")
    @checks.mod_or_permissions(manage_messages=True)
    async def _scheduler_repeat(self, ctx, name, time_interval, *, command):
        """Add a command to run every [time_interval].

        Intervals are any combination of units: 1s, 2m, 3h, 5d, 1w.
        """
        await self._add_centralized(ctx, name, time_interval, command, True)

    @scheduler.command(pass_context=True, name="repeat_from")
    @checks.mod_or_permissions(manage_messages=True)
    async def _scheduler_repeat_from(self, ctx, name, start, interval, *, command):
        """Add a command to run every [interval] starting at [start].

        Start time must be an ISO8601 timestamp, unix timestamp or 'now'.

        An ISO8601 timestamp looks like this: 2017-12-11T01:15:03.449371-0500.

        The interval is any combination of units: 1s, 2m, 3h, 5d, 1w.
        """
        await self._add_centralized(ctx, name, interval, command, True, start)

    @scheduler.command(pass_context=True, name="repeat_in")
    @checks.mod_or_permissions(manage_messages=True)
    async def _scheduler_repeat_in(self, ctx, name, start_in, interval, *, command):
        """Add a command to run every [interval] starting in [start_in].

        Both intervals are any combination of units: 1s, 2m, 3h, 5d, 1w.
        """
        await self._add_centralized(ctx, name, interval, command, True,
                                    start_in=start_in)

    async def _add_centralized(self, ctx, name, interval, command,
                               repeat, start=None, start_in=None):
        channel = ctx.message.channel
        server = ctx.message.server
        author = ctx.message.author
        name = name.lower()
        now = datetime.now(tz=timezone.utc)

        min_time = 30 if repeat else 5

        prefix = await self.get_prefix(ctx.message)
        command = command.lstrip(prefix)

        try:
            interval = _parse_time(interval)
        except BadTimeExpr as e:
            await self.bot.say(error(e.args[0]))
            return

        if start_in:
            try:
                start_in = _parse_time(start_in)
            except BadTimeExpr as e:
                await self.bot.say(error(e.args[0]))
                return
            start = now + timedelta(seconds=start_in)
        elif start:
            try:
                start = self._get_start(start, now)
            except ValueError:
                await self.bot.say(error('Invalid timestamp format!'))
                return
        else:
            start = now

        if interval < min_time:
            await self.bot.say("I'm sorry, {}, I can't let you do that. "
                               "Your time interval is waaaay too short and "
                               "I'll likely get rate limited. Try going above"
                               " {} seconds.".format(author.name, min_time))
            return
        elif name in self.events.get(server.id, {}):
            if repeat:
                msg = warning("An event with that name already exists!")
            else:
                msg = warning("That command is already scheduled to run!")
            await self.bot.say(msg)
            return

        if repeat:
            logmsg = 'add {} "{}" to {} on {} every {}s starting {}'
            msg = '"{}" will run `{}` every {}, starting at {} ({}).'
        else:
            logmsg = 'add {} "{}" to {} on {} in {}s'
            msg = 'I will run `{1}` in {2}.'

        log.info(logmsg.format(name, command, channel.name,
                               server.name, interval, start.timestamp()))

        await self._add_event(name, command, server, channel, author,
                              interval, repeat, start)

        timeexpr = _generate_timespec(interval)

        delta = self._format_start(start, now)

        msg = msg.format(name, command, timeexpr, start, delta)
        await self.bot.say(msg)

    @scheduler.command(pass_context=True, name="remove")
    async def _scheduler_remove(self, ctx, *, name):
        """Removes a scheduled repeating command by name."""
        server = ctx.message.server
        name = name.lower()

        if not self.events.get(server.id):
            await self.bot.say('No events are scheduled for this server.')
            return

        del self.events[server.id][name]
        await self._remove_event(name, server)
        self.save_events()
        await self.bot.say('"{}" has successfully been removed.'.format(name))

    @scheduler.command(pass_context=True, name="cancel")
    async def _scheduler_cancel(self, ctx, *, command):
        """Cancels a scheduled oneshot (non-repeating) command."""
        server = ctx.message.server
        fname = ctx.message.author.id + '-' + command.lower()

        event = self.events.get(server.id, {}).pop(fname, None)
        cancelled = await self._remove_event(fname, server)

        if event:
            self.save_events()

        if event or cancelled:
            await self.bot.say('"{}" has been successfully cancelled.'.format(command))
        else:
            await self.bot.say('Cannot find a scheduled run of "{}".'.format(command))

    @scheduler.command(pass_context=True, name="list")
    @checks.mod_or_permissions(manage_messages=True)
    async def _scheduler_list(self, ctx):
        """Lists all repeated commands
        """
        server = ctx.message.server

        if not self.events.get(server.id):
            await self.bot.say('No events scheduled for this server.')
            return

        mess = "Names:\n\t"
        mess += "\n\t".join(sorted(self.events[server.id].keys()))
        await self.bot.say(box(mess))

    def dispatch_fake(self, channel, author_id, name, command):
        prefix = self.bot.settings.get_prefixes(channel.server)[0]

        data = {}
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.gmtime())
        data['timestamp'] = timestamp
        data['id'] = randint(10**(17), (10**18) - 1)
        data['content'] = prefix + command
        data['channel'] = channel
        data['author'] = {'id': author_id}
        data['nonce'] = randint(-2**32, (2**32) - 1)
        data['channel_id'] = channel.id
        data['reactions'] = []
        fake_message = discord.Message(**data)
        log.info("Running '{}' in {}".format(name, channel.server))
        self.bot.dispatch('message', fake_message)

    def run_coro(self, event, schedtime):
        channel = self.bot.get_channel(event.channel)

        if channel is None:
            log.debug("Channel no longer found, not running scheduled event.")
        else:
            self.dispatch_fake(channel, event.author, event.name, event.command)

        t = (schedtime, event)
        if t in self.pending:
            del self.pending[t]
        self.pending_by_event[event].remove(schedtime)

    async def process_queue_event(self):
        if self.queue.empty():
            return False

        now = int(time.time())
        next_time, next_event = await self.queue.get()

        diff = max(next_time - now, 0)

        if diff < 30:
            log.debug('scheduling call of "{}" in {}s'.format(
                next_event.name, diff))

            fut = self.bot.loop.call_later(diff, self.run_coro,
                                           next_event, next_time)
            self.pending[(next_time, next_event)] = fut
            self.pending_by_event[next_event].append(next_time)

            if next_event.repeat:
                await self._put_event(next_event, next_time,
                                      next_event.timedelta)
            else:
                del self.events[next_event.server][next_event.name]
                self.save_events()
            return True
        else:
            log.debug('Will run {} "{}" in {}s'.format(
                next_event.name, next_event.command, diff))
            await self._put_event(next_event, next_time)
            return False

    async def get_prefix(self, msg, content=None):
        prefixes = self.bot.command_prefix
        if callable(prefixes):
            prefixes = prefixes(self.bot, msg)
            if asyncio.iscoroutine(prefixes):
                prefixes = await prefixes

        content = content or msg.content

        for p in prefixes:
            if content.startswith(p):
                return p
        return None

    async def queue_manager(self):
        try:
            await self.bot.wait_until_ready()

            while self == self.bot.get_cog('Scheduler'):
                while True:
                    async with self.queue_lock:
                        if not await self.process_queue_event():
                            break

                await asyncio.sleep(5)

        except asyncio.CancelledError:
            pass
        finally:
            log.debug('manager dying')

            while not self.queue.empty():
                await self.queue.get()

            for fut in self.pending.values():
                fut.cancel()

    def _get_start(self, start, now):
        if start.lower() == 'now' or start is None:
            return now
        elif start.count('.') == 1 and start.replace('.', '').isdigit():
            ts = datetime.utcfromtimestamp(float(start))
            return ts.replace(tzinfo=timezone.utc)
        elif start:
            return _convert_iso8601(start)

    def _format_start(self, start, now):
        if start == now:
            return 'now'
        else:
            diff_seconds = (now - start).total_seconds()
            delta = _generate_timespec(abs(diff_seconds))
            if diff_seconds < 0:
                return 'in ' + delta
            else:
                return delta + ' ago'


def check_folder():
    if not os.path.exists('data/scheduler'):
        os.mkdir('data/scheduler')


def check_files():
    if not dataIO.is_valid_json(JSON):
        print('Creating empty %s' % JSON)
        dataIO.save_json(JSON, {})


def setup(bot):
    check_folder()
    check_files()
    bot.add_cog(Scheduler(bot))
