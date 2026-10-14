# -*- coding: utf-8 -*-
"""decimo.bardino.app acilis sayfalarini uretir.

    python build.py

Neden uretici: site Ekim 2026'ya kadar elle yazilmis tek bir Turkce sayfaydi.
Magaza kaydi 12 dilde ve web sitesi alani buraya gosteriyor; Alman oyuncu
Turkce bir sayfaya iniyordu. Alti dilde elle tutulan alti dosya kaciniyor: bir
cumleyi degistirmek icin alti dosyaya dokunmak, bes tanesinin bayat kalmasi
demek. Icerik burada sozluk, HTML yalnizca cikti. Uretilen .html dosyalarini
elle duzenleme, bir sonraki derlemede geri gider.

Kok dizin INGILIZCE, Turkce /tr/ altinda (Colmo ve Palmo ile ayni kural).
Koke gelen ziyaretcinin cogu Turkce bilmiyor; magaza listesi de varsayilan
olarak Ingilizce.

YASAL SAYFALAR da Ekim 2026'dan beri buradan uretiliyor, yalnizca Ingilizce
(kok) ve Turkce (/tr/), ayni dosya adlariyla. Govdeler legal_text.py'de.
Eskiden tek dosyada yedi dil vardi, varsayilani Turkceydi ve Ingilizce
sitedeki "Privacy" baglantisi Turkce bir sayfa aciyordu. Adresler
DEGISMEDI: uygulama (shop_screen, gizlilik ozeti), magaza kayitlari ve
App Store EULA'si /privacy-policy.html, /terms-of-use.html ve
/account-deletion.html'e bagli.

URETILMEYENLER, bilerek: indir.html, tt.html, 404.html (yonlendirme ve hata
sayfalari, elle).

Yapi palmo-site/build.py ile ayni (path_for / file_for, hreflang, sitemap).
Sabitler ayri bir config.py'de degil burada; legal_text.py yalnizca metin
tutuyor ve buradan bir sey okumuyor.
"""
import io
import os
import re
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))

# ── sabitler ────────────────────────────────────────────────────────────────

SITE = "https://decimo.bardino.app"
DOMAIN = SITE.split("//", 1)[1]
APP = "Decimo"
DEV = "Bardino Technology"
PKG = "com.bardino.numberchain"
GOOGLE_PLAY = "https://play.google.com/store/apps/details?id=" + PKG

# Ulkesiz App Store adresi ziyaretciyi kendi ulkesinin magazasina goturuyor.
# Turkce sayfa /tr/ adresini koruyor: eski sayfa oyleydi ve Turkce okuyanin
# buyuk cogunlugu Turkiye magazasinda.
APP_STORE = "https://apps.apple.com/app/decimo-number-chain/id6792291932"
APP_STORE_TR = "https://apps.apple.com/tr/app/decimo-number-chain/id6792291932"

# Olcum: Play kurulum atfi YALNIZCA `referrer` icinden gecer ve icerigi
# URL-kodlu olmak zorunda (bkz. indir.html). Apple utm_*'yi yutuyor ama
# yonlendiren kaydinda kaynak gorunuyor. Degerler eski elle yazilmis sayfayla
# birebir ayni; kampanya verisi dil donusumunde kopmasin.
UTM = "utm_source=decimo_site&utm_medium=web&utm_campaign="

SOCIAL = [
    ("Instagram", "https://www.instagram.com/decimogame/"),
    ("Facebook", "https://www.facebook.com/profile.php?id=61593083333364"),
    ("TikTok", "https://www.tiktok.com/@decimo_game"),
]

# Dil kodu -> (html lang, og locale, kendi dilindeki adi, dar ekran kodu)
# Kok once, gerisi oyunun ayarlar ekranindaki sirayla
# (lib/screens/settings_screen.dart, _languages).
# Portekizce metin Brezilya Portekizcesi ("voce", "tela"): html lang da
# hreflang da "pt-BR". Adres /pt/ kaliyor.
LANGS = [
    ("en", "en", "en_US", "English", "EN"),
    ("tr", "tr", "tr_TR", "Türkçe", "TR"),
    ("de", "de", "de_DE", "Deutsch", "DE"),
    ("fr", "fr", "fr_FR", "Français", "FR"),
    ("es", "es", "es_ES", "Español", "ES"),
    ("pt", "pt-BR", "pt_BR", "Português", "PT"),
]
ROOT_LANG = "en"

# Yasal sayfalar yalnizca bu dillerde (Palmo ile ayni). Diger dillerin
# altbilgisi Ingilizce yasal sayfalara gidiyor.
LEGAL = ("privacy-policy.html", "terms-of-use.html", "account-deletion.html")
LEGAL_LANGS = ("en", "tr")

SUPPORT_MAIL = "info@bardino.app"

# Self-hosted Nunito (assets/fonts, bkz. css/style.css). Derleme sonunda
# varliklari kontrol ediliyor.
FONTS = ["assets/fonts/nunito-%d.woff2" % w for w in (400, 600, 700, 800, 900)]

SHARE = "assets/decimo_share.png"   # 1200x630, yazisiz: her dilde ayni
ICON = "assets/decimo_icon.png"

# Vitrindeki dort kare, 800x1600 webp. Yazi tasiyan kare sayfanin dilinde
# olmali: Ingilizce kareler assets/shots/ altinda ve kok ile de/fr/es/pt
# onlari gosteriyor; Turkce kareler assets/shots/tr/ altinda. Kendi klasoru
# olmayan dil Ingilizce setle aciliyor. Hangi karenin ne oldugu ve nereden
# geldigi: README.md.
SHOTS = ["01_chain.webp", "03_star.webp", "05_map.webp", "06_world.webp"]
SHOT_DIRS = {"tr": "assets/shots/tr"}
SHOT_DEFAULT = "assets/shots"


# ── metin ───────────────────────────────────────────────────────────────────
#
# TURKCE KAYNAK METINDIR. Diger diller ondan cevrildi; anlam degisecekse once
# Turkce degisir. Sayilar (145 bolum, 15 dunya, 5 mod, 7 guclendirme, 146 ve
# 222 puan) oyunun kendisinden: puan floor(8 * uzunluk^1.6), dort tas 73,
# sekiz tas 222. Bolum eklenince "145" bes dilde birden degisir.
#
# Terimler magaza metniyle ayni (Decimo deposu tools/store/listing-copy.mjs):
# "Number Chain", "levels / worlds", Almanca "Level / Welten", Portekizce
# "fases / mundos", "corrente". Guclendirme adlari oyunun kendi dil
# dosyalarindan (lib/l10n/locale_*.dart, powerUp*).
#
# `**x**` kalin yazilir (adim 2'deki 222). Baska bicim yok, gerisi kacirilir.
#
# Ingilizce, Almanca, Fransizca, Ispanyolca ve Portekizce metni Ekim 2026'da
# bir yapay zeka (Claude) Turkceden yazdi; anadili konusan biri okumadi.

T = {}

