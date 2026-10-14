# -*- coding: utf-8 -*-
"""Decimo yasal sayfalarinin govdeleri: gizlilik, kullanim kosullari, hesap
silme. Yalnizca Ingilizce ve Turkce (build.py LEGAL_LANGS). Turkce metin
okura "siz" diye hitap eder (sahibin karari, 14.10.2026); acilis sayfalari
"sen" kaliyor.

HER CUMLE OYUNUN KODUNA DAYANIYOR (Decimo deposu, master ve yayindaki
surum-59 dali, 14.10.2026'da okundu). Metni degistirmeden once kaynagina
bak; kaynagi degisen bir cumle yanlis olur:

  anonim hesap            lib/providers/auth_provider.dart ensureSignedIn
  Google / Apple girisi   lib/services/firebase_service.dart, Apple yalniz
                          iOS'ta (settings_screen _buildAuthTile)
  takma ad, lider tablo   lib/services/leaderboard_service.dart,
                          firestore.rules (skor tablolari herkese acik,
                          users/{uid} yalniz sahibine)
  bulten                  lib/screens/map_screen.dart newsletter_subscribers
  cihaz bilgisi           lib/services/device_profile.dart
  analitik, cokme, riza   lib/services/privacy_service.dart (Ayarlar > Veri
                          Toplama; AEA'da UMP rizasi), game_provider
                          setCustomKeys, auth_provider setUserIdentifier
  bildirim jetonu         lib/services/notification_service.dart
  reklam                  lib/services/ad_service.dart (UMP, ATT,
                          MaxAdContentRating.g)
  Meta                    lib/services/meta_events_service.dart (yalniz
                          Android, riza acikken)
  satin alma              lib/config/iap_config.dart, functions/
                          verify_purchase.js (purchase_receipts),
                          lib/services/revenuecat_service.dart (Android)
  Play Games/Game Center  lib/services/games_service.dart
  hesap silme             firebase_service.deleteAccount,
                          functions/index.js cleanupUserData (makbuzlar
                          silinmiyor, uid'leri "deleted" yapiliyor)
  silme adimlari          lib/screens/profile_screen.dart _buildHesapBolumu,
                          start_screen ust cubuktaki profil simgesi
  abonelik kosullari      l10n subscriptionTerms (24 saat kurali Apple'in)

Tarih degisirse UPDATED'i guncelle; build.py sayfaya ve sitemap'e yaziyor.

Metni 14.10.2026'da bir yapay zeka (Claude) eski yayindaki metinlerden ve
oyunun kodundan yazdi. Kullanim kosullarinin Ingilizcesi o gune kadar hic
yoktu. Bir hukukcu okumadi.
"""

# Metnin ozu degistiginde bu tarih degisir (ortak brif kurali 5).
UPDATED = {
    "privacy-policy.html": "2026-10-14",
    "terms-of-use.html": "2026-10-14",
    "account-deletion.html": "2026-10-14",
}

FIREBASE = "https://firebase.google.com/support/privacy"
ADMOB = "https://policies.google.com/technologies/ads"
GOOGLE = "https://policies.google.com/privacy"
APPLE = "https://www.apple.com/legal/privacy/"
REVENUECAT = "https://www.revenuecat.com/privacy"
META = "https://www.facebook.com/privacy/policy/"


def _a(href, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, text)


# ── Ingilizce ───────────────────────────────────────────────────────────────

