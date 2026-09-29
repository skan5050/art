"""Компиляция .po в .mo без GNU gettext (достаточно для переводов проекта).

    python tools/compile_po.py locale/ru/LC_MESSAGES/django.po
"""
import ast
import struct
import sys
from pathlib import Path


def parse(text):
    entries, cur, key = [], {}, None
    for raw in text.splitlines() + [""]:
        line = raw.strip()
        if not line or line.startswith("#"):
            if cur:
                entries.append(cur)
                cur, key = {}, None
            continue
        if line.startswith('"'):
            cur[key] += ast.literal_eval(line)
            continue
        name, _, value = line.partition(" ")
        key = name
        cur[key] = ast.literal_eval(value)
    return entries


def compile_mo(po_path):
    messages = {}
    for e in parse(Path(po_path).read_text(encoding="utf-8")):
        if "msgid_plural" in e:
            forms = [e[k] for k in sorted(k for k in e if k.startswith("msgstr["))]
            messages[e["msgid"] + "\0" + e["msgid_plural"]] = "\0".join(forms)
        else:
            messages[e["msgid"]] = e.get("msgstr", "")
    keys = sorted(messages)
    ids = b"".join(k.encode() + b"\0" for k in keys)
    strs = b"".join(messages[k].encode() + b"\0" for k in keys)
    n = len(keys)
    offsets, pos_id, pos_str = [], 0, 0
    for k in keys:
        kb, vb = k.encode(), messages[k].encode()
        offsets.append((len(kb), pos_id, len(vb), pos_str))
        pos_id += len(kb) + 1
        pos_str += len(vb) + 1
    header_size = 7 * 4
    ids_start = header_size + n * 16
    strs_start = ids_start + len(ids)
    out = struct.pack("Iiiiiii", 0x950412DE, 0, n, header_size, header_size + n * 8, 0, 0)
    out += b"".join(struct.pack("ii", ln, ids_start + off) for ln, off, _, _ in offsets)
    out += b"".join(struct.pack("ii", ln, strs_start + off) for _, _, ln, off in offsets)
    out += ids + strs
    mo = Path(po_path).with_suffix(".mo")
    mo.write_bytes(out)
    return mo, n


if __name__ == "__main__":
    for path in sys.argv[1:]:
        mo, n = compile_mo(path)
        print(f"{mo}: {n} строк")
