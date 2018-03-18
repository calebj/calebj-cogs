"""Elo cog by GrumpiestVulcan (@calebj#0001)
Commissioned 2018-03-17 by Cxllum#6979"""

from copy import deepcopy
import discord
from discord.ext import commands
from io import BytesIO
from random import choice as randchoice
import re
from .utils.dataIO import dataIO
from .utils.chat_formatting import pagify, box, warning, error, info
from .utils import checks

JSON = 'data/rolelicense.json'
# No 0 or 1 because of potential ambiguity with O and I when reading
KEY_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ23456789'

DEFAULT_TEMPLATE = "{{5}}-{{5}}-{{5}}"
TEMPLATE_RE = r'\{\{(\d+)\}\}'

# {string server_id : {'roles' : {int index : string role_id},
#                      'keys'  : {string key : int index},
#                      'used'  : {string key : [int index,
#                                               string user_id]}
#                                 }}
DEFAULTS = {
    'roles' : {},
    'keys'  : {},
    'used'  : {}
}


class RoleLicense:
    """Redeem role assignments using randomly generated keys"""
    def __init__(self, bot):
        self.bot = bot
        self.data = dataIO.load_json(JSON)

    def save_data(self):
        dataIO.save_json(JSON, self.data)

    def get_data(self, server: discord.Server, create=True):
        if server.id not in self.data:
            if not create:
                return None
            self.data[server.id] = deepcopy(DEFAULTS)
        return self.data[server.id]

    @commands.group(pass_context=True, no_pm=True, aliases=['rlic'], invoke_without_command=True)
    async def rolelicense(self, ctx, *, key: str):
        "Role license commands. Defaults to redeem."
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.redeem, key=key)

    @rolelicense.command(pass_context=True)
    async def redeem(self, ctx, *, key: str):
        """
        Redeems a key
        """

        data = self.get_data(ctx.message.server)
        index = data['keys'].pop(key, None)
        if index is not None:
            index = int(index)
            data['used'][key] = [index, ctx.message.author.id]

            role_id = data['roles'][str(index)]
            role = discord.utils.get(ctx.message.server.roles, id=role_id)

            if str(-index) in data['roles']:
                msg = ('That key for the %s role is valid and is now marked '
                       'as used, but redeeming that role has been disabled. '
                       ' Contact an administrator for help.' % role.name)
                await self.bot.say(error(msg))
                return

            if role:
                try:
                    await self.bot.add_roles(ctx.message.author, role)
                    await self.bot.say(info('Added the %s role to you.'
                                            % role.name))
                except discord.Forbidden:
                    msg = ("That key for the %s role is valid and is now "
                           "marked as used, but I don't have the permissions "
                           "to add it to you. Contact an administrator for "
                           "help." % role.name)

                    if not role.server.me.server_permissions.manage_roles:
                        msg += '\n\nAdmin: I lack the "manage roles" permission.'
                    elif role >= role.server.me.top_role:
                        msg += '\n\nAdmin: the role is too high for me to manage.'

                    await self.bot.say(error(msg))
                except Exception:
                    logger.exception('Unable to add the "%s" role in "%s".'
                                     % (role, ctx.message.server))
                    msg = ('That key for the %s role is valid and is now '
                           'marked as used, but there was an error adding '
                           'the role. Contact an administrator for help.')
                    await self.bot.say(error(msg % role.name))
            else:
                msg = ('That key is valid, but its role has been deleted. '
                       'Contact an administrator for help.')
                await self.bot.say(error(msg))

            self.save_data()
            return

        used = data['used'].get(key)
        if used:
            await self.bot.say(warning('That key has already been redeemed.'))
            return

        await self.bot.say(warning('Invalid key.'))

    @rolelicense.command(pass_context=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def addrole(self, ctx, role: discord.Role):
        """
        Adds a role to the list of redeemable ones
        """

        data = self.get_data(ctx.message.server)

        for i, role_id in data['roles'].items():
            i = int(i)
            if role_id != role.id:
                continue
            elif i < 0:
                data['roles'][str(-i)] = data['roles'].pop(str(i))
                self.save_data()
                await self.bot.say(info('Role re-enabled.'))
                return
            else:
                await self.bot.say(warning('That role is already in the list.'
                                           ''))
                return

        # If we get here, the role is not in the list yet

        if data['roles']:
            next_index = max(map(abs, map(int, data['roles']))) + 1
        else:
            next_index = 1

        data['roles'][str(next_index)] = role.id
        self.save_data()

        await self.bot.say(info('Role added.'))

    @rolelicense.command(pass_context=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def rmrole(self, ctx, role: discord.Role):
        """
        Removes a role from the list of redeemable ones

        Note that keys will show a message that the role has been disabled.
        If you want to transfer the keys to another role, use mvkeys.
        To re-enable the role, use addrole again.
        """

        data = self.get_data(ctx.message.server)

        for i, role_id in data['roles'].items():
            i = int(i)
            if role_id != role.id:
                continue
            elif i > 0:
                data['roles'][str(-i)] = data['roles'].pop(str(i))
                self.save_data()
                await self.bot.say(info('Role disabled.'))
                return
            else:
                await self.bot.say(warning('That role is already disabled.'))
                return

        await self.bot.say(error('That role is not in the list yet.'))

    @rolelicense.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def generate(self, ctx, quantity: int, role: discord.Role, attachment: bool = False, *, template=DEFAULT_TEMPLATE):
        """
        Generates a list of keys for a role

        Keys are sent as a text file attachment if [attachment] is true.
        Template specification substitutes {{N}} with N random characters.
        """

        data = self.get_data(ctx.message.server)

        found = None
        for i, role_id in data['roles'].items():
            i = int(i)
            if role_id != role.id:
                continue
            else:
                found = i
                break

        if found is None:
            await self.bot.say(error('That role is not in the list yet.'))
            return
        elif quantity <= 0:
            await self.bot.say(error('Quantity must be 1 or more.'))
            return

        # TODO: check template sanity and existing keys

        keys = [re.sub(TEMPLATE_RE, self.sub_random, template)
                for i in range(quantity)]
        data['keys'].update({key: found for key in keys})

        if attachment:
            buf = BytesIO()
            for k in keys:
                buf.write(k.encode() + b'\n')

            buf.seek(0)

            filename = "{0.name}-{1.name}.keys.txt".format(
                ctx.message.server,
                role
            )
            await self.bot.send_file(ctx.message.author, buf,
                                     filename=filename)
        else:
            header = 'Keys for {1.name} in {0.name}:\n'.format(
                ctx.message.server,
                role
            )
            keystr = '\n'.join(keys)
            for page in pagify(header + keystr):
                await self.bot.whisper(box(page))

        self.save_data()
        await self.bot.say('Keys generated; check your DMs.')

    @rolelicense.command(pass_context=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def mvkeys(self, ctx, oldrole: discord.Role, newrole: discord.Role):
        """
        Moves unused keys from one role to another
        """

        self.save_data()

    @rolelicense.command(pass_context=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def mvkeys-id(self, ctx, oldrole_id: str, newrole: discord.Role):
        """
        Moves unused keys from a delteed role to another
        """

        self.save_data()

    @rolelicense.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def info(self, ctx):
        """
        Lists (ex-)redeemable roles and their stats
        """

    @staticmethod
    def sub_random(match):
        count = int(match.group(1))
        return ''.join(randchoice(KEY_CHARS) for x in range(count))


def check_files():
    if not dataIO.is_valid_json(JSON):
        print("Creating empty %s" % JSON)
        dataIO.save_json(JSON, {})


def setup(bot):
    check_files()
    bot.add_cog(RoleLicense(bot))