EN_PRIVACY = """            <p class="legal-intro">Decimo is a number chain puzzle game made by Bardino Technology. This policy explains what data the app collects, why, and what choices you have.</p>
            <p><strong>Developer:</strong> Bardino Technology (com.bardino.numberchain) &middot; <strong>Contact:</strong> {mail}</p>

            <section class="legal-section">
                <h2>1. Data we collect</h2>
                <p>We collect what is needed to run the game, save your progress, fix crashes, show ads and measure our own advertising.</p>
                <ul>
                    <li><strong>Automatic account:</strong> on first launch the app creates an anonymous account (Firebase Authentication) with a random identifier. Your progress is saved to our cloud database under this account, and leaderboards use it. It contains no name or e-mail address, and you do not have to sign in for it.</li>
                    <li><strong>Sign-in (optional):</strong> if you sign in with Google (or with Apple on iOS), we receive the e-mail address, name and account identifier that the provider shares, and with Google the address of your profile photo. Your progress is then linked to that account so you can continue on another device. You can play without signing in.</li>
                    <li><strong>Nickname and leaderboards:</strong> the game gives you a nickname, which you can change. When you appear on a leaderboard or in a tournament, that nickname and your score are <strong>visible to other players</strong>. Your real Google or Apple name is never published.</li>
                    <li><strong>Newsletter (optional):</strong> if you enter your e-mail address in the in-game newsletter field, we store it only to tell you about updates. It is not required to play.</li>
                    <li><strong>Game progress and statistics:</strong> levels completed, stars, coins, gems, purchases, settings and play statistics. Stored on your device and in our cloud database (Firebase Firestore), whether or not you sign in.</li>
                    <li><strong>Device information:</strong> device model, operating system and app version, the device's language and region setting, time zone, the Firebase Analytics app instance ID and, on iOS, the identifier for vendor. Stored with your account record. The region comes from your device settings; the app does not ask for your location.</li>
                    <li><strong>Usage and analytics:</strong> in-game events (for example level started, completed or failed, power-ups used), session information and basic device information, via Firebase Analytics. Used in aggregate to balance and improve the game.</li>
                    <li><strong>Crash diagnostics:</strong> crash logs, the state of the device at the time of a crash, the level being played and your account's random identifier, via Firebase Crashlytics.</li>
                    <li><strong>Notifications:</strong> the app stores a push notification token for your device (Firebase Cloud Messaging) with your account. Notifications are shown only if you allow them.</li>
                    <li><strong>Advertising:</strong> ads are served by Google AdMob. Depending on your consent, ads may use your device's advertising identifier. Where consent is required (for example in the EEA and the UK) we ask for it before showing ads. On iOS the advertising identifier is only available if you allow tracking when the app asks. Ad content is limited to the G rating.</li>
                    <li><strong>Ad measurement on Android:</strong> while data collection is on (see section 5), the Android app sends a few events to Meta through the Meta (Facebook) SDK so that we can measure our ads on Facebook and Instagram: app installs and launches, finishing the tutorial, winning the first level, purchases (amount and currency) and ad impressions with their value. The Meta SDK may also receive your advertising identifier. The iOS app sends nothing to Meta.</li>
                    <li><strong>Purchases:</strong> in-app purchases are processed by Apple (App Store) or Google (Google Play). We do not receive your card details. We receive a purchase confirmation, which our server checks with Apple or Google before delivering the item, and we keep a record of each purchase (product, order number, date). On Android, subscriptions and the Remove Ads purchase are also managed through RevenueCat, which receives the purchase details and your account's random identifier.</li>
                    <li><strong>Achievements and platform leaderboards:</strong> if you are signed in to Google Play Games (Android) or Game Center (iOS), the game sends your achievements and scores there. How they are shown depends on that service's own settings.</li>
                </ul>
                <p><strong>We do not sell your personal data.</strong></p>
            </section>

            <section class="legal-section">
                <h2>2. Why we use it</h2>
                <ul>
                    <li>To provide and save your game progress, and to let you continue on another device when you sign in.</li>
                    <li>To run leaderboards, tournaments and the daily puzzle.</li>
                    <li>To diagnose crashes and fix bugs.</li>
                    <li>To understand usage in aggregate, balance difficulty and improve the game.</li>
                    <li>To send the notifications you allowed.</li>
                    <li>To show the ads that keep the game free, measure our own advertising and process optional purchases.</li>
                </ul>
            </section>

            <section class="legal-section">
                <h2>3. Third-party services</h2>
                <p>These providers process data on our behalf under their own terms and policies:</p>
                <ul>
                    <li>{firebase} (Authentication, Firestore, Cloud Functions, Analytics, Crashlytics, Cloud Messaging, Remote Config, App Check)</li>
                    <li>{admob} (advertising)</li>
                    <li>{google} (Google Play purchases, Sign in with Google, Google Play Games)</li>
                    <li>{apple} (App Store purchases, Sign in with Apple, Game Center)</li>
                    <li>{revenuecat} (purchases on Android)</li>
                    <li>{meta} (ad measurement on Android)</li>
                </ul>
            </section>

            <section class="legal-section">
                <h2>4. Retention and deletion</h2>
                <ul>
                    <li>Local data stays on your device until you uninstall the app or clear its data.</li>
                    <li>Cloud data is kept while your account exists, including the automatic anonymous account. Uninstalling the app does not delete it.</li>
                    <li>You can delete your account and its data in the app: <strong>Profile &gt; Delete Account</strong>. This deletes your cloud progress, account record, coins and gems, purchase history, scores (including past daily and tournament entries), push tokens and newsletter address, clears the game data on your device and signs you out. Purchase records are kept without your account identifier, because they stop the same purchase from being redeemed twice. Details: <a href="{deletion}">Account deletion</a>.</li>
                    <li>Data already sent to Firebase Analytics, Crashlytics, AdMob or Meta is kept by those services for their own retention periods.</li>
                </ul>
            </section>

            <section class="legal-section">
                <h2>5. Your choices</h2>
                <ul>
                    <li>Play without signing in if you do not want to share your e-mail address and name. Your progress is still saved under the anonymous account.</li>
                    <li>Turn off usage statistics, crash reports and, on Android, ad measurement in <strong>Settings &gt; Data Collection</strong>.</li>
                    <li>Change your ad consent in <strong>Settings &gt; Ad privacy options</strong>, which appears where the consent form applies.</li>
                    <li>Reset your advertising identifier or limit ad tracking in your device settings; on iOS you can also turn off tracking for Decimo.</li>
                    <li>Turn off notifications in the game's settings or in your device settings.</li>
                    <li>Delete your account and data at any time (see section 4).</li>
                </ul>
            </section>

            <section class="legal-section">
                <h2>6. Children</h2>
                <p>Decimo is intended for a general audience and is not directed to children under 13. We do not knowingly collect data from children under 13. If you believe a child has given us data, contact us and we will delete it.</p>
            </section>

            <section class="legal-section">
                <h2>7. Security and changes</h2>
                <p>We use industry-standard measures (encrypted transport, Google Cloud infrastructure). No method is 100% secure, but we work to protect your data. We may update this policy; material changes will be posted here with a new "last updated" date.</p>
            </section>

            <section class="legal-section">
                <h2>8. Contact</h2>
                <div class="legal-contact">
                    <p><strong>Bardino Technology</strong></p>
                    <p>E-mail: {mail}</p>
                    <p>Web: <a href="https://decimo.bardino.app/">decimo.bardino.app</a></p>
                </div>
            </section>"""