T["tr"] = {
    "title": "Decimo - Sayı Zinciri Bulmacası",
    "desc": "Decimo, bitişik sayıları sürükleyerek zincir kurduğun bir sayı "
            "bulmacası. 15 dünya, 145 bölüm. App Store ve Google Play'de "
            "ücretsiz.",
    "ogdesc": "Bitişik sayıları sürükle, zincir kur. 15 dünya, 145 bölüm, "
              "ücretsiz.",
    "nav": ("Nasıl oynanır", "Neler var", "Ekranlar"),
    "langsLabel": "Dil",
    "h1a": "Sayıları birleştir,",
    "h1b": "zinciri kur.",
    "lead": "Bitişik sayıları artan sırayla bağla, zinciri uzatabildiğin "
            "kadar uzat.",
    "small": "Ücretsiz. İnternetsiz oynanır.",
    "heroAlt": "Decimo oynanış ekranı: sayı ızgarasında kurulan zincir",
    "howT": "Nasıl oynanır",
    "howS": "",
    "steps": [
        ("Sürükle",
         "Parmağını bitişik hücrelerde gezdir; çapraz komşular da sayılır. "
         "Puan için zincirde en az üç taş olmalı."),
        ("Uzat",
         "9'dan sonra 1 gelir, zincir sen bırakmadıkça bitmiyor. Uzun zincir "
         "daha çok puan getirir: dört taşlık iki zincir 146, sekiz taşlık "
         "tek zincir **222** puan."),
        ("Yıldızları topla",
         "Her bölümde birbirinden bağımsız üç yıldız hedefi var; istediğin "
         "sırayla tamamlayabilirsin."),
    ],
    "featT": "İçinde neler var",
    "featS": "Ödüllü reklamlar isteğe bağlı; bölüm aralarındakileri tek bir "
             "satın alımla kapatabilirsin. Oyunu para ödemeden "
             "bitirebilirsin.",
    "feats": [
        ("145", "Elle tasarlanmış bölüm",
         "Her tahta tek tek oynanıp dengelendi."),
        ("15", "Dünya", "Ormandan yanardağa, kristal mağaradan karadeliğe."),
        ("5", "Zincir modu",
         "Artan, azalan, tek, çift, serbest. Aynı tahtada bambaşka hamleler."),
        ("7", "Güçlendirme", "İpucu, geri al, bomba, karıştır, ekstra hamle, "
                            "joker, çift puan."),
    ],
    "shotsT": "Oyundan kareler",
    "shotsS": "",
    # (alt, altyazi), SHOTS sirasiyla
    "shots": [
        ("Zincir kurulurken oynanış ekranı", "Zinciri sürükleyerek kur"),
        ("Bölüm sırasında kazanılan ilk yıldız", "Üç bağımsız yıldız hedefi"),
        ("Bölüm haritası", "Bölümler arasında ilerle"),
        ("Yanardağ dünyasında lav yükselirken kurulan zincir",
         "Her dünyanın kendi havası var"),
    ],
    "numoAlt": "Numo, Decimo'nun maskotu",
    "numoT": "Numo yolda sana eşlik ediyor",
    "numoP": "Zincirin uzadığında seviniyor, takıldığında ipucu veriyor. "
             "Bölümü geçtiğinde en çok o kutluyor.",
    "endT": "Bir bölüm oynayacaktın.",
    "endS": "145 bölüm, 15 dünya. Ücretsiz, iki mağazada da.",
    "family": "Bardino'nun diğer oyunları:",
    "legal": ("Gizlilik politikası", "Kullanım koşulları", "Hesap silme"),
    "support": "Destek",
    "game": "Bir Bardino oyunu",
    "noCookies": "Bu site çerez kullanmaz ve başka sunuculardan hiçbir şey "
                 "yüklemez.",
    "upd": "Son güncelleme",
}

T["en"] = {
    "title": "Decimo - Number Chain Puzzle",
    "desc": "Decimo is a number puzzle: drag across adjacent numbers to build "
            "a chain. 15 worlds, 145 levels. Free on the App Store and Google "
            "Play.",
    "ogdesc": "Drag across adjacent numbers and build a chain. 15 worlds, 145 "
              "levels, free.",
    "nav": ("How to play", "What's inside", "Screenshots"),
    "langsLabel": "Language",
    "h1a": "Link the numbers,",
    "h1b": "build the chain.",
    "lead": "Connect neighboring numbers in rising order and make the chain "
            "as long as you can.",
    "small": "Free. Plays offline.",
    "heroAlt": "Decimo gameplay: a chain being built on the number grid",
    "howT": "How to play",
    "howS": "",
    "steps": [
        ("Drag",
         "Slide your finger across neighboring cells; diagonal neighbors "
         "count too. A chain needs at least three tiles to score."),
        ("Extend",
         "After 9 comes 1, so the chain doesn't end until you let go. Longer "
         "chains score more: two 4-tile chains score 146, one 8-tile chain "
         "scores **222**."),
        ("Collect the stars",
         "Each level has three independent star goals. You can complete them "
         "in any order."),
    ],
    "featT": "What's inside",
    "featS": "Rewarded ads are optional, and the ones between levels can be "
             "switched off with a single purchase. You can reach the end "
             "without paying.",
    "feats": [
        ("145", "Hand-designed levels",
         "Every board was played and balanced one by one."),
        ("15", "Worlds",
         "From the forest to the volcano, from the crystal cave to the black "
         "hole."),
        ("5", "Chain modes",
         "Ascending, descending, odd, even, free. Same board, very different "
         "moves."),
        ("7", "Power-ups", "Hint, undo, bomb, shuffle, extra moves, joker, "
                          "double points."),
    ],
    "shotsT": "From the game",
    "shotsS": "",
    "shots": [
        ("Gameplay screen while a chain is being drawn",
         "Drag to build the chain"),
        ("The first star, earned mid-level", "Three independent star goals"),
        ("The level map", "Move from level to level"),
        ("A chain being built as lava rises in the volcano world",
         "Every world has its own mood"),
    ],
    "numoAlt": "Numo, Decimo's mascot",
    "numoT": "Numo keeps you company along the way",
    "numoP": "Numo cheers when your chain grows and gives you a hint when you "
             "get stuck. When you clear a level, no one celebrates more.",
    "endT": "You were only going to play one level.",
    "endS": "145 levels, 15 worlds. Free, in both stores.",
    "family": "More from Bardino:",
    "legal": ("Privacy policy", "Terms of use", "Account deletion"),
    "support": "Support",
    "game": "A Bardino game",
    "noCookies": "This site sets no cookies and loads nothing from other "
                 "servers.",
    "upd": "Last updated",
}

