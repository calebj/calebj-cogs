import asyncio
import aiohttp
import platform
import sys
import os
from collections import deque
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
from discord.ext import commands
from hashlib import sha1
from base64 import b64encode


class GVAnalytics:
    __version__ = 1.34
    STATS_URL = 'https://stats.calebj.io/piwik.php'
    BASE_URL = 'https://red.calebj.io/'
    PATH = 'data/lib_calebj/'
    JSON = PATH + 'analytics.json'
    Q1 = ("Hello! Caleb here. This is just a quick heads that I've started "
          "gathering usage information for my cogs.\n")
    Q2 = ("When enabled, your bot will send anonymous data about which cogs "
          "you've loaded and how many of each command you run, along with "
          "which OS and python version you're running.\n"
          "Nobody but me has access to the data, and I won't share it.\n\n"
          "You can read my full privacy policy here: "
          "<https://github.com/calebj/calebj-cogs/blob/master/PRIVACY.md>.\n"
          "Other questions? DM <@!152111727402680320> or email me@calebj.io ."
          )
    PARAM_BASE = {
        'idsite': 3,
        'rec'   : 1,
        'apiv'  : 1,
    }

    def __init__(self, bot, e=()):
        self.__module__ = 'cogs.lib_calebj.analytics'  # detach
        self.bot = bot
        self.terminate = False
        self.params_base = {}
        self.queue = deque(e, maxlen=512)
        self.gvanalytics.help = 'Enable or disable analytics for calebj cogs\n\n' + self.Q2

        self.data = {}
        if dataIO.is_valid_json(self.JSON):
            self.data = dataIO.load_json(self.JSON)

        self.task = self.bot.loop.create_task(self._start())

    @classmethod
    def start(cls, bot):
        cog = cls(bot)
        bot.add_cog(cog)
        return cog

    @classmethod
    def replace(cls, oldcog):
        if cls.__version__ > oldcog.__version__:
            if oldcog.__version__ > 1.32:
                cog = cls(oldcog.bot, oldcog.queue)
            else:
                cog = cls(oldcog.b, oldcog.q)
            cog.bot.remove_cog(oldcog.__class__.__name__)
            cog.bot.add_cog(cog)
            return cog

    def upgrade(self, newcls):
        return newcls.replace(self)

    def __unload(self):
        self.terminate = True
        self.task.cancel()

    def save(self):
        if not os.path.exists(self.PATH):
            os.makedirs(self.PATH)
        dataIO.save_json(self.JSON, self.data)

    def send(self, iface, cat, res=None, act=None, value=None, user=None, name_first=False):
        if self.terminate:
            return False

        self.queue.append((iface, cat, res, act, value, user, name_first))

        return True

    def _update_base_params(self, u):
        self.params_base = self.PARAM_BASE.copy()
        self.params_base.update({
            'uid': self.anon(u),
            '_id': self.anon(self.bot.user.id, True)[:16],
            'dimension2': self.anon(self.bot.user.id),
            'ua' : ' '.join((
                'Python/%s' % platform.python_version(),
                '(' + platform.system(), platform.release() + ')',
                self.__class__.__name__ + '/%s' % self.__version__
            ))
        })

    async def _ask_consent(self, owner):
        try:
            m = await self.bot.send_message(owner, self.Q1 + self.Q2 + "Type 'OK' if you're fine with this.")
            reply = await self.bot.wait_for_message(channel=m.channel, author=owner, timeout=600)

            a = reply and reply.content.lower().startswith(('ok'))
            if a:
                self.data['consent'] = True
                reply = 'Analytics have been enabled.'
            elif reply:
                self.data['consent'] = False
                reply = 'You have declined to participate in analytics.'
            else:
                reply = "Timed out waiting for a response. I'll ask again later."

            reply += ' You can use `[p]gvanalytics` to change this option at any time.'
            await self.bot.send_message(owner, reply)
            self.save()
            return a
        except Exception:
            return None

    async def _start(self):
        try:
            await self.bot.wait_until_ready()
            if self.bot.user.bot:
                u = await self.bot.get_user_info(self.bot.settings.owner)
            else:
                u = self.bot.user
            self._update_base_params(u.id)

            if self.data.get('consent') is None:
                if self.bot.user.bot:
                    await self._ask_consent(u)
                else:
                    await asyncio.sleep(1)
                    m = "If you're okay with this, run [p]gvanalytics on\a"
                    m = ['=' * 80, self.Q1 + self.Q2 + m, '=' * 80]
                    print('\n\n'.join(m))

            await self._run()

        except asyncio.CancelledError:
            pass

    async def _run(self):
        async with aiohttp.ClientSession() as cs:
            while not self.terminate:
                await asyncio.sleep(0.1)
                if not self.data.get('consent') or not len(self.queue):
                    continue

                event = self.queue.popleft()
                if not await self._send(cs, event):
                    self.queue.append(event)  # retry later

    async def _send(self, session, event):
        params = self._get_params(event)
        async with session.get(self.STATS_URL, params=params, timeout=10) as resp:
            async with resp:
                return resp.status in {200, 204}

    def _get_params(self, event):
        iface, cat, res, act, value, user, name_first = event
        ret = self.params_base.copy()
        ev_path = [cat]

        if (act if name_first else res):
            ev_path.extend([act, res] if name_first else [res, act])

        anp = '/'.join(i for i in ev_path if i)

        ret.update({
            'act_name': anp,
            'url' : self.BASE_URL + anp,
            'dimension1': iface.version
        })

        if user is not None:
            ret['uid'] = self.anon(user)

        return ret

    @commands.command(name='gvanalytics')
    @checks.is_owner()
    async def gvanalytics(self, on_off: bool = None):
        'Enable or disable analytics for calebj cogs'
        if on_off is not None:
            self.data['consent'] = on_off
            self.save()
            v = 'have been'
        else:
            on_off = self.data.get('consent')
            v = 'are currently'

        w = 'enabled' if on_off else 'disabled'
        await self.bot.say('Analytics %s %s.' % (v, w))

    def anon(self, d, h=False):
        b = sha1(d.encode())
        if h:
            return b.hexdigest()
        else:
            return b64encode(b.digest()).decode()


class AnalyticsInterface:
    def __init__(self, bot):
        self.bot = bot
        self.version = None
        self.project = None

    def send_action(self, cat, res=None, act=None, value=None, uid=None, name_first=False):
        core = self._get_core()
        if core:
            return core.send(self, cat, res, act, value, uid, name_first)
        return False

    def _get_core(self):
        cog = self.bot.get_cog('GVAnalytics')
        if not cog:
            return GVAnalytics.start(self.bot)

        return GVAnalytics.replace(cog) or cog


class CogAnalytics(AnalyticsInterface):
    def __init__(self, wrapped):
        super().__init__(wrapped.bot)
        module = sys.modules.get(wrapped.__module__)
        if module:
            module_ver = getattr(module, '__version__', None)
        else:
            module_ver = None

        self.version = getattr(wrapped, '__version__', module_ver)
        self.project = getattr(wrapped, '__name__', wrapped.__class__.__name__)
        self.send_action('cog', self.project, 'load', name_first=True)

    def command(self, ctx, value=None):
        uid = ctx.message.author.id
        self.send_action('command', self.project, ctx.command.qualified_name,
                         value, uid=uid)