EN_TERMS = """            <p class="legal-intro">By downloading or using Decimo ("the app") you agree to these terms. The app is provided by Bardino Technology.</p>

            <section class="legal-section">
                <h2>1. License</h2>
                <p>We grant you a limited, non-exclusive, non-transferable license to use the app for personal, non-commercial purposes. You may not reverse engineer, copy or misuse the app.</p>
            </section>

            <section class="legal-section">
                <h2>2. In-app purchases</h2>
                <p>Decimo is free to download and play. You can buy the following in the app:</p>
                <ul>
                    <li><strong>Coin packs:</strong> coins and gems to use in the game.</li>
                    <li><strong>Special offers:</strong> a starter pack during your first seven days, and a refill of lives.</li>
                    <li><strong>Remove Ads:</strong> a one-time purchase that turns off the full-screen ads between levels. Optional rewarded ads stay available.</li>
                    <li><strong>VIP subscription:</strong> monthly or yearly, with the benefits listed in the shop.</li>
                </ul>
                <p>Payment is handled by Apple (App Store) or Google (Google Play) and is subject to their terms. The price is shown in the shop before you buy. We do not see or store your card details.</p>
                <h3>Subscriptions</h3>
                <p>A VIP subscription lasts one month or one year and renews automatically at the end of each period until you cancel it. On the App Store, cancel at least 24 hours before the period ends to avoid the next charge; Apple charges the renewal within the 24 hours before the period ends. You can manage or cancel the subscription in your App Store or Google Play account settings. Deleting the app or your Decimo account does not cancel it.</p>
                <h3>Refunds and restoring</h3>
                <p>Refund requests are handled by Apple or Google under their refund policies. Coins, gems, lives and power-ups have no cash value and cannot be exchanged for money. Remove Ads and an active subscription can be restored with <strong>Restore Purchases</strong> in the shop. If you delete your Decimo account, the coins, gems and progress in it are deleted too. Your statutory rights are not affected.</p>
            </section>

            <section class="legal-section">
                <h2>3. Ads</h2>
                <p>The app shows ads through Google AdMob: rewarded ads that you choose to watch, and full-screen ads between levels. Remove Ads or an active VIP subscription turns off the ads between levels. The <a href="{privacy}">Privacy policy</a> explains what data ads use.</p>
            </section>

            <section class="legal-section">
                <h2>4. Disclaimer</h2>
                <p>The app is provided "as is". We do not guarantee that it will run without interruption or errors. To the extent permitted by applicable law, we are not liable for indirect damages arising from the use of the app.</p>
            </section>

            <section class="legal-section">
                <h2>5. Changes and contact</h2>
                <p>We may update these terms. For questions: {mail}</p>
            </section>"""