T["de"] = {
    "title": "Decimo - Zahlenketten-Puzzle",
    "desc": "Decimo ist ein Zahlenpuzzle: Zieh über benachbarte Zahlen und bau "
            "eine Kette. 15 Welten, 145 Level. Kostenlos im App Store und bei "
            "Google Play.",
    "ogdesc": "Zieh über benachbarte Zahlen und bau eine Kette. 15 Welten, 145 "
              "Level, kostenlos.",
    "nav": ("So wird gespielt", "Was drin ist", "Screenshots"),
    "langsLabel": "Sprache",
    "h1a": "Verbinde die Zahlen,",
    "h1b": "bau die Kette.",
    "lead": "Zieh über benachbarte Zahlen in aufsteigender Reihenfolge und "
            "mach die Kette so lang, wie du kannst.",
    "small": "Kostenlos. Auch offline spielbar.",
    "heroAlt": "Decimo im Spiel: Auf dem Zahlengitter entsteht eine Kette",
    "howT": "So wird gespielt",
    "howS": "",
    "steps": [
        ("Ziehen",
         "Fahr mit dem Finger über benachbarte Felder, diagonal zählt auch. "
         "Punkte gibt es erst ab drei Steinen in einer Kette."),
        ("Verlängern",
         "Nach der 9 kommt die 1, die Kette endet erst, wenn du loslässt. "
         "Längere Ketten bringen mehr Punkte: zwei Ketten aus vier Steinen "
         "146, eine Kette aus acht Steinen **222**."),
        ("Sterne sammeln",
         "Jedes Level hat drei voneinander unabhängige Sternziele; du kannst "
         "sie in beliebiger Reihenfolge erreichen."),
    ],
    "featT": "Was drin ist",
    "featS": "Werbung mit Belohnung ist freiwillig, die zwischen den Levels "
             "lässt sich mit einem einzigen Kauf abschalten. Bis zum Ende "
             "kommst du auch, ohne zu bezahlen.",
    "feats": [
        ("145", "Handgemachte Level",
         "Jedes Brett wurde einzeln gespielt und ausbalanciert."),
        ("15", "Welten",
         "Vom Wald zum Vulkan, von der Kristallhöhle zum Schwarzen Loch."),
        ("5", "Kettenmodi",
         "Aufsteigend, absteigend, ungerade, gerade, frei. Auf demselben "
         "Brett ganz andere Züge."),
        ("7", "Hilfen",
         "Hinweis, Rückgängig, Bombe, Mischen, Extrazüge, Joker, doppelte "
         "Punkte."),
    ],
    "shotsT": "Aus dem Spiel",
    "shotsS": "",
    "shots": [
        ("Spielbildschirm, während eine Kette gezogen wird",
         "Kette durch Ziehen bauen"),
        ("Der erste Stern, mitten im Level verdient",
         "Drei unabhängige Sternziele"),
        ("Die Levelkarte", "Von Level zu Level"),
        ("Eine Kette entsteht, während in der Vulkanwelt die Lava steigt",
         "Jede Welt hat ihre eigene Stimmung"),
    ],
    "numoAlt": "Numo, das Maskottchen von Decimo",
    "numoT": "Numo begleitet dich unterwegs",
    "numoP": "Numo freut sich, wenn deine Kette wächst, und gibt dir einen "
             "Hinweis, wenn du feststeckst. Wenn du ein Level schaffst, "
             "feiert niemand mehr als Numo.",
    "endT": "Du wolltest doch nur ein Level spielen.",
    "endS": "145 Level, 15 Welten. Kostenlos, in beiden Stores.",
    "family": "Mehr von Bardino:",
    "legal": ("Datenschutz", "Nutzungsbedingungen", "Konto löschen"),
    "support": "Support",
    "game": "Ein Spiel von Bardino",
    "noCookies": "Diese Seite setzt keine Cookies und lädt nichts von "
                 "anderen Servern.",
}

T["fr"] = {
    "title": "Decimo - Chaîne de nombres",
    "desc": "Decimo est un puzzle de nombres : fais glisser ton doigt sur des "
            "nombres voisins pour former une chaîne. 15 mondes, 145 niveaux. "
            "Gratuit sur l'App Store et Google Play.",
    "ogdesc": "Fais glisser ton doigt sur des nombres voisins et forme une "
              "chaîne. 15 mondes, 145 niveaux, gratuit.",
    "nav": ("Comment jouer", "Au programme", "Captures"),
    "langsLabel": "Langue",
    "h1a": "Relie les nombres,",
    "h1b": "forme la chaîne.",
    "lead": "Enchaîne des nombres voisins dans l'ordre croissant et allonge "
            "la chaîne autant que tu peux.",
    "small": "Gratuit. Jouable hors ligne.",
    "heroAlt": "Decimo en jeu : une chaîne se forme sur la grille de nombres",
    "howT": "Comment jouer",
    "howS": "",
    "steps": [
        ("Glisse",
         "Fais glisser ton doigt sur des cases voisines ; la diagonale compte "
         "aussi. Une chaîne rapporte des points à partir de trois cases."),
        ("Allonge",
         "Après 9 vient 1 : la chaîne ne s'arrête que quand tu lâches. Les "
         "chaînes longues rapportent plus : deux chaînes de quatre cases "
         "font 146 points, une chaîne de huit cases **222**."),
        ("Récolte les étoiles",
         "Chaque niveau a trois objectifs d'étoile indépendants ; tu peux "
         "les remplir dans l'ordre que tu veux."),
    ],
    "featT": "Au programme",
    "featS": "Les pubs récompensées sont facultatives, et celles entre les "
             "niveaux se désactivent avec un seul achat. Tu peux aller "
             "jusqu'au bout sans payer.",
    "feats": [
        ("145", "Niveaux faits main",
         "Chaque plateau a été joué et équilibré un par un."),
        ("15", "Mondes",
         "De la forêt au volcan, de la grotte de cristal au trou noir."),
        ("5", "Modes de chaîne",
         "Croissant, décroissant, impair, pair, libre. Sur le même plateau, "
         "des coups tout autres."),
        ("7", "Bonus",
         "Indice, annuler, bombe, mélanger, coups bonus, joker, points "
         "doubles."),
    ],
    "shotsT": "Images du jeu",
    "shotsS": "",
    "shots": [
        ("L'écran de jeu pendant qu'une chaîne se forme",
         "Forme la chaîne en glissant"),
        ("La première étoile, gagnée en cours de niveau",
         "Trois objectifs d'étoiles indépendants"),
        ("La carte des niveaux", "Avance de niveau en niveau"),
        ("Une chaîne se forme pendant que la lave monte dans le monde du "
         "volcan", "Chaque monde a son ambiance"),
    ],
    "numoAlt": "Numo, la mascotte de Decimo",
    "numoT": "Numo t'accompagne en chemin",
    "numoP": "Numo se réjouit quand ta chaîne s'allonge et te donne un indice "
             "quand tu bloques. Quand tu termines un niveau, c'est Numo qui "
             "le fête le plus.",
    "endT": "Tu ne devais jouer qu'un seul niveau.",
    "endS": "145 niveaux, 15 mondes. Gratuit, sur l'App Store comme sur "
            "Google Play.",
    "family": "Autres jeux de Bardino :",
    "legal": ("Confidentialité", "Conditions d'utilisation",
              "Suppression du compte"),
    # Fransizcada iki noktadan once bosluk var; kirilmayan bosluk, satir
    # sonunda iki nokta tek basina kalmasin diye.
    "support": "Assistance ",
    "game": "Un jeu Bardino",
    "noCookies": "Ce site ne dépose aucun cookie et ne charge rien depuis "
                 "d'autres serveurs.",
}

