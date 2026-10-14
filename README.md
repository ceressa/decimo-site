# decimo-site

[decimo.bardino.app](https://decimo.bardino.app) - Decimo'nun tanitim sayfasi, gizlilik
politikasi, kullanim kosullari, hesap silme sayfasi ve reklam yonlendirmeleri.

Oyun deposu ayri: `com.bardino.numberchain`, `E:\dev\mobile\Decimo-numberchain`.

## Acilis sayfalari elle yazilmaz, uretilir

```powershell
python build.py
```

Site Ekim 2026'ya kadar elle yazilmis tek bir Turkce sayfaydi; magaza kaydi 12
dilde ve web sitesi alani buraya gosteriyor. Alti dilde elle tutulan alti dosya
kaciniyor: bir cumleyi degistirmek icin alti dosyaya dokunmak, bes tanesinin
bayat kalmasi demek. Icerik `build.py` icinde sozluk, HTML yalnizca cikti.
**Uretilen dosyalari elle duzenleme**, bir sonraki derlemede geri gider.

Uretilen dosyalar: `index.html`, `tr|de|fr|es|pt/index.html`, yasal sayfalar
(`privacy-policy.html`, `terms-of-use.html`, `account-deletion.html` ve
`tr/` altindaki Turkce kopyalari), `sitemap.xml`, `robots.txt`,
`manifest.json`, `.nojekyll`.

- **Yasal sayfalar yalnizca Ingilizce (kok) ve Turkce (`/tr/`)**, govdeleri
  `legal_text.py`'de. Turkce metin "siz" diye hitap eder. Her cumlenin oyun
  deposundaki kaynagi dosyanin basinda yazili; metnin ozu degisirse
  `UPDATED` tarihi de degisir. Adresler eskisiyle ayni, cunku uygulama
  (magaza ekrani, gizlilik ozeti), magaza kayitlari ve App Store EULA'si bu
  adreslere bagli. Ingilizce yasal sayfa, Turkce tarayicidan ve site
  disindan gelen ziyaretciyi `/tr/` kopyasina gonderir (eski tek sayfa
  tarayici diliyle aciliyordu); `?lang=en` bunu durdurur.
- **Yazi tipi kendi sunucumuzda**: `assets/fonts/nunito-*.woff2`, oyunun
  kendi Nunito TTF'lerinden fontTools ile Latin + Latin Extended-A olarak
  kesildi, lisans `assets/fonts/OFL.txt`. Sayfa baska bir sunucudan hicbir sey
  yuklemiyor ve altbilgi bunu soyluyor; bir CDN eklenirse o cumle de degismeli.
- **E-posta adresleri `<!--email_off-->` icinde**: Cloudflare'in Email
  Address Obfuscation'i adresi JavaScript'siz 404 veren bir baglantiya
  ceviriyordu. Adres uretecin icinde `mail_link()`'ten geciyor.

- Acilis sayfasi alti dilde: **en (kok)**, tr, de, fr, es, pt. Yapi Colmo ve
  Palmo ile ayni (`palmo-site/build.py`): dizin bicimli adresler, hreflang ve
  x-default, dil basina canonical ve og:locale.
- **Turkce kaynak metindir.** Diger diller ondan cevrildi; anlam degisecekse
  once `T["tr"]` degisir, sonra digerleri.
- Ingilizce, Almanca, Fransizca, Ispanyolca ve Portekizce metni Ekim 2026'da
  bir yapay zeka (Claude) Turkceden yazdi. Terimler magaza metninden
  (`tools/store/listing-copy.mjs`) ve oyunun dil dosyalarindan alindi; anadili
  konusan biri henuz okumadi.

`build.py` derleme sonunda eksikleri listeler (CNAME, gorseller). O liste is
listesidir, hata degil.

Yerelde bakmak icin (adresler `/css/...` bicimde mutlak, dosyayi cift tiklamak
yetmez):

```powershell
python -m http.server 8093 --bind 127.0.0.1
```

## Elle duran dosyalar

Bunlar uretilmiyor ve **adresleri degismez**: magaza kayitlari, reklamlar ve
TikTok videosu onlara bagli.

| Dosya | Neden elle |
|---|---|
| `indir.html` | Reklam trafigini cihaza gore magazaya yonlendiriyor. |
| `tt.html` | TikTok kisa adresi, kokteki sayfaya utm ile gidiyor. |
| `404.html` | Kopuk zincir sayfasi. |
| `app-ads.txt`, `CNAME` | AdMob ve alan adi. |

## Ekran goruntuleri

Vitrinde dort kare, 800x1600 webp (kalite 82, method 6). Yazi tasiyan kare
**sayfanin dilinde** olmali:

- `assets/shots/` Ingilizce set: kok ve de/fr/es/pt bunu gosteriyor.
- `assets/shots/tr/` Turkce set: yalniz /tr/.

Kendi klasoru olmayan dil Ingilizce setle aciliyor (`build.py`, `SHOT_DIRS`).
Kareler magazadaki surumun (1.0.31, `d3dc1ea`) Windows Release derlemesinden,
`tools/store/capture-shots.ps1` ile cekildi; siteye ozel kare cizilmiyor.

| Dosya | Ne |
|---|---|
| `01_chain.webp` | L32, zincir cizilirken. Kahraman gorseli de bu. |
| `03_star.webp` | L32, "1. yildiz" ani. |
| `05_map.webp` | Bolum haritasi. |
| `06_world.webp` | L50, yanardag: lav sirasi yukselmisken zincir. |

## Yayin

GitHub Pages, `master` dali, kok dizin. `python build.py` yerelde kosuluyor
ve cikti commit ediliyor. `.nojekyll` uretiliyor, boylece alt cizgiyle
baslayan bir klasor ileride sessizce yayindan dusmez.

Yayina aldiktan sonra tek tek GET ile geri oku, panelin "basarili" demesine
guvenme: `/`, `/tr/`, `/de/`, `/sitemap.xml`, `/privacy-policy.html`,
`/indir.html`, `/app-ads.txt`.