EN_DELETION = """            <p class="legal-intro">This page explains how to permanently delete your <strong>Decimo</strong> (com.bardino.numberchain) account and its data. Deletion cannot be undone.</p>
            <p>Every player has an account, even without signing in: the app creates an anonymous account on first launch and saves your progress to our servers under it.</p>

            <section class="legal-section">
                <h2>1. Delete in the app (recommended)</h2>
                <p>Deletion takes effect immediately:</p>
                <div class="steps-deletion">
                    <div class="step-del">Open Decimo and tap the profile icon at the top of the main screen.</div>
                    <div class="step-del">In the <strong>Account</strong> section, tap <strong>Delete Account</strong>.</div>
                    <div class="step-del">Confirm in the dialog.</div>
                </div>
                <p>Your account and its data are deleted and you are signed out. If you signed in with Google or Apple, you may be asked to sign in again to confirm that it is you.</p>
            </section>

            <section class="legal-section">
                <h2>2. Request deletion by e-mail</h2>
                <p>If you cannot open the app, you can send a deletion request by e-mail:</p>
                <ul>
                    <li>If you signed in with Google or Apple, write from that e-mail address or include it in the message.</li>
                    <li>If you never signed in, include your in-game nickname so that we can find the account.</li>
                    <li>Use the subject line <strong>"Decimo Account Deletion Request"</strong> and send it to {mail_del}.</li>
                </ul>
                <p>E-mail requests are processed within <strong>7 business days</strong>.</p>
            </section>

            <section class="legal-section">
                <h2>3. Data that is deleted</h2>
                <ul>
                    <li><strong>Account record:</strong> the account identifier and, if you signed in, your e-mail address and name (Firebase Authentication).</li>
                    <li><strong>Cloud save:</strong> levels, stars, coins, gems, settings, statistics, purchase history and device information (Firebase Firestore).</li>
                    <li><strong>Scores:</strong> your leaderboard entries, including past daily and tournament entries.</li>
                    <li><strong>Other:</strong> push notification tokens and your newsletter address.</li>
                    <li><strong>On your device:</strong> the game's progress, your nickname and the saved name and e-mail address.</li>
                </ul>
                <div class="callout">
                    <p>Uninstalling the app removes the data on your device, but not your account on our servers. Use Delete Account for that.</p>
                </div>
            </section>

            <section class="legal-section">
                <h2>4. Data that may be kept</h2>
                <ul>
                    <li><strong>Purchase records:</strong> kept without your account identifier, because they stop the same purchase from being redeemed twice. Apple and Google keep their own payment records.</li>
                    <li><strong>Crash reports and usage statistics:</strong> those already sent to Firebase Crashlytics and Analytics stay there for those services' retention periods. They do not contain your name or e-mail address.</li>
                    <li><strong>Achievements and scores</strong> sent to Google Play Games or Game Center belong to your profile in that service and are managed there.</li>
                </ul>
            </section>

            <section class="legal-section">
                <h2>5. Contact</h2>
                <div class="legal-contact">
                    <p><strong>Bardino Technology</strong></p>
                    <p>E-mail: {mail}</p>
                    <p>Web: <a href="https://decimo.bardino.app/">decimo.bardino.app</a></p>
                </div>
            </section>"""


# ── Turkce ──────────────────────────────────────────────────────────────────