T["es"] = {
    "title": "Decimo - Cadena de números",
    "desc": "Decimo es un puzle de números: desliza el dedo por números "
            "vecinos para formar una cadena. 15 mundos, 145 niveles. Gratis "
            "en el App Store y Google Play.",
    "ogdesc": "Desliza el dedo por números vecinos y forma una cadena. 15 "
              "mundos, 145 niveles, gratis.",
    "nav": ("Cómo se juega", "Qué incluye", "Capturas"),
    "langsLabel": "Idioma",
    "h1a": "Une los números,",
    "h1b": "forma la cadena.",
    "lead": "Conecta números vecinos en orden ascendente y alarga la cadena "
            "todo lo que puedas.",
    "small": "Gratis. Se juega sin conexión.",
    "heroAlt": "Decimo en juego: una cadena formándose en la cuadrícula de "
               "números",
    "howT": "Cómo se juega",
    "howS": "",
    "steps": [
        ("Desliza",
         "Pasa el dedo por casillas vecinas; en diagonal también cuenta. Una "
         "cadena da puntos a partir de tres fichas."),
        ("Alarga",
         "Después del 9 viene el 1: la cadena no termina hasta que sueltas. "
         "Las cadenas largas dan más puntos: dos cadenas de cuatro fichas "
         "suman 146, una de ocho fichas **222**."),
        ("Consigue las estrellas",
         "Cada nivel tiene tres objetivos de estrella independientes; puedes "
         "cumplirlos en el orden que quieras."),
    ],
    "featT": "Qué incluye",
    "featS": "Los anuncios con recompensa son opcionales, y los que aparecen "
             "entre niveles se quitan con una sola compra. Puedes llegar al "
             "final sin pagar.",
    "feats": [
        ("145", "Niveles hechos a mano",
         "Cada tablero se jugó y se equilibró uno a uno."),
        ("15", "Mundos",
         "Del bosque al volcán, de la cueva de cristal al agujero negro."),
        ("5", "Modos de cadena",
         "Ascendente, descendente, impar, par, libre. En el mismo tablero, "
         "jugadas muy distintas."),
        ("7", "Ayudas",
         "Pista, deshacer, bomba, mezclar, movimientos extra, comodín, "
         "puntos dobles."),
    ],
    "shotsT": "Del juego",
    "shotsS": "",
    "shots": [
        ("Pantalla de juego mientras se dibuja una cadena",
         "Forma la cadena deslizando el dedo"),
        ("La primera estrella, ganada a mitad de nivel",
         "Tres objetivos de estrella independientes"),
        ("El mapa de niveles", "Avanza de nivel en nivel"),
        ("Una cadena formándose mientras sube la lava en el mundo del volcán",
         "Cada mundo tiene su propio ambiente"),
    ],
    "numoAlt": "Numo, la mascota de Decimo",
    "numoT": "Numo te acompaña por el camino",
    "numoP": "Numo se alegra cuando tu cadena crece y te da una pista cuando "
             "te atascas. Cuando superas un nivel, nadie lo celebra tanto "
             "como Numo.",
    "endT": "Ibas a jugar solo un nivel.",
    "endS": "145 niveles, 15 mundos. Gratis, en las dos tiendas.",
    "family": "Más de Bardino:",
    "legal": ("Privacidad", "Términos de uso", "Eliminar cuenta"),
    "support": "Soporte",
    "game": "Un juego de Bardino",
    "noCookies": "Este sitio no usa cookies y no carga nada desde otros "
                 "servidores.",
}

T["pt"] = {
    "title": "Decimo - Corrente de números",
    "desc": "Decimo é um puzzle de números: arraste o dedo por números "
            "vizinhos para montar uma corrente. 15 mundos, 145 fases. Grátis "
            "na App Store e no Google Play.",
    "ogdesc": "Arraste o dedo por números vizinhos e monte uma corrente. 15 "
              "mundos, 145 fases, grátis.",
    "nav": ("Como jogar", "O que tem", "Telas"),
    "langsLabel": "Idioma",
    "h1a": "Ligue os números,",
    "h1b": "monte a corrente.",
    "lead": "Conecte números vizinhos em ordem crescente e deixe a corrente "
            "o mais longa que você conseguir.",
    "small": "Grátis. Joga-se offline.",
    "heroAlt": "Decimo em jogo: uma corrente sendo montada na grade de "
               "números",
    "howT": "Como jogar",
    "howS": "",
    "steps": [
        ("Arraste",
         "Passe o dedo por casas vizinhas; na diagonal também vale. Uma "
         "corrente só pontua a partir de três peças."),
        ("Estique",
         "Depois do 9 vem o 1: a corrente só termina quando você solta. "
         "Correntes longas valem mais: duas correntes de quatro peças somam "
         "146 pontos, uma de oito peças **222**."),
        ("Pegue as estrelas",
         "Cada fase tem três metas de estrela independentes; você pode "
         "cumpri-las na ordem que quiser."),
    ],
    "featT": "O que tem",
    "featS": "Os anúncios com recompensa são opcionais, e os que aparecem "
             "entre as fases saem com uma única compra. Dá para chegar ao fim "
             "sem pagar.",
    "feats": [
        ("145", "Fases feitas à mão",
         "Cada tabuleiro foi jogado e equilibrado um por um."),
        ("15", "Mundos",
         "Da floresta ao vulcão, da caverna de cristal ao buraco negro."),
        ("5", "Modos de corrente",
         "Crescente, decrescente, ímpar, par, livre. No mesmo tabuleiro, "
         "jogadas bem diferentes."),
        ("7", "Itens", "Dica, desfazer, bomba, embaralhar, jogadas extras, "
                      "curinga, pontos duplos."),
    ],
    "shotsT": "Do jogo",
    "shotsS": "",
    "shots": [
        ("Tela de jogo enquanto uma corrente é desenhada",
         "Monte a corrente arrastando o dedo"),
        ("A primeira estrela, conquistada no meio da fase",
         "Três metas de estrela independentes"),
        ("O mapa de fases", "Avance de fase em fase"),
        ("Uma corrente sendo montada enquanto a lava sobe no mundo do vulcão",
         "Cada mundo tem seu próprio clima"),
    ],
    "numoAlt": "Numo, o mascote do Decimo",
    "numoT": "Numo acompanha você pelo caminho",
    "numoP": "Numo comemora quando sua corrente cresce e dá uma dica quando "
             "você empaca. Quando você passa de fase, ninguém comemora mais "
             "do que o Numo.",
    "endT": "Era para ser só uma fase.",
    "endS": "145 fases, 15 mundos. Grátis, nas duas lojas.",
    "family": "Mais da Bardino:",
    "legal": ("Privacidade", "Termos de uso", "Excluir conta"),
    "support": "Suporte",
    "game": "Um jogo da Bardino",
    "noCookies": "Este site não usa cookies e não carrega nada de outros "
                 "servidores.",
}


# ── yollar ──────────────────────────────────────────────────────────────────
#
# URL ile DOSYA ayri (Palmo'daki gibi): URL dizin bicimindedir (/tr/), dosya
# her zaman index.html'dir. Canonical, hreflang ve x-default ayni adresi
# gosteriyor; ayni belge iki adresle isaret edilmiyor.

def path_for(code, page="index.html"):
    """Yayindaki URL yolu (bastaki / olmadan). Acilis sayfasi dizinle biter."""
    d = "" if code == ROOT_LANG else code + "/"
    return d if page == "index.html" else d + page


def file_for(code, page="index.html"):
    """Diskteki dosya yolu."""
    return page if code == ROOT_LANG else "%s/%s" % (code, page)


def langs_with(page):
    """Bu sayfanin gercekten uretildigi diller. Dil cubugu ve hreflang
    yalnizca bunlari listeler: Colmo'da bu filtre yoktu ve her yasal sayfa
    uretilmemis dort sayfaya baglanti veriyordu."""
    if page == "index.html":
        return [c for c, _l, _o, _n, _k in LANGS]
    return [c for c, _l, _o, _n, _k in LANGS if c in LEGAL_LANGS]


