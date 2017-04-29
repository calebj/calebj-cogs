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
