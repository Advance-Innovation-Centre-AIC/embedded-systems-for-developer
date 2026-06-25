#!/usr/bin/env python3
"""Turn every inline `practise_codes/<file>.py` mention in the session decks into
a clickable link that opens the exact file on GitHub in a new tab (with a ↗ icon).

- Only touches inline <code> (Marp renders fenced code blocks as
  <code class="language-...">, which this regex does NOT match — so code inside
  ``` blocks is left alone).
- Skips any path whose file does not actually exist in <course>/practise_codes/
  (no broken links).
- Supports an optional line range, e.g. practise_codes/flappy_step3.py:60-69 ->
  GitHub #L60-L69 anchor.
- Idempotent: a file already containing 'pc-gh-link' is skipped, so it is safe to
  re-run after re-rendering the Marp decks.
Run from anywhere; resolves paths relative to the repo root (parent of tools/)."""
import re, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-developer/blob/main"
COURSES = ["developer-i", "developer-ii"]
ICON = '<sup style="color:#22d3ee;font-weight:800">&#8599;</sup>'  # ↗ open-in-new-tab

# practise_codes/<name>.py  with optional :start  or :start-end (hyphen or en-dash)
PAT = re.compile(r'<code>(practise_codes/([A-Za-z0-9_]+\.py)(?::(\d+)(?:[-–](\d+))?)?)</code>')

total = 0
for course in COURSES:
    cdir = os.path.join(ROOT, course)
    pc = os.path.join(cdir, 'practise_codes')
    have = {os.path.basename(p) for p in glob.glob(os.path.join(pc, '*.py'))}
    for f in sorted(glob.glob(os.path.join(cdir, 'session-*.html'))):
        html = open(f, encoding='utf-8').read()
        if 'pc-gh-link' in html:        # idempotent guard
            continue
        n = [0]

        def repl(m):
            full, fname, ls, le = m.group(1), m.group(2), m.group(3), m.group(4)
            filepart = full.split(':', 1)[0]            # drop any :line-range
            if fname not in have:                       # no broken links
                return m.group(0)
            href = '%s/%s/%s' % (REPO, course, filepart)
            if ls:
                href += '#L' + ls + ('-L' + le if le else '')
            n[0] += 1
            return ('<a class="pc-gh-link" href="%s" target="_blank" rel="noopener" '
                    'title="เปิดไฟล์บน GitHub (แท็บใหม่)" style="text-decoration:none">'
                    '<code>%s</code>%s</a>' % (href, full, ICON))

        new = PAT.sub(repl, html)
        if n[0]:
            open(f, 'w', encoding='utf-8').write(new)
            total += n[0]
            print('  %-28s +%d links' % (os.path.basename(f), n[0]))
print('practise_codes -> GitHub links added:', total)