def html_lang(code):
    """html lang ve hreflang degeri (pt -> pt-BR)."""
    return dict((c, l) for c, l, _o, _n, _k in LANGS)[code]


def legal_lang(code):
    """Bu dildeki sayfanin yasal baglantilari hangi dile gider."""
    return code if code in LEGAL_LANGS else ROOT_LANG


def has(rel):
    return os.path.exists(os.path.join(HERE, rel.replace("/", os.sep)))


def shot(code, name):
    """Karenin yolu: dilin kendi klasorunde varsa o, yoksa Ingilizce set."""
    d = SHOT_DIRS.get(code)
    if d and has("%s/%s" % (d, name)):
        return "%s/%s" % (d, name)
    return "%s/%s" % (SHOT_DEFAULT, name)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def esc_b(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(s))


def app_store(code):
    return APP_STORE_TR if code == "tr" else APP_STORE


def mail_link(subject=None):
    """Destek adresi, Cloudflare'in dokunmamasi icin email_off icinde.

    Site Cloudflare arkasinda ve Email Address Obfuscation acik: isaretsiz
    bir adres /cdn-cgi/l/email-protection#... baglantisina cevriliyor ve o
    adres JavaScript kapaliyken 404. Sayfadaki HER adres bu fonksiyondan
    gecmeli."""
    href = "mailto:" + SUPPORT_MAIL
    if subject:
        href += "?subject=" + quote(subject)
    return ('<!--email_off--><a href="%s">%s</a><!--/email_off-->'
            % (esc(href), SUPPORT_MAIL))


AYLAR = {
    "en": ("January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"),
    "tr": ("Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
           "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"),
}


def tarih(code, iso):
    """2026-10-14 -> "14 October 2026" / "14 Ekim 2026"."""
    y, m, d = (int(x) for x in iso.split("-"))
    return "%d %s %d" % (d, AYLAR[code][m - 1], y)


# ── iskelet ─────────────────────────────────────────────────────────────────

def head(code, page, title, desc, ogdesc=None, extra=""):
    """Sayfa basi. hreflang yalnizca bu sayfanin GERCEKTEN var oldugu
    dilleri listeler (yasal sayfada EN ve TR); x-default sayfa bazli, yani
    Turkce gizlilik sayfasinin dil-notr karsiligi Ingilizce gizlilik
    sayfasidir, ana sayfa degil.

    Yazi tipi /css/style.css icinde @font-face ile kendi sunucumuzdan geliyor;
    sayfa baska bir sunucudan hicbir sey yuklemiyor (altbilgideki not buna
    dayaniyor, oraya bir CDN eklenirse o cumle de degismeli)."""
    lang = html_lang(code)
    loc = dict((c, o) for c, _l, o, _n, _k in LANGS)[code]
    alts = "\n    ".join(
        '<link rel="alternate" hreflang="%s" href="%s/%s">'
        % (html_lang(c), SITE, path_for(c, page)) for c in langs_with(page))
    alts += ('\n    <link rel="alternate" hreflang="x-default" href="%s/%s">'
             % (SITE, path_for(ROOT_LANG, page)))
    css = '<link rel="stylesheet" href="/css/style.css">'
    if page != "index.html":
        css += '\n    <link rel="stylesheet" href="/css/legal.css">'
    ogdesc = desc if ogdesc is None else ogdesc
    return """<!DOCTYPE html>
<html lang="%(lang)s">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">%(extra)s
    <meta name="description" content="%(desc)s">
    <meta name="robots" content="index, follow">
    <meta property="og:type" content="website">
    <meta property="og:url" content="%(site)s/%(path)s">
    <meta property="og:title" content="%(title)s">
    <meta property="og:description" content="%(ogdesc)s">
    <meta property="og:image" content="%(site)s/%(share)s">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="%(loc)s">
    <meta property="og:site_name" content="%(app)s">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="%(title)s">
    <meta name="twitter:description" content="%(ogdesc)s">
    <meta name="twitter:image" content="%(site)s/%(share)s">
    <meta name="theme-color" content="#2E2C7A">
    <title>%(title)s</title>
    <link rel="canonical" href="%(site)s/%(path)s">
    %(alts)s
    <link rel="icon" type="image/png" href="/%(icon)s">
    <link rel="apple-touch-icon" href="/%(icon)s">
    <link rel="manifest" href="/manifest.json">
    %(css)s
</head>
<body>
""" % dict(lang=lang, loc=loc, desc=esc(desc), ogdesc=esc(ogdesc),
           title=esc(title), site=SITE, path=path_for(code, page), alts=alts,
           share=SHARE, icon=ICON, app=APP, css=css, extra=extra)


def lang_bar(code, t, page="index.html"):
    """Dil secici. Bayrak yok: bayrak dili degil ulkeyi gosterir ve bu
    dillerin hepsi birden cok ulkede konusuluyor (Colmo/Palmo ile ayni).

    Her baglantida iki etiket var: tam ad ve iki harfli kod. Hangisinin
    gorunecegine CSS karar veriyor (dar ekranda kod). Tam ad dar ekranda
    yalnizca gozden gizleniyor, ekran okuyucu yine "Deutsch" okuyor.

    Yalnizca sayfanin var oldugu diller: yasal sayfada EN ve TR."""
    avail = langs_with(page)
    out = []
    for c, l, _o, name, kod in LANGS:
        if c not in avail:
            continue
        cur = ' aria-current="page"' if c == code else ""
        out.append('<a href="/%s" hreflang="%s" lang="%s"%s>'
                   '<span class="kod">%s</span><span class="ad">%s</span></a>'
                   % (path_for(c, page), l, l, cur, kod, esc(name)))
    return ('<div class="diller" role="navigation" aria-label="%s">%s</div>'
            % (esc(t["langsLabel"]), "".join(out)))


def header(code, t, page="index.html"):
    # Capa adlari (#nasil, #icinde, #ekranlar) her dilde ayni: eski Turkce
    # sayfaya verilmis bir #ekranlar baglantisi kirilmasin. Capalar yalnizca
    # acilis sayfasinda; yasal sayfada gidecekleri bolum yok.
    nav = ""
    if page == "index.html":
        a, b, c = t["nav"]
        nav = ("""<nav class="cipa">
            <a href="#nasil">%s</a>
            <a href="#icinde">%s</a>
            <a href="#ekranlar">%s</a>
        </nav>
        """ % (esc(a), esc(b), esc(c)))
    return """<header class="ust">
    <div class="kap">
        <a class="marka" href="/%(home)s">
            <img src="/%(icon)s" alt="Decimo" width="40" height="40">
            <b>Decimo</b>
        </a>
        %(nav)s%(bar)s
    </div>
</header>
""" % dict(home=path_for(code), icon=ICON, nav=nav,
           bar=lang_bar(code, t, page))


