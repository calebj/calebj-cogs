# Procedurally generated duel cog for Red-DiscordBot
# Copyright (c) 2016 Caleb Jonson
# Idea and rule system courtesy of Axas

import discord
from discord.ext import commands
from .utils.dataIO import dataIO
from __main__ import send_cmd_help
import random
import os
import logging
import asyncio

# Constants
MAX_ROUNDS = 4
INITIAL_HP = 20
TARGET_SELF = 'self'
TARGET_OTHER = 'target'
TARGET_OTHER_BLOCKABLE = 'blockable'
TARGET_OTHER_MISSABLE = 'missable'

DATA_PATH = "data/duels/"
JSON_PATH = DATA_PATH + "duelist.json"
LOG_PATH = DATA_PATH + "duelist.log"

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

WEAPONS = {'swing': {
                'axe': 3,
                'scimitar': 4,
                'buzzsaw': 5,
                'chainsaw': 6,
                'broadsword': 7,
                'katana': 4,
                'falchion': 5
                },
           'fire': {
               'raygun': 5
               },
           'hurl': {
               'spear': 6,
               'naginata': 5,
               'lance': 4
               }
           }


MELEE = {'stab': {
            'dagger': 5
            },
         'drive': {
            'fist': 4
            }
        }

MARTIAL = {'roundhouse kick': 6,
           'uppercut': 5,
           'bitch-slap': 2,
           'headbutt': 4}

BODYPARTS = ['head', 'throat', 'neck', 'solar plexus', 'ribcage', 'balls']

VERB_IND_SUB = {'munch': 'munches'}

ATTACK = {"{a} {v} their {o} at {d}!": indicatize(WEAPONS),
          "{a} {v} their {o} into {d}!": indicatize(MELEE),
          "{a} {v} their {o} into {d}'s {b}!": indicatize(MELEE),
          "{a} {v} {d}!": indicatize(MARTIAL),
          "{d} is bowled over by {a}'s sudden bull rush!": 6,
          "{a} tickles {d}, causing them to pass out from lack of breath": 2,
          "{a} points at something in the distance, distracting {d} long enough to {v} them!": MARTIAL
          }

CRITICAL = {"Quicker than the eye can follow, {a} delivers a devastating blow with their {o} to {d}'s {b}.": WEAPONS,
            "{a} nails {d} in the {b} with their {o}! Critical hit!": WEAPONS}

HEALS = {'inject': {
                'morphine': 4,
                'nanomachines': 5
             },
            'munch': {
                'on some': {
                    'cake': 5,
                    'cat food':3,
                    'dog food': 4
                    },
                'on a': {
                    'waffle': 4
                }
            },

            'drink': {
                'some': {
                    'Ambrosia':7
                },
                'a': {
                    'generic hp potion': 5
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
        return self.member.nick if self.member.nick else self.member.name

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


class Duels:
    def __init__(self, bot):
        self.bot = bot
        self.duelists = dataIO.load_json("data/duels/duelist.json")

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

    @commands.command(name="duels", pass_context=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def _duels(self, ctx, top : int=10):
        """Shows the duel leaderboard, defaults to top 10"""
        server = ctx.message.server
        if top < 1:
            top = 10
        if server.id in self.duelists:
            def sort_wins(kv):
                _,v = kv
                return v['wins'] - v['losses']

            duels_sorted = sorted(self.duelists[server.id].items(), key=sort_wins,
                                  reverse=True)
            if len(duels_sorted) < top:
                top = len(duels_sorted)
            topten = duels_sorted[:top]
            highscore = ""
            place = 1
            members = {uid: server.get_member(uid) for uid, _ in topten} # only look up once each
            names = {uid: m.nick if m.nick else m.name for uid, m in members.items()}
            max_name_len = max([len(n) for n in names.values()])

            # header
            highscore += '#'.ljust(len(str(top))+1) # pad to digits in longest number
            highscore += 'Name'.ljust(max_name_len + 4)
            for stat in ['wins', 'losses', 'draws']:
                highscore += stat.ljust(8)
            highscore += '\n'

            for uid, stats in topten:
                member = members[uid]
                highscore += str(place).ljust(len(str(top))+1) # pad to digits in longest number
                highscore += names[uid].ljust(max_name_len + 4)
                for stat in ['wins', 'losses', 'draws']:
                    val = stats[stat]
                    #highscore += '{}:'.format(stat).ljust(8)
                    highscore += '{}'.format(val).ljust(8)
                highscore += "\n"
                place += 1
            if highscore:
                if len(highscore) < 1985:
                    await self.bot.say("```py\n"+highscore+"```")
                else:
                    await self.bot.say("The leaderboard is too big to be displayed. Try with a lower <top> parameter.")
        else:
            await self.bot.say("There are no scores registered in this server. Start fighting!")

    @commands.command(name="duel", pass_context=True, no_pm=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def _duel(self, ctx, user: discord.Member=None):
        """Duel another player"""
        if not user:
            await self.bot.reply("please mention a user to duel with!")
        else:
            author = ctx.message.author
            p1 = Player(self, author)
            p2 = Player(self, user)
            if user == author:
                await self.bot.reply("you can't duel yourself, silly!")
                return

            order = [(p1, p2), (p2, p1)]
            random.shuffle(order)
            msg = "%s challenges %s to a duel!" % (p1, p2)
            msg += "\nBy a coin toss, %s will go first." % order[0][0]
            await self.bot.say(msg)
            for i in range(MAX_ROUNDS):
                if p1.hp <= 0 or p2.hp <= 0:
                    break
                for attacker, defender in order:
                    if p1.hp <= 0 or p2.hp <= 0:
                        break
                    if attacker.member == ctx.message.server.me:
                        msg = self.generate_action(attacker, defender, 'BOT')
                    else:
                        msg = self.generate_action(attacker, defender)
                    await self.bot.say(msg)
                    await asyncio.sleep(1)

            if p1.hp != p2.hp:
                victor = p1 if p1.hp > p2.hp else p2
                loser = p1 if p1.hp < p2.hp else p2
                victor.wins += 1
                loser.losses += 1
                msg = 'After %d rounds, %s wins with %d HP!' % (
                    i+1, victor.mention, victor.hp)
            else:
                for p in [p1, p2]:
                    p.draws += 1
                msg = 'After %d rounds, the duel ends in a tie!' % (i+1)

            # append stats
            msg += '\nStats: '
            for p, delim in [(victor, '; '), (loser, '.')]:
                msg += '%s has %d wins, %d losses, %d draws%s' % (p, p.wins, p.losses, p.draws, delim)
            await self.bot.say(msg)

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
        move = movelist.pop(0)  # always first
        verb = movelist.pop(0) if movelist else None  # Optional
        obj = movelist.pop() if movelist else None  # Optional
        if movelist:
            verb += ' ' + movelist.pop()  # Optional but present when obj is
        return move, obj, verb, hp_delta


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
    if not os.path.exists(DATA_PATH):
        print("Creating data/duels folder...")
        os.mkdir(DATA_PATH)
		

def check_files():
    if not dataIO.is_valid_json(JSON_PATH):
        print("Creating duelist.json...")
        dataIO.save_json(JSON_PATH, {})


def setup(bot):
    global logger
    check_folders()
    check_files()
    n = Duels(bot)
    logger = logging.getLogger("red.duels")
    if logger.level == 0: # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename=LOG_PATH, encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    bot.add_cog(n)
