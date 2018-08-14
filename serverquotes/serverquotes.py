import aiohttp
import csv
from datetime import datetime
import discord
from discord.ext import commands
from discord.ext.commands.view import StringView
from enum import Enum
from io import BytesIO, StringIO
import math
import os
from random import randrange
import re
import sqlite3
import struct
from textwrap import dedent
from typing import Iterable, Optional, Sequence

from .utils.chat_formatting import error, warning
from .utils.checks import check_permissions, is_owner, admin_or_permissions, mod_or_permissions
from .utils.dataIO import dataIO


PATH = 'data/serverquotes/'
JSON = PATH + 'quotes.json'
SQLDB = PATH + 'quotes.sqlite'
DEFAULT_UPDATE_KEYS = (('quote_id',), ('server_id', 'server_quote_id'))

# message links in embeds don't work yet
# PERMALINK = 'https://discordapp.com/channels/{server_id}/{channel_id}/{message_id}'

numbs = {
    "back_10": "⏪",
    "back": "⬅",
    "exit": "❌",
    "next": "➡",
    "next_10": "⏩",
    "random": "🎲",
    "show": "🔍"
}

INIT_SQL = """
CREATE TABLE IF NOT EXISTS quotes (
    quote_id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id INTEGER NOT NULL,
    server_quote_id INTEGER,
    date_said TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    added_by INTEGER NOT NULL,
    author_id INTEGER,
    author_name TEXT COLLATE NOCASE,
    quote TEXT,
    migrated INTEGER DEFAULT 0,
    image_url TEXT,
    attachment_url TEXT,
    attachment_filename TEXT,
    channel_id INTEGER,
    message_id INTEGER,
    UNIQUE (server_id, server_quote_id)
);

CREATE INDEX IF NOT EXISTS quotes_server_id ON quotes(server_id);
CREATE INDEX IF NOT EXISTS quotes_server_quote_id ON quotes(server_quote_id);
CREATE INDEX IF NOT EXISTS quotes_date_added ON quotes(date_added);
CREATE INDEX IF NOT EXISTS quotes_date_said ON quotes(date_said);
CREATE INDEX IF NOT EXISTS quotes_added_by ON quotes(added_by);
CREATE INDEX IF NOT EXISTS quotes_author_id ON quotes(author_id);

CREATE TABLE IF NOT EXISTS server_counters (
    server_id INTEGER NOT NULL,
    last_qid INTEGER NOT NULL DEFAULT 0,
    UNIQUE (server_id)
);

CREATE TRIGGER IF NOT EXISTS quotes_set_sqid AFTER INSERT ON quotes
  WHEN NEW.server_quote_id IS NULL
  BEGIN
    REPLACE INTO server_counters (server_id, last_qid)
        VALUES (NEW.server_id,
                COALESCE((SELECT last_qid FROM server_counters sc WHERE sc.server_id IS NEW.server_id), 0) + 1);

    UPDATE quotes
        SET server_quote_id = (SELECT last_qid FROM server_counters WHERE server_counters.server_id IS NEW.server_id)
        WHERE quotes.quote_id = NEW.quote_ID;
  END;

CREATE TRIGGER IF NOT EXISTS quotes_reset_sqid AFTER UPDATE ON quotes
  WHEN NEW.server_quote_id IS NULL
  BEGIN
    REPLACE INTO server_counters (server_id, last_qid)
        VALUES (NEW.server_id,
                COALESCE((SELECT last_qid FROM server_counters sc WHERE sc.server_id IS NEW.server_id), 0) + 1);

    UPDATE quotes
        SET server_quote_id = (SELECT last_qid FROM server_counters WHERE server_counters.server_id IS NEW.server_id)
        WHERE quotes.quote_id = NEW.quote_ID;
  END;

CREATE TRIGGER IF NOT EXISTS quotes_set_sqid_noinc AFTER INSERT ON quotes
  WHEN NEW.server_quote_id IS NOT NULL
  BEGIN
    REPLACE INTO server_counters (server_id, last_qid)
        VALUES (NEW.server_id,
                MAX(COALESCE((SELECT last_qid FROM server_counters sc WHERE sc.server_id IS NEW.server_id), 0),
                    COALESCE((SELECT MAX(server_quote_id) FROM quotes q WHERE q.server_id IS NEW.server_id), 0)));
  END;

CREATE TABLE IF NOT EXISTS nicknames (
    server_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    nickname TEXT,
    PRIMARY KEY (server_id, user_id)
);

CREATE INDEX IF NOT EXISTS nicknames_server_id ON nicknames(server_id);
CREATE INDEX IF NOT EXISTS nicknames_server_uid ON nicknames(server_id, user_id);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    discriminator INTEGER NOT NULL,
    avatar_url TEXT,
    UNIQUE (username, discriminator)
);

CREATE TABLE IF NOT EXISTS server_links (
    from_id INTEGER NOT NULL,
    to_id INTEGER NOT NULL,
    PRIMARY KEY (from_id, to_id)
);

CREATE INDEX IF NOT EXISTS server_links_from_id ON server_links(from_id);

DROP VIEW IF EXISTS quotes_view;

CREATE VIEW IF NOT EXISTS quotes_view_230 AS
  SELECT quotes.*,
         qu.avatar_url AS author_avatar_url,
         au.avatar_url AS added_by_avatar_url,
         COALESCE(qu.username || '#' || SUBSTR('0000' || qu.discriminator, -4, 4), author_name,
                  'missingno#' || author_id, '(unknown)') AS global_author,
         COALESCE(au.username || '#' || SUBSTR('0000' || au.discriminator, -4, 4),
                  'missingno#' || added_by, '(unknown)') AS global_added_by,
         COALESCE(qn.nickname, qu.username || '#' || SUBSTR('0000' || qu.discriminator, -4, 4), author_name,
                  'missingno#' || author_id, '(unknown)') AS display_author,
         COALESCE(an.nickname, au.username || '#' || SUBSTR('0000' || au.discriminator, -4, 4),
                  'missingno#' || added_by, '(unknown)') AS display_added_by
  FROM quotes
  LEFT JOIN users qu ON qu.user_id = quotes.author_id
  LEFT JOIN users au ON au.user_id = quotes.added_by
  LEFT JOIN nicknames qn ON qn.server_id = quotes.server_id
                        AND qn.user_id = quotes.author_id
  LEFT JOIN nicknames an ON an.server_id = quotes.server_id
                        AND an.user_id = quotes.added_by;
"""

FTS_SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS quotes_fts USING FTS4(tokenize=porter);

CREATE TRIGGER IF NOT EXISTS quotes_fts_INSERT AFTER INSERT ON quotes
  BEGIN
    INSERT INTO quotes_fts(rowid, content) VALUES (NEW.quote_id, NEW.quote);
  END;

DROP TRIGGER IF EXISTS quotes_view_UPDATE;
DROP TRIGGER IF EXISTS quotes_view_DELETE;

