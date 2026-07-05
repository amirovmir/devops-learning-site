# -*- coding: utf-8 -*-
"""Чинит типовые ошибки JSON от генераторов: неэкранированные кавычки,
невалидные \escape, управляющие символы."""
import json, glob, re, sys

VALID_ESC = set('"\\/bfnrtu')

def repair(text):
    out = []
    i, n = 0, len(text)
    in_str = False
    while i < n:
        c = text[i]
        if not in_str:
            if c == '"':
                in_str = True
            out.append(c)
            i += 1
            continue
        # inside string
        if c == '\\':
            nxt = text[i+1] if i+1 < n else ''
            if nxt in VALID_ESC:
                out.append(c); out.append(nxt); i += 2
            else:
                out.append('\\\\'); i += 1
            continue
        if c == '"':
            # закрывающая или внутренняя? смотрим следующий значимый символ
            j = i + 1
            while j < n and text[j] in ' \t':
                j += 1
            nxt = text[j] if j < n else ''
            if nxt in ',:}]' or (nxt == '\n' or nxt == '\r'):
                # проверим случай "\n  \"key\":" — после переноса строки
                if nxt in '\r\n':
                    k = j
                    while k < n and text[k] in '\r\n \t':
                        k += 1
                    nxt2 = text[k] if k < n else ''
                    if nxt2 in ',}]"' or nxt2 == '':
                        in_str = False
                        out.append(c); i += 1; continue
                    else:
                        out.append('\\"'); i += 1; continue
                in_str = False
                out.append(c); i += 1; continue
            else:
                out.append('\\"'); i += 1; continue
        if ord(c) < 0x20:
            out.append({'\n':'\\n','\t':'\\t','\r':'\\r'}.get(c, ''))
            i += 1
            continue
        out.append(c); i += 1
    return ''.join(out)

fixed, failed = [], []
for p in sorted(glob.glob('devops-learning-site/data/section_*.json')):
    raw = open(p, encoding='utf-8').read()
    try:
        json.loads(raw)
        continue
    except Exception:
        pass
    r = repair(raw)
    try:
        obj = json.loads(r)
        open(p, 'w', encoding='utf-8').write(json.dumps(obj, ensure_ascii=False, indent=1))
        fixed.append(p)
    except Exception as e:
        failed.append((p, str(e)))

print('fixed:', len(fixed))
for f in failed:
    print('FAILED:', f)
