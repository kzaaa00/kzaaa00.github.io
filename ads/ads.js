/* tapitta の広告枠（全ページ共通）。
   広告会社を変えるときは、下の SLOTS だけ直せばよい（ゲームの HTML は触らない）。
   - result: ゲームの結果画面、「ほかのゲームで遊ぶ」の下
   - list:   一覧ページ、6本目のあと
   各枠の値:
     null                                    … 広告なし
     {type:'admax',   id:'忍者AdMaxの広告枠ID'}
     {type:'imobile', pid:1, mid:2, asid:3}   … i-mobile の広告スポット
     {type:'adsense', slot:'AdSenseの広告ユニットID'}
     [ {...}, {...} ]                         … 配列なら表示のたびにどれか1つ（併用・比較用）
   遊んでいる最中は出さない。結果画面が開くたびに読み込み直す（AdMax のみ。AdSense は最初の1回だけ）。 */
(function () {
  var SLOTS = {
    result: { type: 'admax', id: 'eb89faf517e68b4d7d00f6f53c60414c' },  // 忍者AdMax「tapitta結果画面」
    list:   { type: 'admax', id: '5c6f97434182620655874aee677c16c6' }   // 忍者AdMax「tapitta一覧ページ」
  };
  var ADSENSE_CLIENT = 'ca-pub-2540616238933875';
  var NO_ADS = /\/(ai-tegara-binta|ronten-binta|potechi)\//;

  // アクセス計測（GoatCounter、Cookieなし）。ページ表示と、広告の表示・タップの目安を数える。
  var GC = 'https://tapitta.goatcounter.com/count';
  var gcQueue = [];
  function track(name) {
    var ev = { path: name, title: location.pathname, event: true };
    if (window.goatcounter && window.goatcounter.count) window.goatcounter.count(ev); else gcQueue.push(ev);
  }
  (function () {
    if (!/tapitta\.com$/.test(location.hostname)) return;   // 手元での確認は数えない
    var sc = document.createElement('script');
    sc.async = true; sc.src = 'https://gc.zgo.at/count.js'; sc.setAttribute('data-goatcounter', GC);
    sc.onload = function () {
      var t = setInterval(function () {
        if (!window.goatcounter || !window.goatcounter.count) return;
        clearInterval(t);
        while (gcQueue.length) window.goatcounter.count(gcQueue.shift());
      }, 200);
    };
    document.head.appendChild(sc);
  })();
  // 広告の中（別サイトの枠）をタップしてページから離れたら「タップの目安」として数える
  window.addEventListener('blur', function () {
    setTimeout(function () {
      var a = document.activeElement;
      if (a && a.tagName === 'IFRAME') {
        var w = a.closest && a.closest('.tpAd');
        if (w) track('ad-tap-' + w.getAttribute('data-slot'));
      }
    }, 0);
  });

  if (NO_ADS.test(location.pathname)) return;

  function pick(v) { return Array.isArray(v) ? v[Math.floor(Math.random() * v.length)] : v; }

  function style() {
    if (document.getElementById('tpAdStyle')) return;
    var s = document.createElement('style'); s.id = 'tpAdStyle';
    s.textContent = '.tpAd{margin:28px auto 8px;text-align:center;width:100%;max-width:336px}' +
      '.tpAd small{display:block;font-size:10px;letter-spacing:.1em;color:#8a8f99;margin-bottom:4px}' +
      '.tpAd .tpAdBox{min-height:250px;display:flex;align-items:center;justify-content:center}';
    document.head.appendChild(s);
  }

  function load(src) {
    if (document.querySelector('script[src="' + src + '"]')) return;
    var sc = document.createElement('script'); sc.async = true; sc.src = src; sc.charset = 'utf-8';
    document.head.appendChild(sc);
  }

  // 広告を1つ描く。refresh=true の枠は、呼ぶたびに中身を新しい広告に入れ替える。
  function render(host, cfg, name) {
    cfg = pick(cfg);
    if (!cfg || !host) return;
    style();
    var wrap = host.querySelector('.tpAd');
    if (wrap) {
      if (!canRefresh(cfg)) return;          // AdSense は勝手に入れ替えない
      wrap.lastChild.innerHTML = '';
    } else {
      wrap = document.createElement('div'); wrap.className = 'tpAd'; wrap.setAttribute('data-slot', name);
      wrap.innerHTML = '<small>広告</small><div class="tpAdBox"></div>';
      host.appendChild(wrap);
    }
    track('ad-show-' + name);
    var box = wrap.lastChild;
    if (cfg.type === 'admax') {
      // 小窓（同じサイトのページ）の中で読み込むので、毎回まっさらな広告になる
      var f = document.createElement('iframe');
      f.src = '/ads/frame.html?admax=' + cfg.id;
      f.title = '広告'; f.width = 300; f.height = 250; f.scrolling = 'no'; f.loading = 'eager';
      f.style.cssText = 'border:0;display:block;width:300px;height:250px;overflow:hidden';
      box.appendChild(f);
    } else if (cfg.type === 'imobile') {
      var id = 'im-' + cfg.asid + '-' + name;
      var i = document.createElement('div'); i.id = id; box.appendChild(i);
      (window.adsbyimobile = window.adsbyimobile || []).push({ pid: cfg.pid, mid: cfg.mid, asid: cfg.asid, type: 'banner', display: 'inline', elementid: id });
      load('https://imp-adedge.i-mobile.co.jp/script/v1/spot.js?20220104');
    } else if (cfg.type === 'adsense') {
      var a = document.createElement('ins');
      a.className = 'adsbygoogle'; a.style.cssText = 'display:inline-block;width:300px;height:250px';
      a.setAttribute('data-ad-client', ADSENSE_CLIENT); a.setAttribute('data-ad-slot', cfg.slot);
      box.appendChild(a);
      load('https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ADSENSE_CLIENT);
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    }
  }
  function canRefresh(cfg) { return cfg.type === 'admax'; }

  function init() {
    // 一覧ページ
    var list = document.getElementById('adList');
    if (list) render(list, SLOTS.list, 'list');
    // ゲームの結果画面：開くたびに広告を読み直す（遊び直すと新しい広告）
    var result = document.getElementById('result');
    var btns = result && result.querySelector('.btns');
    if (!btns || !SLOTS.result) return;
    var host = null, shown = false;
    function check() {
      if (result.hidden) { shown = false; return; }
      if (shown) return;
      shown = true;
      if (!host) {
        host = document.createElement('div');
        btns.parentNode.insertBefore(host, btns.nextSibling);
      }
      render(host, SLOTS.result, 'result');
    }
    new MutationObserver(check).observe(result, { attributes: true, attributeFilter: ['hidden'] });
    check();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
