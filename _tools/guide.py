#!/usr/bin/env python3
"""各ゲームのタイトル画面の下に「遊び方・コツ・このゲームについて」の文章を入れる。

usage: python3 _tools/guide.py [repo_dir]
  文章は _tools/guides_ja.py（日本語版 <slug>/）と _tools/guides_en.py（英語版 en/<slug>/）。
  何度実行しても同じ結果になる（前に入れたものを外してから入れ直す）。
  文章のないゲームは何もしない。英語版を build_en.py で作り直したあとも、これをもう一度実行する。

AdSense の審査（「パブリッシャーのコンテンツを含まない画面」）対策。
タイトル画面は今までどおり1画面目に出て、下へスクロールすると文章が読める。遊んでいる最中は出ない。
"""
import os, re, sys, html, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))

LABEL = {
    'ja': dict(hint='▼ 遊び方とコツ', play='遊び方', tips='うまくいくコツ', about='このゲームについて',
               nav=[('/', 'ほかのゲームを見る'), ('/about/', 'このサイトについて')], aria='遊び方と解説'),
    'en': dict(hint='▼ How to play & tips', play='How to play', tips='Tips', about='About this game',
               nav=[('/en/', 'More games'), ('/en/about/', 'About tapitta')], aria='How to play and notes'),
}

CSS = '''<!--tpGuideCss:v1--><style>
#title.tpG{justify-content:flex-start;overflow-y:auto;overflow-x:hidden;touch-action:pan-y;overscroll-behavior:contain;-webkit-overflow-scrolling:touch}
#title.tpG>.tpHero{flex:0 0 auto;width:100%;min-height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;padding-bottom:40px;box-sizing:border-box}
#title .tpHint{position:absolute;left:50%;bottom:0;transform:translateX(-50%);font:700 12px/1.4 "Zen Maru Gothic","Hiragino Sans","Yu Gothic","Meiryo",sans-serif;color:inherit;opacity:.8;text-decoration:none;white-space:nowrap;padding:8px 12px}
#title .tpGuide{flex:0 0 auto;width:min(100%,420px);box-sizing:border-box;margin:12px auto 28px;padding:18px 18px 14px;background:#fffdf8;color:#2a2622;border-radius:14px;box-shadow:0 2px 14px rgba(0,0,0,.2);text-align:left;font:500 14px/1.85 "Zen Maru Gothic","Hiragino Sans","Yu Gothic","Meiryo",sans-serif;letter-spacing:0;-webkit-user-select:text;user-select:text;text-shadow:none}
#title .tpGuide h2{font:900 15px/1.5 "Zen Maru Gothic","Hiragino Sans","Yu Gothic","Meiryo",sans-serif;color:#2a2622;margin:18px 0 6px;padding:0 0 4px;border:0;border-bottom:2px solid #e8dfd2;text-align:left;letter-spacing:0;text-transform:none}
#title .tpGuide h2:first-child{margin-top:0}
#title .tpGuide p,#title .tpGuide li{font-size:14px;line-height:1.85;color:#2a2622;margin:0 0 8px;opacity:1;font-weight:500}
#title .tpGuide ol,#title .tpGuide ul{margin:0 0 8px;padding:0 0 0 1.4em}
#title .tpGuide .tpNav{display:flex;flex-wrap:wrap;gap:6px 16px;margin:14px 0 2px;font-size:13px}
#title .tpGuide a{color:#b3261e;font-weight:700;text-decoration:underline}
</style><!--/tpGuideCss-->'''

RESET = ('<script>(function(){var t=document.getElementById("title");if(!t)return;'
         'new MutationObserver(function(){if(!t.hidden)t.scrollTop=0;}).observe(t,{attributes:true,attributeFilter:["hidden"]});})();</script>')


def esc(s):
    return html.escape(s, quote=False)


def guide_html(lang, g):
    L = LABEL[lang]
    out = [f'<!--tpGuide--><section class="tpGuide" id="tpGuide" aria-label="{L["aria"]}">']
    out.append(f'<h2>{L["play"]}</h2><ol>' + ''.join(f'<li>{esc(x)}</li>' for x in g['play']) + '</ol>')
    out.append(f'<h2>{L["tips"]}</h2><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in g['tips']) + '</ul>')
    out.append(f'<h2>{L["about"]}</h2>' + ''.join(f'<p>{esc(x)}</p>' for x in g['about']))
    out.append('<p class="tpNav">' + ''.join(f'<a href="{h}">{esc(t)}</a>' for h, t in L['nav']) + '</p>')
    out.append('</section>' + RESET + '<!--/tpGuide-->')
    return ''.join(out)


def strip(s):
    """前に入れたものを全部外す（元のページに戻す）。"""
    s = re.sub(r'<!--tpGuideCss:v\d+-->.*?<!--/tpGuideCss-->\n?', '', s, flags=re.S)
    s = re.sub(r'<!--tpGuide-->.*?<!--/tpGuide-->', '', s, flags=re.S)
    s = re.sub(r'<!--tpHint-->.*?<!--/tpHero-->', '', s, flags=re.S)
    s = s.replace('<!--tpHero--><div class="tpHero">', '')
    s = s.replace('<div id="title" class="panel tpG">', '<div id="title" class="panel">')
    return s


def title_span(s):
    """<div id="title" class="panel"> の中身の範囲 (start, end) を返す。"""
    m = re.search(r'<div id="title" class="panel">', s)
    if not m:
        return None
    i, depth = m.end(), 1
    for t in re.finditer(r'<(/?)div\b[^>]*>', s[i:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return m.start(), i, i + t.start()
    raise ValueError('title panel not closed')


def apply(s, lang, g):
    s = strip(s)
    if not g:
        return s
    sp = title_span(s)
    if not sp:
        raise ValueError('no #title panel')
    open_at, a, b = sp
    inner = s[a:b]
    hint = f'<!--tpHint--><a class="tpHint" href="#tpGuide">{LABEL[lang]["hint"]}</a></div><!--/tpHero-->'
    new = ('<div id="title" class="panel tpG"><!--tpHero--><div class="tpHero">' + inner.rstrip() + '\n    '
           + hint + '\n    ' + guide_html(lang, g) + '\n  ')
    s = s[:open_at] + new + s[b:]
    s = s.replace('</head>', CSS + '\n</head>', 1)
    return s


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.G


def main(repo):
    for lang, data, base in (('ja', load('guides_ja'), ''), ('en', load('guides_en'), 'en')):
        for slug, g in data.items():
            p = os.path.join(repo, base, slug, 'index.html')
            src = open(p, encoding='utf-8').read()
            out = apply(src, lang, g)
            if out != src:
                open(p, 'w', encoding='utf-8').write(out)
                print('updated', os.path.relpath(p, repo))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE))
