#!/usr/bin/env python3

import base64
import sys
import zlib

base = '''import zlib, base64
exec(zlib.decompress(base64.b85decode("""%s""".replace("\\n", ""))))'''

code_str = sys.stdin.read()
b85 = base64.b85encode(zlib.compress(code_str.encode(), 9))
print(base % b85.decode())