TR_PRIVACY = """            <p class="legal-intro">Decimo, Bardino Technology'nin geliştirdiği bir sayı zinciri bulmaca oyunudur. Bu politika, uygulamanın hangi verileri neden topladığını ve hangi seçeneklere sahip olduğunuzu açıklar.</p>
            <p><strong>Geliştirici:</strong> Bardino Technology (com.bardino.numberchain) &middot; <strong>İletişim:</strong> {mail}</p>

            <section class="legal-section">
                <h2>1. Topladığımız veriler</h2>
                <p>Oyunu çalıştırmak, ilerlemenizi kaydetmek, çökmeleri düzeltmek, reklam göstermek ve kendi reklamlarımızı ölçmek için gereken veriyi toplarız.</p>
                <ul>
                    <li><strong>Otomatik hesap:</strong> uygulama ilk açılışta rastgele bir kimlik taşıyan anonim bir hesap (Firebase Authentication) oluşturur. İlerlemeniz bu hesapla bulut veritabanımıza kaydedilir, lider tabloları da bu hesabı kullanır. Hesapta adınız veya e-posta adresiniz yoktur ve bunun için giriş yapmanız gerekmez.</li>
                    <li><strong>Giriş (isteğe bağlı):</strong> Google ile (iOS'ta Apple ile de) giriş yaparsanız sağlayıcının paylaştığı e-posta adresinizi, adınızı ve hesap kimliğinizi, Google ile girişte ayrıca profil fotoğrafınızın adresini alırız. İlerlemeniz bu hesaba bağlanır ve başka bir cihazda devam edebilirsiniz. Giriş yapmadan da oynayabilirsiniz.</li>
                    <li><strong>Takma ad ve lider tabloları:</strong> oyun size bir takma ad verir, bunu değiştirebilirsiniz. Bir lider tablosunda veya turnuvada yer aldığınızda takma adınız ve skorunuz <strong>diğer oyunculara açık şekilde</strong> görünür. Gerçek Google veya Apple adınız hiçbir zaman yayınlanmaz.</li>
                    <li><strong>Bülten (isteğe bağlı):</strong> oyun içindeki bülten alanına e-posta adresinizi girerseniz, yalnızca güncellemelerden haberdar etmek için saklarız. Oynamak için gerekmez.</li>
                    <li><strong>Oyun ilerlemesi ve istatistikler:</strong> tamamlanan bölümler, yıldızlar, altın, elmas, satın almalar, ayarlar ve oyun istatistikleri. Giriş yapıp yapmadığınızdan bağımsız olarak cihazınızda ve bulut veritabanımızda (Firebase Firestore) saklanır.</li>
                    <li><strong>Cihaz bilgisi:</strong> cihaz modeli, işletim sistemi ve uygulama sürümü, cihazın dil ve bölge ayarı, saat dilimi, Firebase Analytics'in uygulama kurulum kimliği (app instance ID) ve iOS'ta satıcıya özel cihaz kimliği (identifier for vendor). Hesap kaydınızla birlikte saklanır. Bölge bilgisi cihaz ayarlarınızdan gelir; uygulama konum izni istemez.</li>
                    <li><strong>Kullanım ve analitik:</strong> oyun içi olaylar (örneğin bölüm başlatma, tamamlama, kaybetme, güçlendirme kullanımı), oturum bilgisi ve temel cihaz bilgisi, Firebase Analytics aracılığıyla. Oyunu dengelemek ve geliştirmek için toplu olarak kullanılır.</li>
                    <li><strong>Çökme tanılaması:</strong> çökme kayıtları, çökme anındaki cihaz durumu, o sırada oynanan bölüm ve hesabınızın rastgele kimliği, Firebase Crashlytics aracılığıyla.</li>
                    <li><strong>Bildirimler:</strong> uygulama, cihazınızın anlık bildirim jetonunu (Firebase Cloud Messaging) hesabınızla birlikte saklar. Bildirimler yalnızca izin verirseniz gösterilir.</li>
                    <li><strong>Reklam:</strong> reklamlar Google AdMob tarafından sunulur. Onay tercihinize bağlı olarak reklamlar cihazınızın reklam kimliğini kullanabilir. Onayın gerektiği yerlerde (örneğin AEA ve Birleşik Krallık) reklam göstermeden önce onayınızı isteriz. iOS'ta reklam kimliği yalnızca uygulama sorduğunda izlemeye izin verirseniz kullanılabilir. Reklam içeriği "G" derecesiyle sınırlıdır.</li>
                    <li><strong>Android'de reklam ölçümü:</strong> veri toplama açıkken (bkz. madde 5) Android uygulaması, Facebook ve Instagram'daki reklamlarımızı ölçebilmemiz için Meta (Facebook) SDK'sı üzerinden Meta'ya birkaç olay gönderir: uygulamanın yüklenmesi ve açılması, eğitimin bitirilmesi, ilk bölümün kazanılması, satın almalar (tutar ve para birimi) ve reklam gösterimleri ile değerleri. Meta SDK'sı reklam kimliğinizi de alabilir. iOS uygulaması Meta'ya hiçbir şey göndermez.</li>
                    <li><strong>Satın almalar:</strong> uygulama içi satın almalar Apple (App Store) veya Google (Google Play) tarafından işlenir. Kart bilgilerinizi almayız. Bir satın alma onayı alırız; sunucumuz ürünü teslim etmeden önce bunu Apple veya Google ile doğrular ve her satın almanın kaydını (ürün, sipariş numarası, tarih) saklarız. Android'de abonelikler ve Reklamsız satın alımı ayrıca RevenueCat üzerinden yönetilir; RevenueCat satın alma bilgisini ve hesabınızın rastgele kimliğini alır.</li>
                    <li><strong>Başarımlar ve platform lider tabloları:</strong> Google Play Games'e (Android) veya Game Center'a (iOS) giriş yapmışsanız oyun başarımlarınızı ve skorlarınızı oraya gönderir. Bunların orada nasıl görüneceği o hizmetin kendi ayarlarına bağlıdır.</li>
                </ul>
                <p><strong>Kişisel verilerinizi satmayız.</strong></p>
            </section>

            <section class="legal-section">
                <h2>2. Kullanım amaçları</h2>
                <ul>
                    <li>Oyun ilerlemenizi sağlamak ve kaydetmek; giriş yaptığınızda başka bir cihazda devam etmenizi sağlamak.</li>
                    <li>Lider tablolarını, turnuvaları ve günlük bulmacayı çalıştırmak.</li>
                    <li>Çökmeleri tanılamak ve hataları düzeltmek.</li>
                    <li>Kullanımı toplu olarak anlamak, zorluğu dengelemek ve oyunu geliştirmek.</li>
                    <li>İzin verdiğiniz bildirimleri göndermek.</li>
                    <li>Oyunu ücretsiz tutan reklamları göstermek, kendi reklamlarımızı ölçmek ve isteğe bağlı satın almaları işlemek.</li>
                </ul>
            </section>

            <section class="legal-section">
                <h2>3. Üçüncü taraf hizmetleri</h2>
                <p>Bu sağlayıcılar verileri kendi koşul ve politikaları kapsamında bizim adımıza işler:</p>
                <ul>
                    <li>{firebase} (Authentication, Firestore, Cloud Functions, Analytics, Crashlytics, Cloud Messaging, Remote Config, App Check)</li>
                    <li>{admob} (reklam)</li>
                    <li>{google} (Google Play satın almaları, Google ile giriş, Google Play Games)</li>
                    <li>{apple} (App Store satın almaları, Apple ile giriş, Game Center)</li>
                    <li>{revenuecat} (Android'de satın almalar)</li>
                    <li>{meta} (Android'de reklam ölçümü)</li>
                </ul>
            </section>

            <section class="legal-section">
                <h2>4. Saklama ve silme</h2>
                <ul>
                    <li>Yerel veriler, uygulamayı kaldırana veya uygulama verisini temizleyene kadar cihazınızda kalır.</li>
                    <li>Bulut verisi, otomatik anonim hesap dahil, hesabınız var oldukça saklanır. Uygulamayı kaldırmak bu veriyi silmez.</li>
                    <li>Hesabınızı ve verilerinizi uygulama içinden silebilirsiniz: <strong>Profil &gt; Hesabı Sil</strong>. Bu işlem bulut ilerlemenizi, hesap kaydınızı, altın ve elmaslarınızı, satın alma geçmişinizi, skorlarınızı (geçmiş günlük ve turnuva kayıtları dahil), bildirim jetonlarınızı ve bülten adresinizi siler, cihazınızdaki oyun verisini temizler ve oturumunuzu kapatır. Satın alma kayıtları hesap kimliğiniz çıkarılarak saklanır; aynı satın almanın ikinci kez kullanılmasını engellerler. Ayrıntılar: <a href="{deletion}">Hesap silme</a>.</li>
                    <li>Firebase Analytics, Crashlytics, AdMob veya Meta'ya daha önce gönderilmiş veriler, bu hizmetlerin kendi saklama süreleri boyunca onlarda kalır.</li>
                </ul>
            </section>

            <section class="legal-section">
                <h2>5. Tercihleriniz</h2>
                <ul>
                    <li>E-posta adresinizi ve adınızı paylaşmak istemiyorsanız giriş yapmadan oynayın. İlerlemeniz yine anonim hesapla kaydedilir.</li>
                    <li>Kullanım istatistiklerini, çökme raporlarını ve Android'de reklam ölçümünü <strong>Ayarlar &gt; Veri Toplama</strong> ile kapatabilirsiniz.</li>
                    <li>Reklam onayınızı, onay formunun geçerli olduğu yerlerde görünen <strong>Ayarlar &gt; Reklam gizlilik seçenekleri</strong> ile değiştirebilirsiniz.</li>
                    <li>Reklam kimliğinizi cihaz ayarlarınızdan sıfırlayabilir veya reklam takibini sınırlayabilirsiniz; iOS'ta Decimo için izlemeyi de kapatabilirsiniz.</li>
                    <li>Bildirimleri oyunun ayarlarından veya cihaz ayarlarınızdan kapatabilirsiniz.</li>
                    <li>Hesabınızı ve verilerinizi istediğiniz zaman silebilirsiniz (bkz. madde 4).</li>
                </ul>
            </section>

            <section class="legal-section">
                <h2>6. Çocuklar</h2>
                <p>Decimo genel kitleye yöneliktir ve 13 yaş altı çocuklara yönelik değildir. Bilerek 13 yaş altı çocuklardan veri toplamayız. Bir çocuğun bize veri verdiğini düşünüyorsanız bize yazın, sileriz.</p>
            </section>

            <section class="legal-section">
                <h2>7. Güvenlik ve değişiklikler</h2>
                <p>Sektör standardı önlemler kullanırız (şifreli aktarım, Google Cloud altyapısı). Hiçbir yöntem %100 güvenli değildir, ancak verinizi korumak için çalışırız. Bu politikayı güncelleyebiliriz; önemli değişiklikler yeni bir "son güncelleme" tarihiyle burada yayımlanır.</p>
            </section>

            <section class="legal-section">
                <h2>8. İletişim</h2>
                <div class="legal-contact">
                    <p><strong>Bardino Technology</strong></p>
                    <p>E-posta: {mail}</p>
                    <p>Web: <a href="https://decimo.bardino.app/tr/">decimo.bardino.app</a></p>
                </div>
            </section>"""