CREATE TRIGGER IF NOT EXISTS quotes_DELETE AFTER DELETE ON quotes
  BEGIN
    DELETE FROM quotes_fts WHERE rowid = OLD.rowid;
  END;

CREATE TRIGGER IF NOT EXISTS quotes_UPDATE AFTER UPDATE ON quotes
  WHEN OLD.quote <> NEW.quote
  BEGIN
    UPDATE quotes_fts SET content=NEW.quote WHERE quotes_fts.rowid = OLD.quote_id;
  END;
"""

SQL_211 = """
CREATE TABLE server_counters_new (
    server_id INTEGER NOT NULL DEFAULT 0,
    last_qid INTEGER NOT NULL DEFAULT 0,
    UNIQUE (server_id)
);

INSERT INTO server_counters_new (server_id, last_qid)
    SELECT COALESCE(server_id, 0), MAX(last_qid)
    FROM server_counters
    GROUP BY server_id;

DROP TABLE server_counters;
ALTER TABLE server_counters_new RENAME TO server_counters;
"""

NAMES_SQL = """
SELECT DISTINCT server_id, user_id, nickname, username, discriminator, avatar_url FROM (
    SELECT server_id, author_id AS user_id FROM quotes
    UNION
    SELECT server_id, added_by AS user_id FROM quotes
)
LEFT NATURAL JOIN users
LEFT NATURAL JOIN nicknames
WHERE user_id IS NOT NULL;
"""

RANK_SQL = "bm25(MATCHINFO(quotes_fts, 'pcnalx'), 1)"

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

__version__ = '2.4.1'


class SortField(Enum):
    NONE = None
    QUOTE_ID = 'quote_id'
    SERVER_QUOTE_ID = 'server_quote_id'
    DATE_ADDED = 'date_added'
    DATE_SAID = 'date_said'


class SortDirection(Enum):
    NONE = None
    ASC = 'ASC'
    DESC = 'DESC'
    RANDOM = 'RANDOM()'


def okay(text):
    return "\N{WHITE HEAVY CHECK MARK} {}".format(text)


def check_fts4() -> bool:
    with sqlite3.connect(':memory:') as con:
        cur = con.execute('pragma compile_options;')
        available_pragmas = cur.fetchall()
        return ('ENABLE_FTS3',) in available_pragmas


def _parse_match_info(buf):
    # See http://sqlite.org/fts3.html#matchinfo
    bufsize = len(buf)  # Length in bytes.
    return [struct.unpack('@I', buf[i:i + 4])[0] for i in range(0, bufsize, 4)]


# Okapi BM25 ranking implementation (FTS4 only).
def bm25(raw_match_info, *args):
    """
    Usage:
        # Format string *must* be pcnalx
        # Second parameter to bm25 specifies the index of the column, on
        # the table being queries.
        bm25(matchinfo(document_tbl, 'pcnalx'), 1) AS rank
    """
    match_info = _parse_match_info(raw_match_info)
    K = 1.2
    B = 0.75
    score = 0.0

    P_O, C_O, N_O, A_O = range(4)
    term_count = match_info[P_O]
    col_count = match_info[C_O]
    total_docs = match_info[N_O]
    L_O = A_O + col_count
    X_O = L_O + col_count

    if not args:
        weights = [1] * col_count
    else:
        weights = [0] * col_count
        for i, weight in enumerate(args):
            weights[i] = args[i]

    for i in range(term_count):
        for j in range(col_count):
            weight = weights[j]
            if weight == 0:
                continue

            avg_length = float(match_info[A_O + j])
            doc_length = float(match_info[L_O + j])
            if avg_length == 0:
                D = 0
            else:
                D = 1 - B + (B * (doc_length / avg_length))

            x = X_O + (3 * j * (i + 1))
            term_frequency = float(match_info[x])
            docs_with_term = float(match_info[x + 2])

            idf = max(
                math.log(
                    (total_docs - docs_with_term + 0.5) /
                    (docs_with_term + 0.5)),
                0)
            denom = term_frequency + (K * D)
            if denom == 0:
                rhs = 0
            else:
                rhs = (term_frequency * (K + 1)) / denom

            score += (idf * rhs) * weight

    return -score


def _map_scalar_or_vector(value, operation, check_type=None):
    if check_type is not None:
        def conv(x):
            return operation(x) if isinstance(x, check_type) else x
    else:
        conv = operation

    if isinstance(value, Iterable) and not isinstance(value, str):
        return tuple(conv(x) for x in value)
    else:
        return conv(value)


class ServerQuotes:
    """
    Store and retrieve memorable quotes from your server
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect(SQLDB, detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row

        with self.db as con:
            con.executescript(INIT_SQL)

            if check_fts4():
                self.has_fts = True
                con.executescript(FTS_SQL)
                con.create_function('bm25', -1, bm25)
            else:
                self.has_fts = False

        self.bot.loop.create_task(self._populate_userinfo())
        self.bot.loop.create_task(self._upgrade_210())
        self._upgrade_211()
        self._upgrade_230()

        try:
            self.analytics = CogAnalytics(self)
        except Exception as e:
            self.bot.logger.exception(e)
            self.analytics = None

    def __unload(self):
        self.save()
        self.db.close()

    def save(self):
        self.db.commit()

    # Authorization/permission checks

    async def _authorize_del(self, ctx, record):
        if record['added_by'] == int(ctx.message.author.id):
            return True
        elif check_permissions(ctx, {'administrator': True}):
            return True
        else:
            return self.is_mod_or_superior(ctx.message.author)

    # DB interface

    async def _populate_userinfo(self):
        await self.bot.wait_until_ready()

        with self.db:
            users = {}
            nicknames = {}
            missing_ids = set()
            updated_ids = set()

            query = self.db.execute(NAMES_SQL)

            for server_id, user_id, nickname, username, discriminator, avatar_url in query:
                server = self.bot.get_server(str(server_id))

                if not server:
                    continue

                member = server.get_member(str(user_id))

                if not member:
                    missing_ids.add(user_id)
                    continue

                m_avatar_url = member.avatar_url or member.default_avatar_url

                if user_id not in users and (discriminator != member.discriminator or username != member.name
                                             or avatar_url != m_avatar_url):
                    users[user_id] = (member.name, member.discriminator, m_avatar_url)

                nk = (server_id, user_id)
                if nk not in nicknames and nickname != member.nick:
                    nicknames[nk] = member.nick

                updated_ids.add(user_id)

            missing_ids -= updated_ids

            if missing_ids:
                missing_ids = set(str(x) for x in missing_ids)

                for member in self.bot.get_all_members():
                    if member.id in missing_ids:
                        missing_ids.remove(member.id)
                        users[int(member.id)] = (member.name, member.discriminator,
                                                 member.avatar_url or member.default_avatar_url)

            if users:
                rows = [(uid, *t) for uid, t in users.items()]
                self.db.executemany("REPLACE INTO users (user_id, username, discriminator, avatar_url) "
                                    "VALUES (?, ?, ?, ?);", rows)

            if nicknames:
                rows = [(*nk, nickname) for nk, nickname in nicknames.items()]
                self.db.executemany("REPLACE INTO nicknames (server_id, user_id, nickname) VALUES (?, ?, ?);", rows)

    async def _upgrade_210(self):
        with self.db as con:
            cols = {c['name'] for c in con.execute("PRAGMA table_info(quotes);")}

            for cname, ctype in {
                'image_url'           : 'TEXT',
                'attachment_url'      : 'TEXT',
                'attachment_filename' : 'TEXT',
                'message_id'          : 'INTEGER',
                'channel_id'          : 'INTEGER'
            }.items():
                if cname not in cols:
                    con.execute("ALTER TABLE quotes ADD COLUMN {} {};".format(cname, ctype))
                if ctype == 'INTEGER':
                    con.execute("CREATE INDEX IF NOT EXISTS quotes_{0}_idx ON quotes({0});".format(cname))

        url_regex = re.compile(r"(?is)\b(?:https?://)(?:[a-z0-9]\.?)+/[^\s]+")

        with self.db as con:
            async with aiohttp.ClientSession() as session:
                for row in con.execute("SELECT quote_id, quote FROM quotes WHERE image_url IS NULL;"):
                    match = url_regex.search(row['quote'])

                    if not match:
                        continue

                    url = match.group()

                    async with session.head(url, allow_redirects=True) as response:
                        if response.status != 200 or not response.headers['Content-Type'].lower().startswith('image/'):
                            continue

                    params = [row['quote'].replace(url, ''), url, row['quote_id']]
                    con.execute("UPDATE quotes SET quote = ?, image_url = ? WHERE quote_id = ?", params)

    def _upgrade_211(self):
        with self.db as con:
            cols = {c['name']: c for c in con.execute("PRAGMA table_info(server_counters);")}

            if cols['server_id']['pk']:
                con.executescript(SQL_211)

    def _upgrade_230(self):
        with self.db as con:
            cols = {c['name']: c for c in con.execute("PRAGMA table_info(quotes);")}

            if 'is_global' not in cols:
                con.executescript("ALTER TABLE quotes ADD COLUMN is_global INTEGER NOT NULL DEFAULT 0;"
                                  "CREATE INDEX quotes_is_global ON quotes(is_global);")

    def _update_member(self, member: discord.Member, update_only=False):
        mid = int(member.id)
        avatar = member.avatar_url or member.default_avatar_url

        with self.db as con:
            if update_only:
                con.execute("UPDATE nicknames SET nickname = ? WHERE server_id = ? AND user_id = ?",
                            (member.nick, member.server.id, mid))
                con.execute("UPDATE users SET username = ?, discriminator = ?, avatar_url = ? WHERE user_id = ?",
                            (member.name, member.discriminator, avatar, mid))
            else:
                con.execute("REPLACE INTO nicknames(server_id, user_id, nickname) VALUES (?, ?, ?);",
                            (member.server.id, mid, member.nick))
                con.execute("REPLACE INTO users(user_id, username, discriminator, avatar_url) VALUES (?, ?, ?, ?);",
                            (mid, member.name, member.discriminator, avatar))

    def _normalize_kwargs(self, kwargs):
        kwargs = kwargs.copy()

        for k in ('server', 'author'):
            if k in kwargs:
                obj = kwargs.pop(k)
                kwargs[k + '_id'] = obj and _map_scalar_or_vector(obj, lambda x: x.id)

                if k == 'author' and obj.server and 'server_id' not in kwargs:
                    kwargs['server_id'] = _map_scalar_or_vector(obj, lambda x: x.server.id)

        if 'added_by' in kwargs:
            kwargs['added_by'] = _map_scalar_or_vector(kwargs['added_by'], lambda x: x.id, check_type=discord.User)

        for k in ('quote_id', 'server_id', 'server_quote_id', 'added_by', 'author_id', 'message_id', 'channel_id'):
            if k in kwargs:
                kwargs[k] = _map_scalar_or_vector(kwargs[k], int, str)

        # for k in ('date_added', 'date_said'):
        #     if isinstance(kwargs.get(k), datetime):
        #         kwargs[k] = int(kwargs[k].timestamp())

        for k in ('migrated', 'is_global'):
            if k in kwargs and not isinstance(kwargs[k], (bool, type(None))):
                kwargs[k] = int(bool(kwargs[k]))

        return kwargs

    def _build_where(self, kwargs, params=None, wheres=None):
        if wheres is None:
            wheres = []

        if params is None:
            params = []

        for param, value in kwargs.items():
            if isinstance(value, Iterable) and not isinstance(value, str):
                if not isinstance(value, Sequence):
                    value = tuple(value)

                wheres.append(param + " IN (%s)" % ', '.join('?' * len(value)))
                params.extend(value)
            else:
                wheres.append(param + " IS ?")
                params.append(value)

        if wheres:
            where = " WHERE " + " AND ".join(wheres)
        else:
            where = " "

        return where, params

    def _message_to_kwargs(self, message: discord.Message, set_server=True) -> dict:
        kwargs = {
            'message_id' : int(message.id),
            'author_id'  : int(message.author.id),
            'channel_id' : int(message.channel.id),
            'quote'      : message.content,
            'date_said'  : message.timestamp
        }

        if set_server:
            kwargs['server_id'] = int(message.server.id)

        if message.embeds:
            data = message.embeds[0]
            if data['type'] == 'image':
                kwargs['image_url'] = data['url']

                if kwargs['quote']:
                    kwargs['quote'] = kwargs['quote'].replace(data['url'], '')

        if message.attachments:
            file = message.attachments[0]
            if file['url'].lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')) \
                    or ('width' in file and 'height' in file):
                kwargs['image_url'] = file['url']
            else:
                kwargs['attachment_url'] = file['url']
                kwargs['attachment_filename'] = file['filename']

        return kwargs

    def _add_quote(self, ctx, **kwargs):
        message = kwargs.pop('message', ctx.message)
        message_dict = self._message_to_kwargs(message, set_server=kwargs.get('server') is None)

        if message is ctx.message:
            for k in ('message', 'channel', 'server'):
                k += '_id'
                if k in message_dict:
                    kwargs[k] = message_dict[k]
        else:
            kwargs.update(message_dict)

        if 'added_by' not in kwargs:
            kwargs['added_by'] = ctx.message.author.id

        params = self._normalize_kwargs(kwargs)

        if 'quote' not in params:
            params['quote'] = ''

        columns = list(params)
        params = [params[k] for k in columns]
        sql = "INSERT INTO quotes (%s) VALUES (%s);" % (', '.join(columns), ', '.join('?' * len(params)))

        with self.db as con:
            cur = con.execute(sql, params)
            return cur.execute("SELECT * FROM quotes_view_230 WHERE quote_id = last_insert_rowid();").fetchone()

    def _update_quotes(self, key_on=DEFAULT_UPDATE_KEYS, *, where=None, enforce_key=True, **kwargs) -> int:
        if 'message' in kwargs:
            message = kwargs.pop('message')
            message_dict = self._message_to_kwargs(message, set_server=kwargs.get('server') is None)
            kwargs.update(message_dict)

        params = self._normalize_kwargs(kwargs)

        if key_on is not DEFAULT_UPDATE_KEYS and where is not None:
            raise ValueError("only key_on OR where can be defined, not both")
        elif where and not isinstance(where, dict):
            raise TypeError("where must be a dict")
        elif where:
            if 'message' in where:
                message = where.pop('message')
                message_dict = self._message_to_kwargs(message, set_server=where.get('server') is None)
                where.update(message_dict)

            where = self._normalize_kwargs(where)
        else:
            where = {}

            for keys in key_on:
                if all(k in params for k in keys):
                    if where:
                        raise ValueError('extra identifying keys: %s' % (keys,))

                    where.update({k: params.pop(k) for k in keys})

        if enforce_key and not where:
            raise ValueError('no identifying keys found in passed arguments')
        elif not params:
            raise ValueError('no data to update')

        columns = list(params)
        params = [params[k] for k in columns]
        sets = ', '.join('%s = ?' % c for c in columns)
        where, params = self._build_where(where, params)
        sql = "UPDATE quotes SET %s %s;" % (sets, where)

        with self.db as con:
            cursor = con.execute(sql, params)
            return cursor.rowcount

    def _delete_quotes(self, **kwargs) -> int:
        kwargs = self._normalize_kwargs(kwargs)
        where, params = self._build_where(kwargs)
        sql = "DELETE FROM quotes " + where

        with self.db as con:
            cursor = con.execute(sql, params)
            return cursor.rowcount

    def _populate_linked_server_ids(self, kwargs):
        if 'server_id' in kwargs:
            server_id = kwargs['server_id']

            if not isinstance(server_id, Iterable):
                server_id = [server_id]

            with self.db as con:
                params = ','.join('?'*len(server_id))
                cur = con.execute("SELECT to_id FROM server_links WHERE from_id IN (%s)" % params, server_id)
                server_id.extend(r['to_id'] for r in cur.fetchall())

            kwargs['server_id'] = server_id

        return kwargs

    def _get_quotes(self, sort_field=SortField.QUOTE_ID, sort_direction=SortDirection.ASC, limit=None, **kwargs):
        kwargs = self._normalize_kwargs(kwargs)

        if kwargs.pop('link', False):
            kwargs = self._populate_linked_server_ids(kwargs)

        where, params = self._build_where(kwargs)

        sql = "SELECT * FROM quotes_view_230 " + where

        if sort_direction is SortDirection.RANDOM:
            sql += " ORDER BY RANDOM() "
        elif isinstance(sort_field, SortField) and sort_field is not SortField.NONE:
            sql += " ORDER BY `%s` " % sort_field.value

            if isinstance(sort_direction, SortDirection) and sort_direction is not SortDirection.NONE:
                sql += sort_direction.value

        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)

        with self.db as con:
            cur = con.execute(sql, params)
            return cur.fetchall()

    def _do_search(self, term, limit=10, offset=0, link=False, **kwargs):
        kwargs = self._normalize_kwargs(kwargs)

        if link:
            kwargs = self._populate_linked_server_ids(kwargs)

        where, params = self._build_where(kwargs, params=[term], wheres=["content MATCH ?"])

        if not self.has_fts:
            return []

        sql = dedent("""
            SELECT SNIPPET(quotes_fts, '**', '**', '…') AS snippet, quotes_view_230.*
            FROM quotes_fts
            JOIN (
                SELECT docid, bm25(MATCHINFO(quotes_fts, 'pcnalx'), 1) AS rank
                FROM quotes_fts
                JOIN quotes_view_230 ON docid = quote_id
                {where} ORDER BY rank DESC LIMIT ? OFFSET ?
            ) AS rt USING(docid)
            JOIN quotes_view_230 ON quote_id = docid
            WHERE quotes_fts MATCH ? ORDER BY rt.rank DESC
            """.format(where=where))

        params.extend((limit, offset, term))

        with self.db as con:
            cur = con.execute(sql, params)
            return cur.fetchall()

    # Commands

    @commands.group(pass_context=True, no_pm=True, invoke_without_command=True)
    async def quote(self, ctx, *, num_or_member: str = None):
        """
        Show/mange server quotes

        If no valid subcommand is given, attempts to look up quote ID or member.
        [p]quote random also works. Without any argument, invokes [p]quote list.
        [p]quote help displays this help and all subcommands.
        """
        if num_or_member and num_or_member.strip(" '\"`").lower() == 'random':
            ctx.view = StringView('yes')
            await self.quote_list.invoke(ctx)
        elif num_or_member and num_or_member.strip(" '\"`").lower() == 'help':
            await self.bot.send_cmd_help(ctx)
        elif num_or_member:
            ctx.view = StringView(num_or_member)

            if num_or_member.isdecimal():
                await self.quote_show.invoke(ctx)
            else:
                await self.quote_by.invoke(ctx)
        else:
            await self.quote_list.invoke(ctx)

    @commands.cooldown(6, 60, commands.BucketType.channel)
    @quote.command(pass_context=True, no_pm=True, name='list')
    async def quote_list(self, ctx, jump_to_random: bool = False):
        """
        Allows you to page through a list of all quotes
        """
        records = self._get_quotes(server=ctx.message.server, link=True)

        if not records:
            await self.bot.say(warning("There are no quotes in this server!"))
            return

        if len(records) > 1:
            page = randrange(len(records)) if jump_to_random else 0
            await self.embed_menu(ctx, records, page=page)
        else:
            embed = self.format_quote_embed(ctx, records[0])
            await self.bot.say(embed=embed)

    @quote.command(pass_context=True, no_pm=True, name='search', rest_is_raw=True)
    @commands.cooldown(6, 60, commands.BucketType.channel)
    async def quote_search(self, ctx, *, query: str):
        """
        Searches for quotes by quoted text

        Results are sorted by relevance (uses sqlite FTS4 + Okapi BM25)
        """
        query = query.lstrip()
        records = self._do_search(query, limit=50, server=ctx.message.server, link=True)

        if not self.has_fts:
            await self.bot.say(warning("Missing FTS extension; please contact the bot owner. If you are the owner, see "
                                       "here: <https://sqlite.org/fts3.html#compiling_and_enabling_fts3_and_fts4>"))
            return
        elif not records:
            await self.bot.say("Sorry, no matches.")
            return

        await self.embed_menu(ctx, records, use_snippet=True)

    @quote.command(pass_context=True, no_pm=True, name='show')
    @commands.cooldown(6, 60, commands.BucketType.channel)
    async def quote_show(self, ctx, num: int):
        """
        Displays a stored quote by its number
        """
        records = self._get_quotes(server=ctx.message.server, server_quote_id=num, link=True)

        if not records:
            await self.bot.say(warning("Couldn't find that quote in this server."))
            return

        # If servers are linked, the same server quote ID could have multiple matches
        if len(records) > 1:
            await self.embed_menu(ctx, records)
        else:
            embed = self.format_quote_embed(ctx, records[0])
            await self.bot.say(embed=embed)

    @commands.cooldown(6, 60, commands.BucketType.channel)
    @quote.command(pass_context=True, no_pm=True, name='by')
    async def quote_by(self, ctx, member: discord.Member, show_all: bool = False):
        """
        Displays a random quote by the specified member

        If show_all is a trueish value, page through all quotes by the member
        """
        kwargs = {} if show_all else {'sort_direction': SortDirection.RANDOM, 'limit': 1}
        records = self._get_quotes(server=ctx.message.server, author=member, link=True, **kwargs)

        if not records:
            await self.bot.say(warning("There aren't any quotes by %s yet." % member))
            return

        if len(records) > 1:
            await self.embed_menu(ctx, records)
        else:
            embed = self.format_quote_embed(ctx, records[0])
            await self.bot.say(embed=embed)

    @commands.cooldown(6, 60, commands.BucketType.channel)
    @quote.command(pass_context=True, no_pm=True, name='by-nm')
    async def quote_by_nm(self, ctx, author: str, show_all: bool = False):
        """
        Displays a random quote by the specified (non-member) author

        If show_all is a trueish value, page through all quotes by the author
        """
        kwargs = {} if show_all else {'sort_direction': SortDirection.RANDOM, 'limit': 1}
        records = self._get_quotes(server=ctx.message.server, author_name=author, link=True, **kwargs)

        if not records:
            await self.bot.say(warning("There aren't any quotes by %s yet." % author))
            return

        if len(records) > 1:
            await self.embed_menu(ctx, records)
        else:
            embed = self.format_quote_embed(ctx, records[0])
            await self.bot.say(embed=embed)

    @commands.cooldown(6, 60, commands.BucketType.channel)
    @quote.command(pass_context=True, no_pm=True, name='me', aliases=['myself', 'self'])
    async def quote_self(self, ctx, show_all: bool = False):
        """
        Displays quotes by the member running the command

        If show_all is a trueish value, page through all quotes by the member
        """
        kwargs = {} if show_all else {'sort_direction': SortDirection.RANDOM, 'limit': 1}
        records = self._get_quotes(server=ctx.message.server, author=ctx.message.author, **kwargs, link=True)

        if not records:
            await self.bot.say(warning("There aren't any quotes by you yet."))
            return

        if len(records) > 1:
            await self.embed_menu(ctx, records)
        else:
            embed = self.format_quote_embed(ctx, records[0])
            await self.bot.say(embed=embed)

    @mod_or_permissions(administrator=True)
    @quote.command(pass_context=True, no_pm=True, name='add', rest_is_raw=True)
    async def quote_add(self, ctx, author: discord.Member, *, quote: str):
        """
        Adds a member's quote to the server quote database

        The first argument must be the author's nickname or a mention.
        The rest of the command is interpreted as the quote itself.

        To add a quote from a non-member, use [p]quote add-nm
        Or, to add a quote directly from a message, use [p]quote add-msg .
        """
        if quote is not None:
            quote = quote.lstrip()  # remove whitespace

            # remove quotes but only if symmetric
            if quote.startswith('"') and quote.endswith('"'):
                quote = quote[1:-1]

        if quote or ctx.message.attachments or (ctx.message.embeds and ctx.message.embeds[0].get('type') == 'image'):
            self._update_member(ctx.message.author)
            self._update_member(author)
            ret = self._add_quote(ctx, quote=quote, author=author)
            await self.bot.say(okay("Quote #%i added." % ret['server_quote_id']))
        else:
            await self.bot.say(warning("Cannot add a quote with no text, attachments or embed images."))

    @mod_or_permissions(administrator=True)
    @quote.command(pass_context=True, no_pm=True, name='add-nm', rest_is_raw=True)
    async def quote_add_nm(self, ctx, author: str, *, quote: str = None):
        """
        Adds a quote to the server quote database

        The first argument is the author. If it has spaces, use double quotes.
        The rest of the command is interpreted as the quote itself.

        Quotes added using this command will not be tied to a member.
        To add a quote from a member, use [p]quote add .
        Or, to add a quote directly from a message, use [p]quote add-msg .
        """
        if quote is not None:
            quote = quote.lstrip()  # remove whitespace

            # remove quotes but only if symmetric
            if quote.startswith('"') and quote.endswith('"'):
                quote = quote[1:-1]

        if quote or ctx.message.attachments or (ctx.message.embeds and ctx.message.embeds[0].get('type') == 'image'):
            self._update_member(ctx.message.author)
            ret = self._add_quote(ctx, quote=quote, author_name=author)
            await self.bot.say(okay("Quote #%i added." % ret['server_quote_id']))
        else:
            await self.bot.say(warning("Cannot add a quote with no text, attachments or embed images."))

    @mod_or_permissions(administrator=True)
    @quote.command(pass_context=True, no_pm=True, name='add-msg')
    async def quote_add_msg(self, ctx, message_id: int, channel: discord.Channel = None):
        """
        Adds a message to the server quote database

        The full text of the message is used. If the message belongs to
        another channel, specify it as the second argument.
        """
        try:
            msg = await self.bot.get_message(channel or ctx.message.channel, str(message_id))
        except discord.errors.NotFound:
            await self.bot.say(warning("Couldn't find that message in %s."
                                       % (channel.mention if channel else 'this channel')))
            return

        if msg.content or msg.attachments or (msg.embeds and msg.embeds[0].get('type') == 'image'):
            self._update_member(ctx.message.author)
            self._update_member(msg.author)
            ret = self._add_quote(ctx, message=msg)
            await self.bot.say(okay("Quote #%i added." % ret['server_quote_id']))
        else:
            await self.bot.say(warning("Cannot add a quote with no text, attachments or embed images."))

    @quote.command(pass_context=True, no_pm=True, name='remove', aliases=['rm', 'delete'])
    async def quote_remove(self, ctx, num: int):
        """
        Deletes a quote by its number
        """
        match = self._get_quotes(server=ctx.message.server, server_quote_id=num)

        if not match:
            await self.bot.say(warning("Couldn't find that quote in this server."))
            return
        elif not await self._authorize_del(ctx, match[0]):
            return

        embed = self.format_quote_embed(ctx, match[0])

        if not await self.confirm_thing(ctx, thing="delete this quote", require_yn=True, embed=embed):
            return

        self._delete_quotes(quote_id=match[0]['quote_id'])
        await self.bot.say(okay("Quote #%i deleted.") % num)

    @mod_or_permissions(administrator=True)
    @quote.command(pass_context=True, no_pm=True, name='global')
    async def quote_global(self, ctx, num: int, yes_no: bool = True):
        """
        Sets whether a quote is accessible in all servers
        """
        match = self._get_quotes(server=ctx.message.server, server_quote_id=num)

        if not match:
            await self.bot.say(warning("Couldn't find that quote in this server."))
            return

        quote_id = match[0]['quote_id']

        if yes_no:
            if match[0]['is_global']:
                await self.bot.say(warning("That quote has already been published."))
                return

            embed = self.format_quote_embed(ctx, match[0])

            if not await self.confirm_thing(ctx, thing="make this quote accessible from all servers",
                                            require_yn=True, embed=embed):
                return

            self._update_quotes(quote_id=quote_id, is_global=True)
            await self.bot.say(okay("Quote #%i published as #g%i.") % (num, quote_id))
        else:
            if not match[0]['is_global']:
                await self.bot.say(warning("That quote is already not published."))
                return

            self._update_quotes(quote_id=quote_id, is_global=False)
            await self.bot.say(okay("Quote #%i unpublished.") % num)

    @quote.command(pass_context=True, no_pm=True, name='dump', aliases=['csv'])
    async def quote_dump(self, ctx):
        """
        Uploads all quotes in the server as a CSV
        """
        strbuf = StringIO(newline='')
        fname = 'quotes_%i_%s.csv' % (datetime.now().timestamp(), ctx.message.server.name)

        rows = []

        with self.db as con:
            cols = [r['name'] for r in con.execute("PRAGMA table_info(quotes);").fetchall()]
            cols.remove('quote_id')
            cols += ['display_author', 'display_added_by']
            writer = csv.DictWriter(strbuf, fieldnames=cols, extrasaction='ignore', quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            rows = [dict(row) for row in self._get_quotes(server=ctx.message.server)]

            for row in rows:
                for k in ['date_said', 'date_added']:
                    if row[k]:
                        row[k] = row[k].timestamp()

            writer.writerows(rows)

        buf = BytesIO(b'\xef\xbb\xbf' + strbuf.getvalue().encode())
        buf.seek(0)
        await self.bot.upload(buf, filename=fname)

    @admin_or_permissions(administrator=True)
    @quote.command(pass_context=True, no_pm=True, name='link')
    async def quote_link(self, ctx, server_id: int = None):
        """
        Links to another server to display or search quotes

        If no server ID is given, lists linked servers.
        """
        link_server = self.bot.get_server(str(server_id))
        params = (int(ctx.message.server.id), server_id)

        if server_id is None:
            links = self.db.execute('SELECT to_id FROM server_links WHERE from_id = ?', params[:1]).fetchall()

            if not links:
                await self.bot.say("Not linked to any servers yet.")
            else:
                servers = []
                missing = []

                for row in links:
                    server_id = str(row['to_id'])
                    server = self.bot.get_server(server_id)

                    if server:
                        servers.append(server)
                    else:
                        missing.append(server_id)

            msg = [
                "**Linked to these servers:**",
                '\n'.join(sorted("{0.name} (ID {0.id})".format(s) for s in servers))
            ]

            if missing:
                msg.extend([
                    "\n**And these server IDs that I'm no longer in:"
                    '\n'.join(missing)
                ])

            await self.bot.say('\n'.join(msg))
            return

        if not (link_server and link_server.get_member(ctx.message.author.id)):
            await self.bot.say(error("Either I'm not in that server or you aren't."))
        elif self.db.execute('SELECT * FROM server_links WHERE from_id = ? AND to_id = ?', params).fetchall():
            await self.bot.say(warning("Already linked to %s." % link_server.name))
        else:
            with self.db as con:
                con.execute('INSERT INTO server_links (from_id, to_id) VALUES (?,?)', params)

            await self.bot.say(okay("Now linked to %s." % link_server.name))

    @admin_or_permissions(administrator=True)
    @quote.command(pass_context=True, no_pm=True, name='unlink')
    async def quote_unlink(self, ctx, server_id: int):
        """
        Unlinks a linked server
        """
        link_server = self.bot.get_server(str(server_id))
        params = (int(ctx.message.server.id), server_id)
        disp = link_server.name if link_server else ('server ID %i' % server_id)

        if not self.db.execute('SELECT * FROM server_links WHERE from_id = ? AND to_id = ?', params).fetchall():
            await self.bot.say("Not linked to %s." % disp)
        else:
            self.db.execute('DELETE FROM server_links WHERE from_id = ? AND to_id = ?', params)
            await self.bot.say(okay("Removed link to %s." % disp))

    @commands.group(pass_context=True, invoke_without_command=True)
    async def gquote(self, ctx, *, num_or_member: str = None):
        """
        Show/mange global quotes

        If no valid subcommand is given, attempts to look up a quote by global ID.
        [p]gquote random also works. Without any argument, invokes [p]gquote list.
        [p]gquote help displays this help and all subcommands.
        """
        if num_or_member and num_or_member.strip(" '\"`").lower() == 'random':
            ctx.view = StringView('yes')
            await self.gquote_list.invoke(ctx)
        elif num_or_member and num_or_member.strip(" '\"`").lower() == 'help':
            await self.bot.send_cmd_help(ctx)
        elif num_or_member:
            ctx.view = StringView(num_or_member)

            if num_or_member.isdecimal():
                await self.gquote_show.invoke(ctx)
            else:
                await self.bot.send_cmd_help(ctx)
        else:
            await self.gquote_list.invoke(ctx)

    @commands.cooldown(6, 60, commands.BucketType.channel)
    @gquote.command(pass_context=True, name='list')
    async def gquote_list(self, ctx, jump_to_random: bool = False):
        """
        Allows you to page through a list of all quotes
        """
        records = self._get_quotes(is_global=True)

        if not records:
            await self.bot.say(warning("There are no quotes in this server!"))
            return

        if len(records) > 1:
            page = randrange(len(records)) if jump_to_random else 0
            await self.embed_menu(ctx, records, page=page)
        else:
            embed = self.format_quote_embed(ctx, records[0])
            await self.bot.say(embed=embed)

    @gquote.command(pass_context=True, name='search', rest_is_raw=True)
    @commands.cooldown(6, 60, commands.BucketType.channel)
    async def gquote_search(self, ctx, *, query: str):
        """
        Searches for global quotes by quoted text

        Results are sorted by relevance (uses sqlite FTS4 + Okapi BM25)
        """
        query = query.lstrip()
        records = self._do_search(query, limit=50, is_global=True)

        if not self.has_fts:
            await self.bot.say(warning("Missing FTS extension; please contact the bot owner. If you are the owner, see "
                                       "here: <https://sqlite.org/fts3.html#compiling_and_enabling_fts3_and_fts4>"))
            return
        elif not records:
            await self.bot.say("Sorry, no matches.")
            return

        await self.embed_menu(ctx, records, use_snippet=True)

    @gquote.command(pass_context=True, name='show')
    @commands.cooldown(6, 60, commands.BucketType.channel)
    async def gquote_show(self, ctx, num: int):
        """
        Displays a stored quote by its number
        """
        records = self._get_quotes(quote_id=num, is_global=True)

        if not records:
            await self.bot.say(warning("Couldn't find that quote."))
            return

        embed = self.format_quote_embed(ctx, records[0])
        await self.bot.say(embed=embed)

    @commands.cooldown(6, 60, commands.BucketType.channel)
    @gquote.command(pass_context=True, name='by-nm')
    async def gquote_by_nm(self, ctx, author: str, show_all: bool = False):
        """
        Displays a random global quote by the specified (non-member) author

        If show_all is a trueish value, page through all quotes by the author
        """
        kwargs = {} if show_all else {'sort_direction': SortDirection.RANDOM, 'limit': 1}
        records = self._get_quotes(author_name=author, is_global=True, **kwargs)

        if not records:
            await self.bot.say(warning("There aren't any global quotes by %s." % author))
            return

        if len(records) > 1:
            await self.embed_menu(ctx, records)
        else:
            embed = self.format_quote_embed(ctx, records[0])
            await self.bot.say(embed=embed)

    @commands.cooldown(6, 60, commands.BucketType.channel)
    @gquote.command(pass_context=True, name='me', aliases=['myself', 'self'])
    async def gquote_self(self, ctx, show_all: bool = False):
        """
        Displays global quotes by the specified member

        If show_all is a trueish value, page through all quotes by the member
        """
        kwargs = {} if show_all else {'sort_direction': SortDirection.RANDOM, 'limit': 1}
        records = self._get_quotes(author_id=ctx.message.author.id, is_global=True, **kwargs)

        if not records:
            await self.bot.say(warning("There aren't any global quotes by you yet."))
            return

        embed = self.format_quote_embed(ctx, records[0])
        await self.bot.say(embed=embed)

    @is_owner()
    @gquote.command(pass_context=True, name='add', rest_is_raw=True)
    async def gquote_add(self, ctx, author: discord.Member, *, quote: str):
        """
        Adds a member's quote to the server global quote database

        The first argument must be the author's nickname or a mention.
        The rest of the command is interpreted as the quote itself.

        To add a quote from a non-member, use [p]gquote add-nm
        Or, to add a quote directly from a message, use [p]gquote add-msg .
        """
        if quote is not None:
            quote = quote.lstrip()  # remove whitespace

            # remove quotes but only if symmetric
            if quote.startswith('"') and quote.endswith('"'):
                quote = quote[1:-1]

        if quote or ctx.message.attachments or (ctx.message.embeds and ctx.message.embeds[0].get('type') == 'image'):
            self._update_member(ctx.message.author)
            self._update_member(author)
            ret = self._add_quote(ctx, quote=quote, author=author, is_global=True, server=False)
            await self.bot.say(okay("Global quote #g%i added." % ret['quote_id']))
        else:
            await self.bot.say(warning("Cannot add a quote with no text, attachments or embed images."))

    @is_owner()
    @gquote.command(pass_context=True, name='add-nm', rest_is_raw=True)
    async def gquote_add_nm(self, ctx, author: str, *, quote: str = None):
        """
        Adds a quote to the server global quote database

        The first argument is the author. If it has spaces, use double quotes.
        The rest of the command is interpreted as the quote itself.

        Quotes added using this command will not be tied to a member.
        To add a quote from a member, use [p]quote add .
        Or, to add a quote directly from a message, use [p]quote add-msg .
        """
        if quote is not None:
            quote = quote.lstrip()  # remove whitespace

            # remove quotes but only if symmetric
            if quote.startswith('"') and quote.endswith('"'):
                quote = quote[1:-1]

        if quote or ctx.message.attachments or (ctx.message.embeds and ctx.message.embeds[0].get('type') == 'image'):
            self._update_member(ctx.message.author)
            ret = self._add_quote(ctx, quote=quote, author_name=author, is_global=True, server=False)
            await self.bot.say(okay("Global quote #g%i added." % ret['quote_id']))
        else:
            await self.bot.say(warning("Cannot add a quote with no text, attachments or embed images."))

    @is_owner()
    @gquote.command(pass_context=True, name='add-msg')
    async def gquote_add_msg(self, ctx, message_id: int, channel: discord.Channel = None):
        """
        Adds a message to the server global quote database

        The full text of the message is used. If the message belongs to
        another channel, specify it as the second argument.
        """
        try:
            msg = await self.bot.get_message(channel or ctx.message.channel, str(message_id))
        except discord.errors.NotFound:
            await self.bot.say(warning("Couldn't find that message in %s."
                                       % (channel.mention if channel else 'this channel')))
            return

        if msg.content or msg.attachments or (msg.embeds and msg.embeds[0].get('type') == 'image'):
            self._update_member(ctx.message.author)
            self._update_member(msg.author)
            ret = self._add_quote(ctx, message=msg, is_global=True, server=False)
            await self.bot.say(okay("Global quote #g%i added." % ret['quote_id']))
        else:
            await self.bot.say(warning("Cannot add a quote with no text, attachments or embed images."))

    @is_owner()
    @gquote.command(pass_context=True, name='remove', aliases=['rm', 'delete'])
    async def gquote_remove(self, ctx, num: int):
        """
        Deletes a quote by its number
        """
        match = self._get_quotes(quote_id=num, is_global=True)

        if not match:
            await self.bot.say(warning("Couldn't find that quote."))
            return

        embed = self.format_quote_embed(ctx, match[0])

        if not await self.confirm_thing(ctx, thing="delete this quote", require_yn=True, embed=embed):
            return

        self._delete_quotes(quote_id=match[0]['quote_id'])
        await self.bot.say(okay("Global quote #%i deleted.") % num)

    @is_owner()
    @gquote.command(pass_context=True, name='unpublish')
    async def gquote_unpublish(self, ctx, num: int):
        """
        Unpublishes a global quote
        """
        match = self._get_quotes(quote_id=num, is_global=True)

        if not match:
            await self.bot.say(warning("Couldn't find that quote."))
            return
        elif not match[0]['server_id']:
            await self.bot.say(error("That quote cannot be unpublished because it isn't from a server."))
            return

        embed = self.format_quote_embed(ctx, match[0])

        if not await self.confirm_thing(ctx, thing="unpublish this quote", require_yn=True, embed=embed):
            return

        self._update_quotes(quote_id=num, is_global=False)
        await self.bot.say(okay("Global quote #%i unpublished.") % num)

    # Legacy command stubs

    @commands.command(pass_context=True, no_pm=True)
    async def lsquotes(self, ctx):
        await self.bot.say("This command is deprecated; use `%squote list` instead.\n\n"
                           "This notice will be removed in a future release." % ctx.prefix)

    @commands.command(pass_context=True, no_pm=True)
    async def rmquote(self, ctx):
        await self.bot.say("This command is deprecated; use `%squote remove <num>` instead.\n\n"
                           "This notice will be removed in a future release." % ctx.prefix)

    @commands.command(pass_context=True, no_pm=True)
    async def addquote(self, ctx):
        await self.bot.say("This command is deprecated; use `%squote add <member> <quote ...>` instead.\n\n"
                           "This notice will be removed in a future release." % ctx.prefix)

    # Utility

    def format_quote_embed(self, ctx, record, extra=None, use_snippet=False) -> discord.Embed:
        timestamp = record['date_said'] or record['date_added'] or discord.Embed.Empty
        description = (record['snippet'] if use_snippet else record['quote']) or discord.Embed.Empty
        same_server = ctx.message.server and int(ctx.message.server.id) == record['server_id']
        server = self.bot.get_server(str(record['server_id']))

        embed = discord.Embed(description=description, timestamp=timestamp)

        if same_server:
            quote_no = 'quote #%i' % record['server_quote_id']
            display_author = record['display_author']

            if record['is_global']:
                quote_no += ' (#g%i)' % record['quote_id']
        else:
            if record['is_global']:
                quote_no = 'quote #g%i' % record['quote_id']
            else:
                quote_no = 'linked quote #%i' % record['server_quote_id']

            display_author = record['global_author']

            if server:
                display_author += ' in ' + server.name

        footer = (extra + ' | ' + quote_no) if extra else quote_no.capitalize()

        if same_server and record['display_added_by']:
            footer += ' | added by ' + record['display_added_by']
        elif not same_server and record['global_added_by']:
            footer += ' | added by ' + record['global_added_by']

        embed.set_footer(text=footer, icon_url=record['added_by_avatar_url'] or discord.Embed.Empty)
        embed.set_author(name='By: ' + display_author)

        if record['author_avatar_url']:
            embed.set_thumbnail(url=record['author_avatar_url'])

        if record['image_url']:
            embed.set_image(url=record['image_url'])

        if record['attachment_url']:
            embed.add_field(name='Attachment', inline=False,
                            value='[{}]({})'.format(record['attachment_filename'], record['attachment_url']))

        return embed

    async def embed_menu(self, ctx, records: list, message: discord.Message = None,
                         page=0, timeout: int = 30, edata=None, use_snippet=None):
        """
        menu control logic for this taken from
        https://github.com/Lunar-Dust/Dusty-Cogs/blob/master/menu/menu.py
        """

        num_records = len(records)
        record = records[page]
        content = 'Result %i/%i:' % (page + 1, num_records)
        embed = self.format_quote_embed(ctx, record, use_snippet=use_snippet)

        expected = ["➡", "⬅", "❌", "⏩", "⏪", "🎲", "🔍"]

        if not message:
            message = await self.bot.send_message(ctx.message.channel, content, embed=embed)

            if num_records > 10:
                await self.bot.add_reaction(message, "⏪")

            if num_records > 1:
                await self.bot.add_reaction(message, "⬅")

            await self.bot.add_reaction(message, "❌")

            if use_snippet is not None:
                await self.bot.add_reaction(message, "🔍")

            if num_records > 1:
                await self.bot.add_reaction(message, "🎲")
                await self.bot.add_reaction(message, "➡")

            if num_records > 10:
                await self.bot.add_reaction(message, "⏩")

        else:
            message = await self.bot.edit_message(message, content, embed=embed)

        react = await self.bot.wait_for_reaction(message=message, user=ctx.message.author,
                                                 timeout=timeout, emoji=expected)
        if react is None:
            try:
                try:
                    await self.bot.clear_reactions(message)
                except Exception:
                    if num_records > 10:
                        await self.bot.remove_reaction(message, "⏪", self.bot.user)

                    if num_records > 1:
                        await self.bot.remove_reaction(message, "⬅", self.bot.user)

                    await self.bot.remove_reaction(message, "❌", self.bot.user)

                    if use_snippet is not None:
                        await self.bot.remove_reaction(message, "🔍", self.bot.user)

                    if num_records > 1:
                        await self.bot.remove_reaction(message, "🎲", self.bot.user)
                        await self.bot.remove_reaction(message, "➡", self.bot.user)

                    if num_records > 10:
                        await self.bot.remove_reaction(message, "⏩", self.bot.user)
            except Exception:
                pass

            return None

        reacts = {v: k for k, v in numbs.items()}
        action = reacts[react.reaction.emoji]

        if action == "back_10":
            page -= 10
        elif action == "back":
            page -= 1
        elif action == "random":
            page += randrange(num_records - 1) + 1
        elif action == "show":
            use_snippet = not use_snippet
        elif action == "next":
            page += 1
        elif action == "next_10":
            page += 10
        else:
            try:
                return await self.bot.delete_message(message)
            except Exception:
                pass

        try:
            await self.bot.remove_reaction(message, react.reaction.emoji, ctx.message.author)
        except Exception:
            pass

        next_page = page % num_records

        return await self.embed_menu(ctx, records, message=message, page=next_page, timeout=timeout,
                                     edata=edata, use_snippet=use_snippet)

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

    # Based on code from red core mod.py
    def is_mod_or_superior(self, obj, admin_only=False):
        if not isinstance(obj, (discord.Message, discord.Member, discord.Role)):
            raise TypeError('Only messages, members or roles may be passed')

        server = obj.server
        admin_role = self.bot.settings.get_server_admin(server).lower()
        mod_role = self.bot.settings.get_server_mod(server).lower()

        if isinstance(obj, discord.Role):
            if admin_only:
                return obj.name.lower() == admin_role
            else:
                return obj.name.lower() in [admin_role, mod_role]
        elif isinstance(obj, discord.Message):
            user = obj.author
        elif isinstance(obj, discord.Member):
            user = obj
        else:
            return False

        check_roles = {r.name for r in user.roles}

        if user.id == self.bot.settings.owner:
            return True
        elif user == server.owner:
            return True
        elif admin_role in check_roles:
            return True
        elif (not admin_only) and mod_role in check_roles:
            return True

        return False

    # Event listeners

    async def on_member_update(self, before, after):
        if (before.nick != after.nick or before.name != after.name or
                before.discriminator != after.discriminator or before.avatar != after.avatar):
            self._update_member(after, update_only=True)

    async def on_command(self, command, ctx):
        if ctx.cog is self and self.analytics:
            self.analytics.command(ctx)


def check_folder():
    if not os.path.exists(PATH):
        print("Creating serverquotes folder...")
        os.makedirs(PATH)


def check_file():
    if dataIO.is_valid_json(JSON):
        print("Migrating quotes.json...")
        data = dataIO.load_json(JSON)
        db = sqlite3.connect(SQLDB)
        rows = []

        db.executescript(INIT_SQL)

        for sid, sdata in data.items():
            for entry in sdata:
                rows.append((sid, entry['added_by'], entry['author_id'], entry['author_name'], entry['text']))
        with db:
            db.executemany("INSERT INTO quotes"
                           "(server_id, added_by, author_id, author_name, quote, date_said, date_added, migrated) "
                           "VALUES (?, ?, ?, ?, ?, NULL, NULL, 1)", rows)

        os.rename(JSON, JSON.replace('.', '_migrated.'))


def setup(bot):
    check_folder()
    check_file()
    n = ServerQuotes(bot)
    bot.add_cog(n)
