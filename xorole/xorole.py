import discord
from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import box, pagify, warning
import asyncio
from collections import defaultdict

"""XORoles (exclusive-or roles) cog by GrumpiestVulcan
Commissioned 2017-07-27 by QuietRepentance (Quiet#8251) for discord.gg/pokken"""

__author__ = "Caleb Johnson <me@calebj.io> (calebj#0001)"
__copyright__ = "Copyright 2017, Holocor LLC"
__version__ = '1.2.0'

JSON = 'data/xorole.json'

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


class XORoleException(Exception):
    pass

class RolesetAlreadyExists(XORoleException):
    pass

class RolesetNotFound(XORoleException):
    pass

class NoRolesetsFound(XORoleException):
    pass

class RoleNotFound(XORoleException):
    pass

class PermissionsError(XORoleException):
    pass


class XORole:
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(JSON)
        self.analytics = CogAnalytics(self)

    def save(self):
        dataIO.save_json(JSON, self.settings)

    def get_settings(self, server):
        sid = server.id
        return self.settings.get(sid, {})

    def update_settings(self, server, settings):
        self.settings[server.id] = settings
        self.save()

    def add_roles(self, server, roleset, *roles):
        rsn, rsl = self.get_roleset(server, roleset)

        rslset = set(rsl)
        newset = set(r.id for r in roles)

        self.update_roleset(server, roleset, list(newset | rslset))

        return [r for r in roles if r.id not in rslset]

    def remove_roles(self, server, roleset, *roles):
        rsn, rsl = self.get_roleset(server, roleset)

        rslset = set(rsl)
        rmset = set(r.id for r in roles)

        self.update_roleset(server, roleset, list(rslset - rmset))

        return [r for r in roles if r.id in rslset]

    def get_rolesets(self, server):
        return self.get_settings(server).get('ROLESETS', {})

    def update_rolesets(self, server, rolesets):
        settings = self.get_settings(server)
        settings['ROLESETS'] = rolesets
        self.update_settings(server, settings)

    def get_roleset(self, server, name, notfound_ok=False):
        current = self.get_rolesets(server)
        if name in current:
            return name, current[name]

        searchname = name.lower().strip()
        for k, v in current.items():
            if k.lower().strip() == searchname:
                return k, v

        if not notfound_ok:
            raise RolesetNotFound("Roleset '%s' does not exist." % name)

    def add_roleset(self, server, name):
        if self.get_roleset(server, name, notfound_ok=True):
            raise RolesetAlreadyExists('A roleset with that name already exists.')

        current = self.get_rolesets(server)
        current[name] = []
        self.update_rolesets(server, current)

    def remove_roleset(self, server, name):
        name, roles = self.get_roleset(server, name)  # Raises RolesetNotFound

        current = self.get_rolesets(server)
        current.pop(name)
        self.update_rolesets(server, current)

    def update_roleset(self, server, name, role_ids):
        rolesets = self.get_rolesets(server)
        name, old_roles = self.get_roleset(server, name)  # Raises RolesetNotFound
        rolesets[name] = role_ids
        self.update_rolesets(server, rolesets)

    def roleset_of_role(self, role, notfound_ok=False):
        rid = role.id
        for rsn, rsl in self.get_rolesets(role.server).items():
            if rid in rsl:
                return rsn
        if not notfound_ok:
            raise NoRolesetsFound("The '%s' role doesn't belong to any "
                                  "rolesets" % role.name)

    def get_roleset_memberships(self, member, roleset):
        rsn, rsl = self.get_roleset(member.server, roleset)

        rslset = set(rsl)
        current_roles = []

        for role in member.roles:
            if role.id in rslset:
                current_roles.append(role)

        return current_roles

    @staticmethod
    def find_role(server, query, notfound_ok=False):
        stripped = query.strip().lower()

        for role in server.roles:
            if role.name.strip().lower() == stripped:  # Ignore case and spaces
                return role
            elif role.id == stripped:  # also work with role IDs
                return role

        if not notfound_ok:
            raise RoleNotFound("Could not find role '%s'." % query)

    @classmethod
    def find_roles(cls, server, *queries):
        found = []
        notfound = []

        for q in queries:
            role = cls.find_role(server, q, notfound_ok=True)
            if role:
                found.append(role)
            else:
                notfound.append(q)

        return found, notfound

    async def role_add_remove(self, member, to_add=(), to_remove=()):

        roles = set(member.roles)
        replace_with = (roles | set(to_add)) - set(to_remove)

        if roles != replace_with:
            try:
                await self.bot.replace_roles(member, *list(replace_with))
            except discord.errors.Forbidden:
                if not (member.server.me.server_permissions.manage_roles or
                        member.server.me.server_permissions.administrator):
                    err = "I don't have permission to manage roles."
                else:
                    err = ('a role I tried to assign or remove is too high '
                           'for me to do so.')
                raise PermissionsError('Error updating roles: ' + err)

    @commands.group(pass_context=True, invoke_without_command=True, no_pm=True)
    async def xorole(self, ctx, *, role: str = None):
        if ctx.invoked_subcommand is None:
            if role:
                await ctx.invoke(self.xorole_add, role=role)
            else:
                await self.bot.send_cmd_help(ctx)

    @xorole.command(name='list', pass_context=True)
    async def xorole_list(self, ctx, *, roleset: str = None):
        "Shows the available roles to in the server or a specific roleset."
        server = ctx.message.server
        try:
            if roleset:
                name, roles = self.get_roleset(server, roleset)
                rs_dict = {name: roles}
            else:
                rs_dict = self.get_rolesets(server)

            lines = ['=== Available roles: ===']

            for i, k in enumerate(sorted(rs_dict.keys())):
                roles = rs_dict[k]
                roles = (discord.utils.get(server.roles, id=r) for r in roles)
                roles = sorted(filter(None, roles))

                lines.append(k + ':')
                if roles:
                    lines.extend((' - %s' % rn) for rn in roles)
                else:
                    lines.append('- (there are no roles in this roleset)')

                if i + 1 < len(rs_dict):
                    lines.append('\n')

            if len(lines) == 1:
                await self.bot.say('No roles are available to assign.')
                return

            for page in pagify('\n'.join(lines)):
                await self.bot.say(box(page))

        except XORoleException as e:
            await self.bot.say(warning(*e.args))

    @xorole.command(name='add', pass_context=True)
    async def xorole_add(self, ctx, *, role: str):
        "Assigns a role to you, removing any others in the same roleset."
        server = ctx.message.server
        member = ctx.message.author

        try:
            role = self.find_role(server, role)
            roleset = self.roleset_of_role(role)
            existing = self.get_roleset_memberships(member, roleset)

            if role in member.roles and len(existing) == 1:
                await self.bot.say('You already have that role; nothing to do.')
                return

            to_add = [role]
            to_remove = [r for r in existing if r != role]

            await self.role_add_remove(member, to_add, to_remove)

            await self.bot.say("Role in roleset %s switched to %s."
                               % (roleset, role.name))

        except XORoleException as e:
            await self.bot.say(warning(*e.args))

    @xorole.command(name='remove', pass_context=True)
    async def xorole_remove(self, ctx, *, role_or_roleset: str):
        "Removes a specific role or any in a roleset from you."
        server = ctx.message.server
        member = ctx.message.author

        try:
            role = self.find_role(server, role_or_roleset, notfound_ok=True)
            if role:
                if role not in member.roles:
                    await self.bot.say("You don't have that role; nothing to do.")
                    return

                to_remove = [role]

            else:
                to_remove = self.get_roleset_memberships(member, role_or_roleset)

            if to_remove:
                await self.role_add_remove(member, to_remove=to_remove)
                plural = 'roles' if len(to_remove) > 1 else 'role'
                rlist = ', '.join(r.name for r in to_remove)
                await self.bot.say('Removed the %s: %s.' % (plural, rlist))
            else:
                await self.bot.say("You don't belong to any roles in the %s "
                                   "roleset." % role_or_roleset)

        except XORoleException as e:
            await self.bot.say(warning(*e.args))

    @xorole.command(name='toggle', pass_context=True)
    async def xorole_toggle(self, ctx, *, role_or_roleset: str):
        "Toggles a role in a single-role roleset on or off, or between two roles in a roleset."
        server = ctx.message.server
        member = ctx.message.author
        try:
            role = self.find_role(server, role_or_roleset, notfound_ok=True)
            if role:
                role_or_roleset = self.roleset_of_role(role)

            roleset, rsl = self.get_roleset(server, role_or_roleset)
            roles = (discord.utils.get(server.roles, id=r) for r in rsl)
            roles = list(filter(None, roles))

            if not 0 < len(roles) <= 2:
                await self.bot.say(warning("Cannot toggle within the '%s' "
                                           "roleset." % roleset))
                return

            if len(roles) == 1:
                single_role = roles[0]
                if single_role in member.roles:
                    to_add = []
                    to_remove = [single_role]
                else:
                    to_add = [single_role]
                    to_remove = []

            elif len(roles) == 2:
                to_remove = self.get_roleset_memberships(member, roleset)
                if len(to_remove) != 1:
                    await self.bot.say(warning("You must have one role in %s "
                                               "to toggle it." % roleset))
                    return

                to_add = roles.copy()
                to_add.remove(to_remove[0])

            await self.role_add_remove(member, to_add, to_remove)
            if to_add and to_remove:
                await self.bot.say('Toggled from %s to %s.'
                                   % (to_remove[0], to_add[0]))
            elif to_add:
                await self.bot.say("Role '%s' added." % to_add[0])
            elif to_remove:
                await self.bot.say("Role '%s' removed." % to_remove[0])

        except XORoleException as e:
            await self.bot.say(warning(*e.args))

    @commands.group(pass_context=True, no_pm=True)
    async def xoroleset(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @checks.mod_or_permissions(administrator=True)
    @xoroleset.command(name='addroleset', pass_context=True)
    async def xoroleset_addroleset(self, ctx, *, name: str):
        "Adds a roleset."
        server = ctx.message.server
        try:
            if len(name.split()) > 1:
                await self.bot.say('For usability reasons, whitespace is not '
                                   'permitted in roleset names. Try again.')
                return

            self.add_roleset(server, name)
            await self.bot.say("Roleset '%s' created." % name)
        except XORoleException as e:
            await self.bot.say(warning(*e.args))

    @checks.mod_or_permissions(administrator=True)
    @xoroleset.command(name='rmroleset', pass_context=True)
    async def xoroleset_rmroleset(self, ctx, *, name: str):
        "Removes a roleset."
        server = ctx.message.server
        try:
            self.remove_roleset(server, name)
            await self.bot.say("Roleset '%s' removed." % name)
        except XORoleException as e:
            await self.bot.say(warning(*e.args))

    @checks.mod_or_permissions(administrator=True)
    @xoroleset.command(name='renroleset', pass_context=True)
    async def xoroleset_renroleset(self, ctx, oldname: str, newname: str):
        "Renames a roleset."
        server = ctx.message.server
        try:
            if len(newname.split()) > 1:
                await self.bot.say('For usability reasons, whitespace is not '
                                   'permitted in roleset names. Try again.')
                return

            rsn, rsl = self.get_roleset(server, oldname)
            rolesets = self.get_rolesets(server)
            rolesets[newname] = rolesets.pop(rsn)
            self.update_rolesets(server, rolesets)
            await self.bot.say("Rename successful.")
        except XORoleException as e:
            await self.bot.say(warning(*e.args))

    @checks.mod_or_permissions(administrator=True)
    @xoroleset.command(name='audit', pass_context=True)
    async def xoroleset_audit(self, ctx):
        "Shows members with than one role in a xorole roleset"
        lines = []
        server = ctx.message.server
        try:
            for rsn, rsl in self.get_rolesets(server).items():
                member_role_pairs = []
                for member in server.members:
                    memberships = self.get_roleset_memberships(member, rsn)
                    if len(memberships) > 1:
                        member_role_pairs.append((member, memberships))

                if not member_role_pairs:
                    continue

                lines.append(rsn + ':')
                for member, roles in member_role_pairs:
                    lines.append(' - %s : %s'
                                 % (member.display_name,
                                    ', '.join(r.name for r in roles)
                                    )
                                 )
                lines.append('\n')

            if not lines:
                await self.bot.say('All roleset memberships are singular.')
                return

            if lines[-1] == '\n':
                lines.pop()

            for page in pagify('\n'.join(lines)):
                await self.bot.say(box(page))

        except XORoleException as e:
            await self.bot.say(warning(*e.args))

        except XORoleException as e:
            await self.bot.say(warning(*e.args))

    @checks.mod_or_permissions(administrator=True)
    @xoroleset.command(name='addroles', aliases=['addrole'], pass_context=True)
    async def xoroleset_addroles(self, ctx, roleset: str, *, roles: str):
        """Adds one or more roles to a xorole roleset.

        Takes names or IDs seperated by commas."""
        server = ctx.message.server
        msg = []
        try:
            roles = roles.split(',')
            found, notfound = self.find_roles(server, *roles)
            rsn, rsl = self.get_roleset(server, roleset)
            to_add = []
            too_high = []
            already_in_roleset = defaultdict(lambda: list())

            for role in found:
                role_rsn = self.roleset_of_role(role, notfound_ok=True)
                if role_rsn and rsn != role_rsn:
                    already_in_roleset[role_rsn].append(role)
                elif role < ctx.message.author.top_role:
                    to_add.append(role)
                else:
                    too_high.append(role)

            if to_add:
                added = self.add_roles(server, roleset, *to_add)
                if added:
                    msg.append('Added these roles to the %s roleset: %s.'
                               % (roleset, ', '.join(r.name for r in added)))
                else:
                    msg.append('All found roles already added; nothing to do.')

            if already_in_roleset:
                msg.append('Some roles are already in other rolesets:')
                for rsn, roles in already_in_roleset.items():
                    rolelist = ', '.join(r.name for r in roles)
                    msg.append(' - %s: %s' % (rsn, rolelist))

            if too_high:
                msg.append('These roles are too high for you to manage: %s.'
                           % ', '.join(r.name for r in too_high))

            if notfound:
                msg.append('Could not find these role(s): %s.'
                           % ', '.join(("'%s'" % x) for x in notfound))

            await self.bot.say('\n'.join(msg))

        except XORoleException as e:
            await self.bot.say(warning(*e.args))

    @checks.mod_or_permissions(administrator=True)
    @xoroleset.command(name='rmroles', aliases=['rmrole'], pass_context=True)
    async def xoroleset_rmroles(self, ctx, roleset: str, *, roles: str):
        """Removes one or more roles from a xorole roleset.

        Takes role names or IDs seperated by commas."""
        server = ctx.message.server
        msg = []
        try:
            roles = roles.split(',')
            found, notfound = self.find_roles(server, *roles)
            to_remove = []
            too_high = []

            for role in found:
                if role < ctx.message.author.top_role:
                    to_remove.append(role)
                else:
                    too_high.append(role)

            if found:
                removed = self.remove_roles(server, roleset, *found)
                if removed:
                    msg.append('Removed these roles from the %s roleset: %s.'
                               % (roleset, ', '.join(r.name for r in removed)))
                else:
                    msg.append('None of the found roles are in the list; nothing to do.')

            if too_high:
                msg.append('These roles are too high for you to manage: %s.'
                           % ', '.join(r.name for r in too_high))

            if notfound:
                msg.append('Could not find these role(s): %s.'
                           % ', '.join(("'%s'" % x) for x in notfound))

            await self.bot.say('\n'.join(msg))

        except XORoleException as e:
            await self.bot.say(warning(*e.args))

    async def on_command(self, command, ctx):
        if ctx.cog is self:
            self.analytics.command(ctx)


def setup(bot):
    if not dataIO.is_valid_json(JSON):
        print("Creating %s..." % JSON)
        dataIO.save_json(JSON, {})

    bot.add_cog(XORole(bot))