TR_TERMS = """            <p class="legal-intro">Decimo'yu ("uygulama") indirerek veya kullanarak bu koşulları kabul etmiş olursunuz. Uygulama Bardino Technology tarafından sağlanır.</p>

            <section class="legal-section">
                <h2>1. Lisans</h2>
                <p>Size, uygulamayı kişisel ve ticari olmayan amaçlarla kullanmanız için sınırlı, münhasır olmayan ve devredilemez bir lisans veriyoruz. Uygulama üzerinde tersine mühendislik yapamaz, uygulamayı kopyalayamaz veya kötüye kullanamazsınız.</p>
            </section>

            <section class="legal-section">
                <h2>2. Uygulama içi satın almalar</h2>
                <p>Decimo'yu indirmek ve oynamak ücretsizdir. Uygulamada şunları satın alabilirsiniz:</p>
                <ul>
                    <li><strong>Altın paketleri:</strong> oyunda kullanılan altın ve elmas.</li>
                    <li><strong>Özel teklifler:</strong> ilk yedi gününüzde başlangıç paketi ve can yenileme.</li>
                    <li><strong>Reklamsız:</strong> bölüm aralarında çıkan tam ekran reklamları kapatan tek seferlik satın alma. İsteğe bağlı ödüllü reklamlar kullanılabilir kalır.</li>
                    <li><strong>VIP abonelik:</strong> aylık veya yıllık; avantajları oyun içi mağazada listelenir.</li>
                </ul>
                <p>Ödemeler Apple (App Store) veya Google (Google Play) üzerinden alınır ve onların koşullarına tabidir. Fiyat, satın almadan önce oyun içi mağazada gösterilir. Kart bilgilerinizi görmeyiz ve saklamayız.</p>
                <h3>Abonelikler</h3>
                <p>VIP abonelik bir ay veya bir yıl sürer ve iptal edilene kadar her dönemin sonunda otomatik olarak yenilenir. App Store'da bir sonraki ücretin alınmaması için dönem bitiminden en az 24 saat önce iptal etmeniz gerekir; Apple yenileme ücretini dönem bitiminden önceki 24 saat içinde tahsil eder. Aboneliğinizi App Store veya Google Play hesap ayarlarınızdan yönetebilir ya da iptal edebilirsiniz. Uygulamayı ya da Decimo hesabınızı silmek aboneliği iptal etmez.</p>
                <h3>İade ve geri yükleme</h3>
                <p>İade talepleri Apple veya Google tarafından, kendi iade politikalarına göre değerlendirilir. Altın, elmas, can ve güçlendirmelerin nakit değeri yoktur ve paraya çevrilemez. Reklamsız satın alımı ve etkin bir abonelik, oyun içi mağazadaki <strong>Satın Alımları Geri Yükle</strong> ile geri yüklenebilir. Decimo hesabınızı silerseniz içindeki altın, elmas ve ilerleme de silinir. Yasal haklarınız saklıdır.</p>
            </section>

            <section class="legal-section">
                <h2>3. Reklamlar</h2>
                <p>Uygulama Google AdMob üzerinden reklam gösterir: ödül için kendi isteğinizle izlediğiniz reklamlar ve bölüm aralarında çıkan tam ekran reklamlar. Bölüm aralarındaki reklamları Reklamsız satın alımı veya etkin bir VIP abonelik kapatır. Reklamların hangi verileri kullandığı <a href="{privacy}">Gizlilik politikası</a>'nda açıklanır.</p>
            </section>

            <section class="legal-section">
                <h2>4. Sorumluluk reddi</h2>
                <p>Uygulama "olduğu gibi" sunulur. Kesintisiz veya hatasız çalışacağına dair garanti vermeyiz. Yürürlükteki yasaların izin verdiği ölçüde, uygulamanın kullanımından doğan dolaylı zararlardan sorumlu değiliz.</p>
            </section>

            <section class="legal-section">
                <h2>5. Değişiklikler ve iletişim</h2>
                <p>Bu koşulları güncelleyebiliriz. Sorularınız için: {mail}</p>
            </section>"""