PLAY_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.6 2.3c-.3.3-.5.8-.5 1.4v16.6c0 .6.2 1.1.5 1.4l.1.1 9.3-9.3v-.2L3.6 2.3zM17 15.4l-3.1-3.1v-.2L17 9l.1.1 3.7 2.1c1 .6 1 1.6 0 2.2L17 15.4zM16 16.4l-3.2-3.2-9.2 9.2c.4.4 1 .4 1.7 0l10.7-6zM16 8.1L5.3 2.1c-.7-.4-1.3-.4-1.7 0l9.2 9.2L16 8.1z"/></svg>')
APPLE_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.4 12.7c0-2.2 1.8-3.3 1.9-3.4-1-1.5-2.6-1.7-3.2-1.7-1.4-.1-2.7.8-3.3.8-.7 0-1.7-.8-2.8-.8-1.5 0-2.8.8-3.6 2.1-1.5 2.6-.4 6.5 1.1 8.6.7 1 1.6 2.2 2.7 2.2 1.1 0 1.5-.7 2.8-.7 1.3 0 1.6.7 2.8.7 1.2 0 1.9-1 2.6-2.1.8-1.2 1.2-2.4 1.2-2.4s-2.2-.9-2.2-3.3zM14.3 5.9c.6-.7 1-1.7.9-2.7-.9 0-2 .6-2.6 1.3-.6.6-1.1 1.7-.9 2.6 1 .1 2-.5 2.6-1.2z"/></svg>')


def stores(code, campaign):
    """Iki magaza dugmesi. Resmi rozet degil, eski sayfanin hap dugmeleri:
    sayfanin tasarimi onlar uzerine kurulu ve rozetler bu sitede hic
    kullanilmadi. Dugme yazisi marka adi, her dilde ayni."""
    referrer = (UTM + campaign).replace("=", "%3D").replace("&", "%26")
    play = "%s&referrer=%s" % (GOOGLE_PLAY, referrer)
    apple = "%s?%s%s" % (app_store(code), UTM, campaign)
    return """<div class="dugmeler">
                <a class="dugme d-play" href="%(play)s">
                    %(psvg)s
                    Google Play
                </a>
                <a class="dugme d-apple" href="%(apple)s">
                    %(asvg)s
                    App Store
                </a>
            </div>""" % dict(play=esc(play), apple=esc(apple),
                             psvg=PLAY_SVG, asvg=APPLE_SVG)


# ── altbilgi: aile blogu ────────────────────────────────────────────────────
#
# Uc oyun sitesinde (decimo, colmo, palmo) altbilgi AYNI yapida: solda
# Bardino'nun kendi logosu, sagda tek cumle ve iki kardes oyunun karti, en
# altta yasal satir. Yapi ortak, gorunum oyunun (bkz. css/style.css).
# Logo, kardes etiketleri ve adres kurali colmo-site/build.py ile birebir
# ayni; birinde degisirse digerlerine de tasinmali. Logo acilistaki taslu
# kilit ve gorunur olunca ayni filmi oynar (assets/bardino-intro.js).
BARDINO_LOGO = (
    '<svg class="aile-logo bardino-intro" viewBox="0 0 600 150" data-bardino-intro role="img" aria-label="Bardino"><g class="bi-mark"><g transform="translate(0 6) scale(1.12)"><rect x="4.5" y="9.5" width="91" height="87" rx="21" class="bi-ef bi-es" stroke-width="5"/><rect x="4.5" y="3" width="91" height="87" rx="21" fill="#FFC83D" class="bi-es" stroke-width="5"/><g fill="none" stroke="#1B2F4A" stroke-width="11.2" stroke-linecap="round"><path d="M37.1 22.1V68.9"/><circle cx="51.5" cy="54.5" r="14.4"/></g></g></g><g class="bi-word"><g transform="translate(134 8) scale(.62)" fill="none" stroke="currentColor" stroke-width="28" stroke-linecap="round" stroke-linejoin="round"><path d="M16 19V136"/><circle cx="52" cy="100" r="36"/><circle cx="166" cy="100" r="36"/><path d="M202 64V136"/><path d="M252 64V136M252 100A36 36 0 0 1 297.32 65.23"/><circle cx="374" cy="100" r="36"/><path d="M410 19V136"/><path d="M460 64V136"/><path d="M510 64V136M510 100A36 36 0 0 1 582 100V136"/><circle cx="664" cy="100" r="36"/></g></g><g transform="translate(139 112) scale(.65)"><g class="bi-stone"><rect x="2" y="6" width="32" height="32" rx="9" class="bi-ef bi-es" stroke-width="3.5"/><rect x="2" y="2" width="32" height="32" rx="9" fill="#2E2C7A" class="bi-es" stroke-width="3.5"/></g><g class="bi-stone"><rect x="44" y="6" width="32" height="32" rx="9" class="bi-ef bi-es" stroke-width="3.5"/><rect x="44" y="2" width="32" height="32" rx="9" fill="#FF5BA3" class="bi-es" stroke-width="3.5"/></g><g class="bi-stone"><rect x="86" y="6" width="32" height="32" rx="9" class="bi-ef bi-es" stroke-width="3.5"/><rect x="86" y="2" width="32" height="32" rx="9" fill="#ABD7B6" class="bi-es" stroke-width="3.5"/></g></g><g class="bi-dot" transform="translate(419.2 30.94)"><rect x="-9.92" y="-19.84" width="19.84" height="19.84" rx="5.58" fill="#FFC83D" class="bi-es" stroke-width="3.1"/></g></svg>')

# Kardes oyunlarin kisa tanimi: kendi sitelerinin basligindaki slogan
# (colmo-site/build.py KARDES_TAG).
KARDES_TAG = {
    "colmo": {"en": "Fill every jar to the brim",
              "tr": "Kavanozları ağzına kadar doldur",
              "de": "Fülle die Gläser bis zum Rand",
              "fr": "Remplis les bocaux à ras bord",
              "es": "Llena los tarros hasta el borde",
              "pt": "Encha os potes até a borda"},
    "palmo": {"en": "Weave the whole board", "tr": "Bütün tahtayı doku",
              "de": "Webe das ganze Brett", "fr": "Tisse tout le plateau",
              "es": "Teje todo el tablero", "pt": "Teça o tabuleiro inteiro"},
}
KARDES_AD = {"colmo": "Colmo", "palmo": "Palmo"}


def kardes_url(g, code):
    """Kardesin sitesi, ayni dilde: kok Ingilizce, digerleri /<kod>/."""
    return "https://%s.bardino.app/%s" % (g, "" if code == "en" else code + "/")


