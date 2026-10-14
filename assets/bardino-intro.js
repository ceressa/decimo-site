/* Bardino acilis filmi, web surumu.
 *
 * Bu dosya dort sitede (bardino.app, decimo, colmo, palmo) BIREBIR ayni.
 * Hareket oyunlardaki BardinoIntro ile ayni anahtar karelerden
 * (lib/.../bardino_logo.dart); orada degisirse burada da degistir.
 *
 * Isaret buyuyerek gelir, yazi tabandan esner, taslar sirayla belirir; i'nin
 * noktasi firlar, uc tasin ustunde piyano tusu gibi seker (tas basilir) ve
 * buyuk bir yayla i'ye donup ezilerek oturur. Anlar kullanicinin sectigi
 * konsept videosundan kare kare olculdu.
 *
 * Logo gorunur olunca bir kez oynar. Tarayicilar sayfa acilinca ses
 * caldirmiyor; data-sound verilmis logoya tiklayinca film sesiyle yeniden
 * oynar. "Hareketi azalt" diyen tarayicida hic oynamaz, logo duruk kalir.
 * Betik calismazsa da logo duruk ve tam gorunur: isaretleme dinlenme hali.
 */
(function () {
  'use strict';

  // Flutter Curves.easeInOut = Cubic(0.42, 0, 0.58, 1).
  function cubic(x1, y1, x2, y2) {
    function b(t, a1, a2) {
      var u = 1 - t;
      return 3 * u * u * t * a1 + 3 * u * t * t * a2 + t * t * t;
    }
    return function (x) {
      var lo = 0, hi = 1, t = x;
      for (var i = 0; i < 24; i++) {
        t = (lo + hi) / 2;
        if (b(t, x1, x2) < x) lo = t; else hi = t;
      }
      return b(t, y1, y2);
    };
  }
  var easeInOut = cubic(0.42, 0, 0.58, 1);

  var MARK = [[0, 0], [33, .55], [67, .81], [100, .97], [160, 1.09], [283, 1],
    [300, 1], [350, 1.11], [467, 1]];
  var WORD = [[0, 0], [145, 0], [167, .35], [200, .76], [233, 1], [285, 1.18],
    [300, 1.18], [367, 1.12], [400, 1]];
  var STONE_POP = [[0, 0], [50, 1.15], [100, 1]];
  var PRESS = [[-10, 0], [20, 1], [120, 0]];
  var LAND_X = [[0, 1], [57, 1.47], [107, 1.41], [140, 1.24], [173, 1.24], [207, 1]];
  var LAND_Y = [[0, 1], [57, .65], [123, .65], [140, .76], [173, .88], [207, 1]];
  var HITS = [620, 762, 900];
  var LAUNCH = 433, LAND = 1160, END = 1600;

  // Kilit biriminde (600x150): noktanin dinlenme merkezi ve alt kenari,
  // taslarin ust kenari ve merkezleri.
  var DOT_X0 = 134 + 460 * .62, DOT_B0 = 8 + 37 * .62;
  var STONE_TOP = 112 + 2 * .65;
  function stoneX(i) { return 139 + (18 + 42 * i) * .65; }
  var WORD_BASE = 8 + 136 * .62;

  function keys(t, k) {
    if (t <= k[0][0]) return k[0][1];
    for (var i = 1; i < k.length; i++) {
      if (t <= k[i][0]) {
        var a = k[i - 1], b = k[i];
        var s = easeInOut((t - a[0]) / (b[0] - a[0]));
        return a[1] + (b[1] - a[1]) * s;
      }
    }
    return k[k.length - 1][1];
  }

  // y(s) = a s^2 + b s + y0; y(1) = y1, en ust nokta tepe.
  function atis(y0, y1, tepe, s) {
    var d = y1 - y0, h = y0 - tepe, p = 2 * d + 4 * h;
    var a = (p + Math.sqrt(Math.max(0, p * p - 4 * d * d))) / 2;
    return a * s * s + (d - a) * s + y0;
  }

  function dotPath(ms) {
    var temas = [0, 1, 2].map(function (i) {
      return [stoneX(i) - DOT_X0, STONE_TOP - DOT_B0];
    });
    var duraklar = [
      [LAUNCH, [0, 0], 0],
      [HITS[0], temas[0], -52.3],
      [HITS[1], temas[1], temas[0][1] - 16],
      [HITS[2], temas[2], temas[1][1] - 16],
      [LAND, [0, 0], -74]
    ];
    for (var i = 1; i < duraklar.length; i++) {
      var t0 = duraklar[i - 1][0], p0 = duraklar[i - 1][1];
      var t1 = duraklar[i][0], p1 = duraklar[i][1], tepe = duraklar[i][2];
      if (ms <= t1) {
        var s = Math.min(1, Math.max(0, (ms - t0) / (t1 - t0)));
        return [p0[0] + (p1[0] - p0[0]) * s, atis(p0[1], p1[1], tepe, s)];
      }
    }
    return [0, 0];
  }

  function frameAt(ms) {
    var f = {
      mark: keys(ms, MARK),
      wordY: keys(ms, WORD),
      stoneIn: [0, 1, 2].map(function (i) { return keys(ms - (300 + 50 * i), STONE_POP); }),
      press: [0, 1, 2].map(function (i) { return keys(ms - HITS[i], PRESS); }),
      dot: [0, 0], dx: 1, dy: 1
    };
    if (ms < LAUNCH) {
      f.dy = f.wordY;
    } else if (ms < LAND) {
      f.dot = dotPath(ms);
      var temas = Math.min.apply(null, HITS.concat([LAND]).map(function (h) { return Math.abs(ms - h); }));
      var k = Math.min(1, Math.max(0, temas / 24));
      f.dx = 1 - .12 * k;
      f.dy = 1 + .30 * k;
    } else {
      f.dx = keys(ms - LAND, LAND_X);
      f.dy = keys(ms - LAND, LAND_Y);
    }
    return f;
  }

  function n(v) { return Math.round(v * 1000) / 1000; }

  function draw(svg, f) {
    var mark = svg.querySelector('.bi-mark');
    var word = svg.querySelector('.bi-word');
    var dot = svg.querySelector('.bi-dot');
    var stones = svg.querySelectorAll('.bi-stone');
    mark.setAttribute('transform', 'translate(56 62) scale(' + n(f.mark) + ') translate(-56 -62)');
    word.setAttribute('transform', 'translate(0 ' + n(WORD_BASE) + ') scale(1 ' + n(f.wordY) + ') translate(0 ' + n(-WORD_BASE) + ')');
    for (var i = 0; i < stones.length; i++) {
      var c = 2 + 42 * i + 16, g = f.stoneIn[i], p = Math.min(1, Math.max(0, f.press[i]));
      stones[i].setAttribute('transform', 'translate(' + c + ' 38) scale(' +
        n(g * (1 + .18 * p)) + ' ' + n(g * (1 - .20 * p)) + ') translate(' + (-c) + ' -38)');
    }
    dot.setAttribute('transform', 'translate(' + n(DOT_X0 + f.dot[0]) + ' ' + n(DOT_B0 + f.dot[1]) +
      ') scale(' + n(f.dx) + ' ' + n(f.dy) + ')');
    dot.style.opacity = f.wordY > 0 ? '' : '0';
  }

  // Olcum icin: oyunlardaki BardinoIntro.frameAt ile ayni sayilari verdigi
  // dogrulanabilsin (bkz. bardino_acilis_test).
  window.bardinoIntroFrameAt = frameAt;

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function play(svg) {
    if (svg._biRaf) cancelAnimationFrame(svg._biRaf);
    var start = null;
    function step(now) {
      if (start === null) start = now;
      var ms = now - start;
      draw(svg, frameAt(Math.min(ms, END)));
      if (ms < END) svg._biRaf = requestAnimationFrame(step);
      else svg._biRaf = null;
    }
    svg._biRaf = requestAnimationFrame(step);
  }

  function sound(svg) {
    var url = svg.getAttribute('data-sound');
    if (!url) return;
    if (!svg._biAudio) svg._biAudio = new Audio(url);
    try {
      svg._biAudio.currentTime = 0;
      var p = svg._biAudio.play();
      if (p && p.catch) p.catch(function () {});
    } catch (e) { /* ses dekorasyon */ }
  }

  var logos = document.querySelectorAll('svg[data-bardino-intro]');
  if (!logos.length || reduce) return;

  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting && !e.target._biPlayed) {
        e.target._biPlayed = true;
        io.unobserve(e.target);
        play(e.target);
      }
    });
  }, { threshold: 0.6 }) : null;

  Array.prototype.forEach.call(logos, function (svg) {
    if (io) {
      // Yalniz zaten ekranda olan logo ilk kareye (bos) cekilir, bir an
      // tam logo gorunup kaybolmasin. Asagidakiler gelene kadar duruk ve tam
      // gorunur kalir: betik hic oynamazsa logo kaybolmaz.
      var r = svg.getBoundingClientRect();
      if (r.bottom > 0 && r.top < (window.innerHeight || 0)) draw(svg, frameAt(0));
      io.observe(svg);
    } else {
      play(svg);
    }
    if (svg.hasAttribute('data-sound')) {
      var tekrar = function () { sound(svg); play(svg); };
      svg.addEventListener('click', tekrar);
      svg.addEventListener('keydown', function (ev) {
        if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); tekrar(); }
      });
    }
  });
})();