TR_DELETION = """            <p class="legal-intro">Bu sayfa, <strong>Decimo</strong> (com.bardino.numberchain) hesabınızı ve verilerinizi kalıcı olarak nasıl silebileceğinizi açıklar. Silme işlemi geri alınamaz.</p>
            <p>Giriş yapmamış olsanız da bir hesabınız vardır: uygulama ilk açılışta anonim bir hesap oluşturur ve ilerlemenizi bu hesapla sunucularımıza kaydeder.</p>

            <section class="legal-section">
                <h2>1. Uygulama içinden silme (önerilen)</h2>
                <p>Silme işlemi hemen gerçekleşir:</p>
                <div class="steps-deletion">
                    <div class="step-del">Decimo'yu açın ve ana ekranın üstündeki profil simgesine dokunun.</div>
                    <div class="step-del"><strong>Hesap</strong> bölümünde <strong>Hesabı Sil</strong>'e dokunun.</div>
                    <div class="step-del">Açılan pencerede silmeyi onaylayın.</div>
                </div>
                <p>Hesabınız ve verileriniz silinir, oturumunuz kapatılır. Google veya Apple ile giriş yaptıysanız, kimliğinizi doğrulamak için yeniden giriş yapmanız istenebilir.</p>
            </section>

            <section class="legal-section">
                <h2>2. E-postayla silme talebi</h2>
                <p>Uygulamayı açamıyorsanız silme talebinizi e-postayla iletebilirsiniz:</p>
                <ul>
                    <li>Google veya Apple ile giriş yaptıysanız o e-posta adresinden yazın ya da adresi mesajda belirtin.</li>
                    <li>Hiç giriş yapmadıysanız, hesabı bulabilmemiz için oyun içi takma adınızı yazın.</li>
                    <li>Konu satırına <strong>"Decimo Hesap Silme Talebi"</strong> yazıp {mail_del} adresine gönderin.</li>
                </ul>
                <p>E-postayla gelen talepler en geç <strong>7 iş günü</strong> içinde işleme alınır.</p>
            </section>

            <section class="legal-section">
                <h2>3. Silinen veriler</h2>
                <ul>
                    <li><strong>Hesap kaydı:</strong> hesap kimliği ve giriş yaptıysanız e-posta adresiniz ile adınız (Firebase Authentication).</li>
                    <li><strong>Bulut kaydı:</strong> bölümler, yıldızlar, altın, elmas, ayarlar, istatistikler, satın alma geçmişi ve cihaz bilgisi (Firebase Firestore).</li>
                    <li><strong>Skorlar:</strong> lider tablolarındaki kayıtlarınız, geçmiş günlük ve turnuva kayıtları dahil.</li>
                    <li><strong>Diğer:</strong> bildirim jetonları ve bülten adresiniz.</li>
                    <li><strong>Cihazınızda:</strong> oyun ilerlemesi, takma adınız ve kayıtlı ad ile e-posta adresi.</li>
                </ul>
                <div class="callout">
                    <p>Uygulamayı kaldırmak cihazınızdaki veriyi siler, sunucularımızdaki hesabınızı silmez. Bunun için Hesabı Sil'i kullanın.</p>
                </div>
            </section>

            <section class="legal-section">
                <h2>4. Saklanabilecek veriler</h2>
                <ul>
                    <li><strong>Satın alma kayıtları:</strong> hesap kimliğiniz çıkarılarak saklanır; aynı satın almanın ikinci kez kullanılmasını engellerler. Apple ve Google kendi ödeme kayıtlarını ayrıca saklar.</li>
                    <li><strong>Çökme raporları ve kullanım istatistikleri:</strong> Firebase Crashlytics ve Analytics'e daha önce gönderilmiş olanlar, bu hizmetlerin saklama süreleri boyunca orada kalır. Adınızı veya e-posta adresinizi içermezler.</li>
                    <li><strong>Başarımlar ve skorlar:</strong> Google Play Games'e veya Game Center'a gönderilenler o hizmetteki profilinize aittir ve oradan yönetilir.</li>
                </ul>
            </section>

            <section class="legal-section">
                <h2>5. İletişim</h2>
                <div class="legal-contact">
                    <p><strong>Bardino Technology</strong></p>
                    <p>E-posta: {mail}</p>
                    <p>Web: <a href="https://decimo.bardino.app/tr/">decimo.bardino.app</a></p>
                </div>
            </section>"""