def footer(code, t):
    """Altbilgi. Uc oyun sitesinde ayni sira (ortak brif, 14.10.2026):

      1. Gizlilik politikasi · Kullanim kosullari · Hesap silme · Destek: adres
      2. Bir Bardino oyunu · telif
      3. Cerez/harici sunucu notu

    Yasal baglantilar sayfanin dilindeki yasal sayfaya gider; yasal sayfasi
    olmayan dil (de/fr/es/pt) Ingilizceye. Sosyal hesaplar yalnizca
    Decimo'da var; ortak satirlari bozmasin diye en sonda ayri satirda."""
    kart = "".join(
        '<li><a href="%s"><img src="/assets/aile/%s.webp" alt="" width="44" '
        'height="44" loading="lazy"><span><b>%s</b><small>%s</small></span>'
        '</a></li>' % (kardes_url(g, code), g, KARDES_AD[g],
                       esc(KARDES_TAG[g][code]))
        for g in ("colmo", "palmo"))
    # bardino.app yalnizca Ingilizce (kok) ve Turkce (/tr/).
    studyo = "https://bardino.app/tr/" if code == "tr" else "https://bardino.app/"
    lc = legal_lang(code)
    # Ayrac ekran okuyucuya okunmuyor; cevresindeki bosluklar satirin dar
    # ekranda kirilabilmesi icin.
    ayrac = ' <span class="f-ayrac" aria-hidden="true">&middot;</span> '
    yasal = ayrac.join(
        '<a href="/%s">%s</a>' % (path_for(lc, f), esc(n))
        for f, n in zip(LEGAL, t["legal"]))
    destek = "%s: %s" % (esc(t["support"]), mail_link())
    sosyal = ayrac.join('<a href="%s">%s</a>' % (esc(u), n) for n, u in SOCIAL)
    return """<footer class="aile">
    <div class="kap aile-ust">
        <a class="aile-marka" href="%(studyo)s">%(logo)s</a>
        <div class="aile-kardes">
            <p>%(family)s</p>
            <ul>%(kart)s</ul>
        </div>
    </div>
    <div class="kap aile-alt">
        <p class="f-satir">%(yasal)s%(ayrac)s%(destek)s</p>
        <p class="f-satir"><a href="%(studyo)s">%(game)s</a>%(ayrac)s&copy; 2026 %(dev)s</p>
        <p class="f-satir f-not">%(nocookie)s</p>
        <p class="f-satir">%(sosyal)s</p>
    </div>
</footer>
""" % dict(studyo=studyo, logo=BARDINO_LOGO, family=esc(t["family"]),
           kart=kart, yasal=yasal, ayrac=ayrac, destek=destek,
           game=esc(t["game"]), dev=DEV, nocookie=esc(t["noCookies"]),
           sosyal=sosyal)


# ── acilis sayfasi ──────────────────────────────────────────────────────────

def landing(code, t):
    """Eski elle yazilmis Turkce sayfanin yapisi, siniflari ve sirasi aynen:
    kahraman, kural (uc adim), ozellikler, vitrin, Numo bandi, kapanis."""
    # Adim taslari kuralin kendisini gosteriyor: 8-9-1 sarmayi anlatiyor,
    # 7-8-9 yalnizca artisi tekrar ederdi.
    taslar = [
        '<span class="tas t1">1</span><span class="ok">→</span>\n'
        '                    <span class="tas t2">2</span><span class="ok">→</span>\n'
        '                    <span class="tas t3">3</span>',
        '<span class="tas t4">8</span><span class="ok">→</span>\n'
        '                    <span class="tas t5">9</span><span class="ok">→</span>\n'
        '                    <span class="tas t6">1</span>',
        '<span class="tas t3">★</span>\n'
        '                    <span class="tas t2">★</span>\n'
        '                    <span class="tas t1">★</span>',
    ]
    steps = "\n".join(
        """            <div class="adim">
                <div class="taslar">
                    %s
                </div>
                <h3>%s</h3>
                <p>%s</p>
            </div>""" % (tas, esc(h), esc_b(p))
        for tas, (h, p) in zip(taslar, t["steps"]))

    feats = "\n".join(
        """            <div class="ozellik">
                <div class="sayi">%s</div>
                <h3>%s</h3>
                <p>%s</p>
            </div>""" % (esc(n), esc(h), esc(p)) for n, h, p in t["feats"])

    shots = "\n".join(
        """            <figure>
                <img src="/%s" alt="%s" width="800" height="1600" loading="lazy">
                <figcaption>%s</figcaption>
            </figure>""" % (shot(code, f), esc(alt), esc(cap))
        for f, (alt, cap) in zip(SHOTS, t["shots"]))

    def alt(s):
        """Bolum alt metni; bossa paragraf hic yazilmaz (bosluk CSS'te)."""
        return ('\n        <p class="bolum-alt">%s</p>' % esc(s)) if s else ""

    body = """
<section class="kahraman">
    <div class="kap">
        <div>
            <h1>%(h1a)s<br><em>%(h1b)s</em></h1>
            <p class="alt">%(lead)s</p>
            %(hero_stores)s
            <p class="kucuk">%(small)s</p>
        </div>
        <div class="telefon">
            <img src="/%(hero)s" alt="%(heroAlt)s" width="800" height="1600" loading="eager">
        </div>
    </div>
</section>

<section id="nasil" class="beyaz-bolum">
    <div class="kap">
        <h2>%(howT)s</h2>%(howS)s
        <div class="adimlar">
%(steps)s
        </div>
    </div>
</section>

<section id="icinde">
    <div class="kap">
        <h2>%(featT)s</h2>%(featS)s
        <div class="ozellikler">
%(feats)s
        </div>
    </div>
</section>

<section id="ekranlar" class="beyaz-bolum">
    <div class="kap">
        <h2>%(shotsT)s</h2>%(shotsS)s
        <div class="vitrin">
%(shots)s
        </div>
    </div>
</section>

<section class="numo-bant">
    <div class="kap">
        <img src="/assets/numo.webp" alt="%(numoAlt)s" width="190" height="190" loading="lazy">
        <div>
            <h2>%(numoT)s</h2>
            <p>%(numoP)s</p>
        </div>
    </div>
</section>

<section class="kapanis">
    <div class="kap">
        <h2>%(endT)s</h2>
        <p class="bolum-alt">%(endS)s</p>
        %(end_stores)s
    </div>
</section>

""" % dict(h1a=esc(t["h1a"]), h1b=esc(t["h1b"]),
           lead=esc(t["lead"]), small=esc(t["small"]),
           hero=shot(code, SHOTS[0]), heroAlt=esc(t["heroAlt"]),
           hero_stores=stores(code, "hero"),
           howT=esc(t["howT"]), howS=alt(t["howS"]), steps=steps,
           featT=esc(t["featT"]), featS=alt(t["featS"]), feats=feats,
           shotsT=esc(t["shotsT"]), shotsS=alt(t["shotsS"]), shots=shots,
           numoAlt=esc(t["numoAlt"]), numoT=esc(t["numoT"]),
           numoP=esc(t["numoP"]),
           endT=esc(t["endT"]), endS=esc(t["endS"]),
           end_stores=stores(code, "cta_band").replace(
               "\n            ", "\n        "))

    same_as = ",\n    ".join('"%s"' % u for u in (
        SOCIAL[0][1], SOCIAL[2][1], SOCIAL[1][1], app_store(code)))
    ld = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MobileApplication",
  "name": "%(app)s",
  "applicationCategory": "GameApplication",
  "operatingSystem": "Android, iOS",
  "url": "%(site)s/%(path)s",
  "inLanguage": "%(lang)s",
  "installUrl": "%(play)s",
  "image": "%(site)s/%(share)s",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "TRY"},
  "publisher": {"@type": "Organization", "name": "%(dev)s"},
  "sameAs": [
    %(same)s
  ]
}
</script>

