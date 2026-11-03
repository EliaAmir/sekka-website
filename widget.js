/*! Sekka "how to reach us" card. No dependencies. Usage:
 *  <script src="https://sekka-eg.com/widget.js" data-name="..." data-address="..." data-station="..." data-lang="ar" async></script>
 *  data-station and data-lang are optional (language falls back to the page's <html lang>, then Arabic).
 *  The card lives in a Shadow DOM, so the host page's CSS cannot break it (font and colours are set on the card itself, sizes are in em). Everything is set with textContent: no HTML injection. */
(function () {
  var s = document.currentScript;
  if (!s || s.getAttribute('data-sekka-done') || !s.parentNode || !Element.prototype.attachShadow) return;
  s.setAttribute('data-sekka-done', '1');

  // keep in sync with src/config.ts (tests/widget.test.ts checks)
  var APP = 'https://apps.apple.com/us/app/sekka-%D8%B3%D9%83%D8%A9-%D9%85%D9%88%D8%A7%D8%B5%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D9%82%D8%A7%D9%87%D8%B1%D8%A9/id6812336357';
  var PLAY = 'https://play.google.com/store/apps/details?id=com.sekka.transport&hl=ar&pli=1';

  var TXT = {
    ar: { h: 'ازاي توصلنا بالمواصلات العامة', st: 'أقرب محطة مترو', go: 'خطّط مشوارك على سكّة، مجانًا', ios: 'حمّل من App Store', and: 'حمّل من Google Play', lbl: 'كارت الوصول بالمواصلات العامة' },
    en: { h: 'How to reach us by public transport', st: 'Nearest metro station', go: 'Plan your trip on Sekka, free', ios: 'Download on the App Store', and: 'Get it on Google Play', lbl: 'How to reach us by public transport' }
  };
  var get = function (n, max) { return (s.getAttribute('data-' + n) || '').replace(/\s+/g, ' ').trim().slice(0, max); };
  var name = get('name', 120), address = get('address', 200), station = get('station', 80);
  if (!name) return;
  var lang = (get('lang', 5) || document.documentElement.lang || '').toLowerCase().slice(0, 2) === 'en' ? 'en' : 'ar';
  var t = TXT[lang];

  var ua = navigator.userAgent || '';
  var ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var android = !ios && /Android/.test(ua);

  var el = function (tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text) e.textContent = text; return e; };
  var btn = function (href, text) { var a = el('a', 'b', text); a.href = href; a.target = '_blank'; a.rel = 'noopener noreferrer'; return a; };

  var host = document.createElement('div');
  host.setAttribute('data-sekka-widget', '');
  var root = host.attachShadow({ mode: 'open' });

  var css = el('style');
  css.textContent =
    ':host{all:initial;display:block;max-width:420px}' +
    '.c{box-sizing:border-box;font:15px/1.55 system-ui,-apple-system,"Segoe UI",Tahoma,sans-serif;padding:18px 20px;border-radius:20px;background:#FBF7EE;color:#07131F;border:1px solid rgba(7,19,31,.14);box-shadow:0 10px 24px -16px rgba(7,19,31,.5)}' +
    '.k{display:flex;align-items:center;gap:8px;font-weight:700;font-size:.82em;color:#00755F}' +
    '.k i{width:10px;height:10px;border-radius:50%;background:#00A889;box-shadow:0 0 0 3px #D9F4EC}' +
    'h2{margin:8px 0 2px;font-size:1.2em;line-height:1.35;font-weight:800}' +
    'p{margin:2px 0;opacity:.86}p b,.n{font-weight:700}' +
    '.go{margin:14px 0 8px;font-weight:700}' +
    '.r{display:flex;flex-wrap:wrap;gap:8px}' +
    '.b{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 16px;border-radius:999px;background:#07131F;color:#FBF7EE;font-weight:700;font-size:.92em;text-decoration:none}' +
    '.b:hover{background:#14283D}.b:focus-visible{outline:3px solid #FFB400;outline-offset:2px}';
  root.appendChild(css);

  var card = el('div', 'c');
  card.setAttribute('role', 'group');
  card.setAttribute('aria-label', t.lbl);
  card.dir = lang === 'ar' ? 'rtl' : 'ltr';
  var k = el('div', 'k'); k.appendChild(el('i')); k.appendChild(el('span', '', 'Sekka · سكّة'));
  card.appendChild(k);
  card.appendChild(el('h2', '', t.h));
  card.appendChild(el('p', 'n', name));
  if (address) card.appendChild(el('p', '', address));
  if (station) { var st = el('p'); st.appendChild(el('b', '', t.st + ': ')); st.appendChild(document.createTextNode(station)); card.appendChild(st); }
  card.appendChild(el('p', 'go', t.go));
  var row = el('div', 'r');
  if (ios || !android) row.appendChild(btn(APP, t.ios));
  if (android || !ios) row.appendChild(btn(PLAY, t.and));
  card.appendChild(row);
  root.appendChild(card);

  s.parentNode.insertBefore(host, s.nextSibling);
})();