TEXT = {
    "en": [
        ("privacy-policy.html", "Privacy policy",
         "What data Decimo collects, why, which services process it, and how "
         "to delete it.", EN_PRIVACY),
        ("terms-of-use.html", "Terms of use",
         "Terms for using Decimo, including in-app purchases, subscriptions "
         "and ads.", EN_TERMS),
        ("account-deletion.html", "Account deletion",
         "How to delete your Decimo account and its data, in the app or by "
         "e-mail.", EN_DELETION),
    ],
    "tr": [
        ("privacy-policy.html", "Gizlilik politikası",
         "Decimo'nun hangi verileri neden topladığı, hangi hizmetlerin "
         "işlediği ve verilerinizi nasıl silebileceğiniz.", TR_PRIVACY),
        ("terms-of-use.html", "Kullanım koşulları",
         "Decimo'yu kullanma koşulları: uygulama içi satın almalar, "
         "abonelikler ve reklamlar.", TR_TERMS),
        ("account-deletion.html", "Hesap silme",
         "Decimo hesabınızı ve verilerinizi uygulama içinden veya e-postayla "
         "nasıl silebileceğiniz.", TR_DELETION),
    ],
}

DELETION_SUBJECT = {
    "en": "Decimo Account Deletion Request",
    "tr": "Decimo Hesap Silme Talebi",
}


def pages(code, mail, link):
    """[(dosya, baslik, aciklama, govde_html)], build.LEGAL sirasiyla.

    mail(subject=None): email_off'lu adres baglantisi (build.mail_link).
    link(page): bu dildeki yasal sayfanin adresi ("/tr/account-deletion.html").
    """
    alanlar = dict(
        mail=mail(),
        mail_del=mail(DELETION_SUBJECT[code]),
        deletion=link("account-deletion.html"),
        privacy=link("privacy-policy.html"),
        firebase=_a(FIREBASE, "Google Firebase"),
        admob=_a(ADMOB, "Google AdMob"),
        google=_a(GOOGLE, "Google"),
        apple=_a(APPLE, "Apple"),
        revenuecat=_a(REVENUECAT, "RevenueCat"),
        meta=_a(META, "Meta"),
    )
    return [(page, title, desc, body.format(**alanlar))
            for page, title, desc, body in TEXT[code]]