<script src="/assets/bardino-intro.js" defer></script>
</body>
</html>
""" % dict(app=APP, site=SITE, path=path_for(code), lang=html_lang(code),
           play=GOOGLE_PLAY, share=SHARE, dev=DEV, same=same_as)

    return (head(code, "index.html", t["title"], t["desc"], t["ogdesc"])
            + "\n" + header(code, t) + body + footer(code, t) + ld)


# ── yasal sayfalar ──────────────────────────────────────────────────────────
#
# Govdeler legal_text.py'de. Adresler eskisiyle ayni (kokte Ingilizce),
# Turkce kopyalar /tr/ altinda ayni dosya adiyla.
#
# INGILIZCE SAYFADAKI YONLENDIRME. Uygulamanin actigi adresler dil eki
# tasimiyor (Decimo deposu: shop_screen _AbonelikKosullari, l10n
# privacyPolicyFull; ?lang= ya da #parca yok). Eski tek sayfa tarayicinin
# diline gore aciliyordu, yani Turkce telefondan gelen oyuncu Turkce
# okuyordu. Bu davranis korunuyor: Turkce tarayicidan ve sitenin DISINDAN
# gelen ziyaretci /tr/ kopyasina gider. Siteden gelen (dil cubugunda
# "English"e basan) kalir. ?lang=tr ve #tr de /tr/'ye, ?lang=en burada.
# Arama motoru tarayicisi Turkce dil bildirmedigi icin yonlendirilmez;
# hreflang iki sayfayi zaten birbirine bagliyor.
REDIRECT_TR = """
    <script>
    (function () {
        try {
            var q = location.search, h = location.hash;
            if (/[?&]lang=en\\b/i.test(q)) return;
            var tr = /[?&]lang=tr\\b/i.test(q) || /^#tr$/i.test(h);
            if (!tr) {
                var ref = document.referrer || "";
                var ic = ref.indexOf(location.protocol + "//" + location.host + "/") === 0;
                var dil = (navigator.languages && navigator.languages[0]) || navigator.language || "";
                tr = !ic && /^tr\\b/i.test(dil);
            }
            if (tr) location.replace("/tr/" + location.pathname.replace(/^.*\\//, ""));
        } catch (e) {}
    })();
    </script>"""


def legal(code, t, page, title, desc, body, updated):
    return (head(code, page, "%s - %s" % (title, APP), desc,
                 extra=REDIRECT_TR if code == ROOT_LANG else "")
            + header(code, t, page)
            + """
<main class="legal-page">
    <div class="legal-container">
        <div class="legal-header">
            <h1>%(title)s</h1>
            <p class="legal-updated">%(upd)s: %(date)s</p>
        </div>
        <div class="legal-content">
%(body)s
        </div>
    </div>
</main>

""" % dict(title=esc(title), upd=esc(t["upd"]), date=tarih(code, updated),
           body=body)
            + footer(code, t)
            + '\n<script src="/assets/bardino-intro.js" defer></script>\n'
              '</body>\n</html>\n')


# ── yazma ───────────────────────────────────────────────────────────────────

def write(rel, text):
    p = os.path.join(HERE, rel.replace("/", os.sep))
    d = os.path.dirname(p)
    if d:
        os.makedirs(d, exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(text)
    return rel


def main():
    # Depoya __pycache__ dusmesin: .gitignore yok, derleme yerelde kosuyor.
    sys.dont_write_bytecode = True
    import legal_text

    made = []
    for code, _l, _o, _n, _k in LANGS:
        made.append(write(file_for(code), landing(code, T[code])))
        if code in LEGAL_LANGS:
            sayfalar = legal_text.pages(
                code, mail=mail_link,
                link=lambda page, c=code: "/" + path_for(c, page))
            assert [p for p, _t, _d, _b in sayfalar] == list(LEGAL)
            for page, title, desc, body in sayfalar:
                made.append(write(
                    file_for(code, page),
                    legal(code, T[code], page, title, desc, body,
                          legal_text.UPDATED[page])))

    made.append(write(".nojekyll", ""))
    made.append(write("robots.txt",
                      "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n"
                      % SITE))

    # Sitemap sayfalardan uretiliyor: acilis sayfalari dil listesinden,
    # yasal sayfalar LEGAL x LEGAL_LANGS. indir.html ve tt.html noindex,
    # girmiyor.
    urls = ["  <url><loc>%s/%s</loc></url>\n" % (SITE, path_for(c))
            for c, _l, _o, _n, _k in LANGS]
    urls += ["  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n"
             % (SITE, path_for(c, p), legal_text.UPDATED[p])
             for c in LEGAL_LANGS for p in LEGAL]
    made.append(write("sitemap.xml",
                      '<?xml version="1.0" encoding="UTF-8"?>\n'
                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                      '%s</urlset>\n' % "".join(urls)))

    # Manifest kokun dilinde: start_url "/" artik Ingilizce sayfa. Ikonlar ve
    # renkler elle yazilmis eski manifestle ayni.
    t = T[ROOT_LANG]
    made.append(write("manifest.json",
                      '{\n'
                      '  "name": "Decimo - Number Chain",\n'
                      '  "short_name": "Decimo",\n'
                      '  "description": "%s",\n'
                      '  "start_url": "/",\n'
                      '  "display": "standalone",\n'
                      '  "background_color": "#FDF6F0",\n'
                      '  "theme_color": "#2E2C7A",\n'
                      '  "orientation": "portrait",\n'
                      '  "lang": "%s",\n'
                      '  "icons": [\n'
                      '    {\n'
                      '      "src": "assets/decimo_icon_192.png",\n'
                      '      "sizes": "192x192",\n'
                      '      "type": "image/png",\n'
                      '      "purpose": "any"\n'
                      '    },\n'
                      '    {\n'
                      '      "src": "assets/decimo_icon.png",\n'
                      '      "sizes": "512x512",\n'
                      '      "type": "image/png",\n'
                      '      "purpose": "any"\n'
                      '    }\n'
                      '  ]\n'
                      '}\n' % (t["ogdesc"].replace('"', '\\"'), ROOT_LANG)))

    print("uretilen dosya: %d" % len(made))
    for m in sorted(made):
        print("  " + m)

    # ── derleme sonrasi uyarilar ────────────────────────────────────────
    # Liste is listesidir, hata degil; ama bos degilse sayfa bir seyi
    # gostermiyor demektir.
    warn = []
    cname = os.path.join(HERE, "CNAME")
    if not os.path.exists(cname):
        warn.append("CNAME yok. Icine tek satir yaz: %s" % DOMAIN)
    else:
        got = io.open(cname, encoding="utf-8").read().strip()
        if got != DOMAIN:
            warn.append("CNAME icerigi '%s', DOMAIN ise '%s'" % (got, DOMAIN))
    need = [SHARE, ICON, "assets/decimo_icon_192.png", "assets/numo.webp",
            "assets/aile/colmo.webp", "assets/aile/palmo.webp",
            "css/style.css", "css/legal.css", "assets/fonts/OFL.txt"] + FONTS
    need += sorted(set(shot(c, f) for c, _l, _o, _n, _k in LANGS
                       for f in SHOTS))
    for rel in need:
        if not has(rel):
            warn.append("%s yok: sayfa olu baglanti veriyor" % rel)
    for c, d in SHOT_DIRS.items():
        eksik = [f for f in SHOTS if not has("%s/%s" % (d, f))]
        if eksik:
            warn.append("%s karesi eksik, Ingilizce kare gosteriliyor: %s"
                        % (c, ", ".join(eksik)))
    if warn:
        print("\nyapilacaklar:")
        for w in warn:
            print("  - " + w)


if __name__ == "__main__":
    main()
