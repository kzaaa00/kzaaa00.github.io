# kzaaa00.github.io

トップページ（ゲーム一覧）: `index.html`。ゲームを足したら `index.html` の一覧にも1枚足す（ai-tegara-binta・ronten-binta・potechi は一覧に出さない）。
各ゲームには `_parts/moregames.html`（タイトル画面の左上「‹ 他のゲーム」と結果画面の「ほかのゲームで遊ぶ」）を `</body>` の直前に貼る。
各ゲームのタイトル画面の下には「遊び方・うまくいくコツ・このゲームについて」の文章を入れる（AdSense の審査で「中身のない画面」と判断されないため）。
文章は `_tools/guides_ja.py`（英語版は `_tools/guides_en.py`）に1本ずつ書いて、`python3 _tools/guide.py` を実行するとページに入る（何度実行しても同じ）。新しいゲームを足したら、ここにも足して実行する。英語版を build_en.py で作り直したあとも実行する。
AdSense のタグ（head の adsbygoogle.js）は、文章のあるページだけに入れる（omakase・ads/frame.html・広告なしのゲームには入れない）。`sitemap.xml` にもページを足す。
ほかに `about/`（このサイトについて・お問い合わせ）と `privacy/`（プライバシーポリシー）。

- [ai-tegara-binta](https://tapitta.com/ai-tegara-binta/)
- [kidoku](https://tapitta.com/kidoku/)
- [yugiri](https://tapitta.com/yugiri/)
- [renji](https://tapitta.com/renji/)
- [omakase](https://tapitta.com/omakase/)
- [shotoku](https://tapitta.com/shotoku/)
- [natto](https://tapitta.com/natto/)
- [jidoudoa](https://tapitta.com/jidoudoa/)
- [tape](https://tapitta.com/tape/)
- [tamago](https://tapitta.com/tamago/)
- [hanketsu](https://tapitta.com/hanketsu/)
- [label](https://tapitta.com/label/)
- [tsurikawa](https://tapitta.com/tsurikawa/)
- [hamigaki](https://tapitta.com/hamigaki/)
- [onigiri](https://tapitta.com/onigiri/)
- [kaisatsu](https://tapitta.com/kaisatsu/)
- [koppu](https://tapitta.com/koppu/)
- [potechi](https://tapitta.com/potechi/)
- [penguin](https://tapitta.com/penguin/)
- [orca](https://tapitta.com/orca/)
- [yuuhi](https://tapitta.com/yuuhi/)
- [ketchup](https://tapitta.com/ketchup/)
- [nenrei](https://tapitta.com/nenrei/)
- [tissue](https://tapitta.com/tissue/)
- [kakinotane](https://tapitta.com/kakinotane/)
- [shampoo](https://tapitta.com/shampoo/)
- [mochi](https://tapitta.com/mochi/)
- [nemurineko](https://tapitta.com/nemurineko/)
- [strawbukuro](https://tapitta.com/strawbukuro/)
- [curtain](https://tapitta.com/curtain/)
- [nekoball](https://tapitta.com/nekoball/)

## 英語版（/en/）

海外向けの英語版は `en/` 以下（https://tapitta.com/en/）。一覧 `en/index.html`、`en/about/`、`en/privacy/`。
各ゲームの `en/<slug>/index.html` は日本語版から自動で作る（手で直さない）。作り方と文言は共有フォルダの `x-posts/game/en/`:
`python3 build_en.py <このリポジトリ>` で日本語版の index.html に英語の文言（`strings_<slug>.py`）を当てて書き出す。日本語版を直したら作り直す。
広告は `ads/ads.js` の `SLOTS_EN`（今は日本語版と同じ枠）。

- [ketchup](https://tapitta.com/en/ketchup/)（日本語版 ketchup）
- [label](https://tapitta.com/en/label/)（日本語版 label）
- [tape](https://tapitta.com/en/tape/)（日本語版 tape）
- [egg](https://tapitta.com/en/egg/)（日本語版 tamago）
