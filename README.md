# Yaman Evkaya — Scientific Portfolio

Bu klasör, doğrudan bir kişisel domaine yüklenebilen statik portföy sitesidir. Harici bir paket veya derleme adımı gerektirmez.

## Yerel önizleme

Bu klasörde basit bir statik sunucu çalıştırın ve tarayıcıdan verilen adresi açın:

```bash
python3 -m http.server 4173
```

## Yayınlama

Klasörün tamamı Netlify, Cloudflare Pages, GitHub Pages veya herhangi bir standart web sunucusunda yayınlanabilir. Yayın kökü bu klasör olmalıdır; giriş dosyası `index.html` dosyasıdır.

**Yayına girmemesi gerekenler:** `Projeler/` klasörü kaynak PDF arşividir ve `.gitignore` ile dışarıda tutulur; sürükle-bırak yükleme yapılıyorsa (ör. Netlify Drop) bu klasörü yüklemeden önce dışarı taşıyın. `Projeler/Makale/` altındaki PDF'in dosya adında satır sonu karakteri vardır; dosyayı yeniden adlandırın, aksi hâlde git ve bazı yükleme araçları hata verir.

Site **yevkaya.com** üzerinde GitHub Pages ile yayındadır (repo `yevkaya/yevkaya.github.io`, dal `main`, kök dizin). DNS: apex için GitHub'ın dört A kaydı, `www` için `yevkaya.github.io` CNAME'i; `CNAME` dosyası özel domaini GitHub'a bildirir. `og:url`, `canonical` ve `sitemap.xml` mutlak adresleri kullanır. `404.html` GitHub Pages'in bulunamayan her yol için gösterdiği sayfadır (mutlak yollar kullanır, bu yüzden `file://` ile değil `python3 -m http.server` ile önizleyin).

Yayın öncesi son adım: `python3 tools/stamp.py` footer'daki "Updated <ay yıl>" damgasını ve `sitemap.xml` içindeki `lastmod` tarihini bugüne çeker. Sosyal paylaşım kartı (`assets/images/social-card.png`, 1200×630) `python3 tools/social_card.py` ile sitenin kendi fontlarından üretilir (Playwright + Chromium gerekir).

Telif: `assets/documents/` altında yalnızca web CV'si yayınlanır. Yayıncı PDF'leri (Springer makalesi: yalnızca DOI linki), ortak yazarlı taslaklar ve tez tam metinleri yazılı izin olmadan siteye konmaz; `Projeler/` arşivi `.gitignore` ile dışarıdadır.

Gizlilik: sitede yalnızca `yaman@yevkaya.com` adresi bulunur; `index.html` içinde adres `data-mail`/`data-host` parçaları olarak durur ve `script.js` tarafından birleştirilir (JS kapalıyken "yaman [at] yevkaya.com" okunur). Ev adresi, telefon, doğum tarihi ve fotoğraf hiçbir dosyada yer almaz; `assets/documents/Yaman-Evkaya-CV.pdf` web sürümüdür.

## İçerik güncelleme

- Ana içerik: `index.html`
- Görsel tasarım: `styles.css`
- Etkileşimler: `script.js`
- Proje belgeleri: `assets/documents/`
- Görseller: `assets/images/`
- Diyalog figürleri (Fig. 3–10) ortak bir plaka sistemiyle çizilir: `tools/plates.py` her figürü Fig. 1 ile aynı anatomide üretir (çerçeveli FIG numarası, başlık, italik bağlam satırı, çizim, lejant, kaynak notu) ve aynı görsel dili kullanır (turkuaz akı/madde/yerleşik, altın plaket-halka/gelişmekte olan, fildişi kaynaklar; mono büyük harfli açıklama başlığı + italik alt satır, noktada biten ince gösterge çizgisi, plaka renginde haleli etiketler, tek nesneyi çevreleyen kesikli dış hat). Fig. 7 (M.Sc.) doğrudan `tools/fig1.py`'deki kesin durumdan (m = 4 temel durumu, Gauss yasası denetlenmiş) ve tezin gerçek-zaman verisinden (`tools/rt_data.json`) çizilir; Fig. 8'deki enerji seviyeleri çizilen potansiyelin kesin spektrumudur.
- `python3 tools/projects.py` proje diyaloglarını (Fig. 7–10) ve kartlardaki küçük figür çizimlerini, `python3 tools/schematics.py` profil diyaloglarını (Fig. 3–6) doğrudan `index.html` içindeki `<template>` bloklarına yazar; elle yapıştırma gerekmez.
- `python3 tools/stamp.py`: footer tarihi (EN/TR/DE sayfalarında yerelleştirilmiş ay adıyla) ve sitemap `lastmod`.
- **Diller.** İngilizce `index.html` tek kaynaktır; Türkçe (`tr/index.html`) ve Almanca (`de/index.html`) sayfalar `python3 tools/i18n.py build` ile ondan üretilir. Araç, İngilizce sayfadaki metin birimlerini (paragraf, başlık, liste, `<dt>/<dd>`, düğme, `aria-label`/`alt`, `<title>`, meta açıklamalar) satır içi işaretlemesiyle birlikte çıkarır ve `tools/i18n/strings.tr.json` / `strings.de.json` sözlüklerinde arar; eşleşmeyen birimler İngilizce kalır ve çıktıda listelenir. Sözlüklerin kaynağı `tools/i18n/tr.py` ve `de.py` dosyalarıdır (İngilizce birimlerin `strings.en.json` sırasına göre indekslenmiş çeviriler; `None` = İngilizce bırak). Figürlerin içindeki yazılar (inline SVG, Fig. 1 canvas) bilinçli olarak İngilizce bırakılır; `<script>`, `<style>` ve `<svg>` hiç dokunulmaz. Tez ve makale başlıkları özel ad olarak çevrilmez. İngilizce metin değişince sıra: `python3 tools/i18n.py extract` → yeni/değişen anahtarları `tr.py`/`de.py`'ye ekle (JSON sözlükler build sırasında otomatik yazılır) → `python3 tools/i18n.py build` → `python3 tools/stamp.py`. Her sayfa `hreflang` alternatiflerini, kendi `canonical`/`og:url`/`og:locale` değerlerini ve gezinmedeki EN · TR · DE anahtarını taşır; alt sayfalar varlıklara `../` ile göreli bağlanır.
- Hero'daki Fig. 1 (`figure.flux-c2`) `tools/fig1.py` ile üretilir ve `index.html` içine inline gömülüdür (ayrıntılar aşağıda). Eski C2 akı panelini üreten `tools/flux.py` artık kullanılmıyor.
- Kullanılmayan eski görseller (`flux-*.svg`, proje `.webp` dosyaları, portre) repodan kaldırılmıştır.

İşe özel motivasyon mektupları, ev adresi, telefon ve doğum tarihi kamusal siteye dahil edilmemiştir.

## Tipografi ve şematikler

- Fontlar `assets/fonts/` içinde, siteyle birlikte sunuluyor (Google Fonts CDN yok, GDPR açısından temiz): Cormorant Garamond (başlıklar), Newsreader (metin), IBM Plex Mono (etiketler), STIX Two Text/Math (formüller). Lisanslar aynı klasörde (OFL).
- Ana sayfadaki Fig. 1, Halimeh et al., PRX Quantum 5, 030358 (2024) Şekil 1–2'deki singlet-örtü gösterimini kullanır: her köşe bir site üçgenidir (merkezde madde sitesi, köşelerde her bağın kendi ucundaki rishon sitesi); aynı köşedeki iki tek-dolu siteyi birleştiren lob bir SU(2) renk singletidir, çift-dolu site yerinde singlet olarak (halka) çizilir. İki cluster türü vardır: **matter cluster** (bir aktif |1,1⟩ bağ, iki ucunda birer madde–rishon singleti, yani q q̄) ve **glueball cluster** (Tr U_p rezonansı: plaket terimi çıplak |0,2⟩ vakumunu yok eder ve yalnızca altıgenin alternatif bağlarındaki üç singlet çiftine, yani iki Kekulé örtüsüne etki edip bunları birbirine çevirir; vakum sektöründeki 16 502 gauge-invariant konfigürasyonun tam taramasıyla doğrulandı). Flux tüpü Q'dan Q̄'ya uzanan açık bir rishon–rishon singlet zinciridir. Döngü: vakumda A halkası rezonansta + ℓ4, ℓ12 matter cluster'ları → Q ve Q̄ elle yerleştirilir (registered koridor sektörü, A halkası tek örtüye kilitlenir) → formation ramp: ℓ6, ℓ4 yok olur, ℓ12, ℓ10, ℓ3 q q̄ annihilasyonuyla tek zincire bağlanır → breaking quench: tam ortadaki ℓ10 bağında vakumdan bir q q̄ çifti doğar ve tüpü ikiye keser, her yarı ℓ3 ve ℓ12'de bir çiftle yeniden kesilir; sonuç dört kısa renk-singlet sicimdir (Q q̄, q q̄, q q̄, q Q̄), ℓ6 ve ℓ4 cluster'ları vakumdan yeniden doğar → kaynaklar kaldırılır: vakum etiketlerine dönen tek yerel hamle her koridor bağında bir rishon kaydırmasıdır (hafif yükler ℓ3, ℓ10, ℓ12 üzerinde yeniden eşleşir) → B halkası rezonansa girer ve rezonans ortak örtü üzerinden A halkasına geri geçer. Çift doğumu ve annihilasyon, bağın ortasından çıkan ya da orada buluşan iki küçük q / q̄ diskiyle çizilir. Her ayrık kare otomatik denetlenir (n_L + n_R = 2, D_v etiketleri, her tek-dolu sitede tam bir singlet; 18 kare). Eksenin altındaki bantlar tezin kesin gerçek-zaman verisidir (κ = 0, R = 4; `tools/rt_data.json`, Response Report Fig. 2'den çıkarıldı, Tablo 4 ile doğrulandı). v7: her renk-singlet nesnesi (matter cluster, perdelenmiş kaynak, açık sicim) kesikli bir dış hatla işaretlenir; hat, nesnenin iskeleti boyunca Gauss konvolüsyon alanının eş-değer eğrisidir. Formation sırasında cluster hatları join'lerde birleşip tek tüp hattına dönüşür ("FLUX TUBE FORMED"), quench'te hat önce ℓ10'da, sonra ℓ3 ve ℓ12'de boğumlanıp dört kısa sicimin elipslerine ayrılır ("STRING BREAKING"); başta ve sonda "GLUEBALL FORMATION" (halka içinde kesikli altın daire) ve "MATTER FORMATION" etiketleri görünür. Hat sayısı her denetim karesinde fiziksel singlet sayısıyla otomatik karşılaştırılır. Şekil dört SVG katmanından oluşur (parıltı, tüp parıltısı, etkileşimli şekil, açıklamalar); her biri ayrı compositor katmanıdır. Ramp ve quench panelleri arasındaki dar boşluk (GS) m = 4 temel durumunun tutulduğu aralıktır. `tools/fig1.py` SVG'yi `index.html` içine, çalışma zamanını `assets/js/fig1.js` olarak yazar (keyframe izleri, sinüs yumuşatma, SVG filtresi yok); `fig1.js` değiştiğinde `FIG1_V=<n> python3 tools/fig1.py` ile önbellek sürümünü artırın.
- Hero arka planındaki kafes her yeniden boyutlandırmada bir kez statik görüntüye çizilir; hareketli parçacıklar Web Animations ile compositor üzerinde yürür; hero'daki gren katmanı `mix-blend-mode` yerine düz alfa kullanır (görsel fark < 0.02/255), böylece arka plandaki hareket her karede tüm hero'yu yeniden harmanlatmaz (tam döngüde 60 fps).
- Fig. 2 (`assets/images/ads-wilson-worldsheet.svg`, `tools/inline_ads.py` ile `index.html` içine gömülür) 10 saniyelik sakin bir döngüyle canlanır (`script.js` sonundaki blok): Wilson döngüsü çizilir, worldsheet kesme derinliği z = ε'a kadar bulk'a sarkar (ön ve arka ağ ayrı clip'lerle, kesit elipsi çizimin izdüşümünden hesaplanır), radyal eksendeki işaret UV → IR iner, sonunda ⟨W⟩ ≃ e^√λ sonucu belirir. Üzerine gelince durur, görünür değilken çalışmaz, `prefers-reduced-motion` açıksa son kare statik gösterilir.
- `tools/design.py`, `styles.css` içindeki yönetilen blokları (FONTS ve DESIGN SYSTEM v4) yeniden yazar.
- `tools/inline_ads.py`, AdS/CFT şemasını (Fig. 2) `assets/images/ads-wilson-worldsheet.svg` kaynağından `index.html` içine gömer; etiketler Fig. 1'in açıklama dilindedir, lejant ve kaynak notu (Drukker, Gross & Ooguri, PRD 60, 125006 (1999)) şeklin altındadır.
- Artık kullanılmayan dosyalar silinebilir: `assets/images/flux-*.svg`, eski `.webp` görseller ve `ads-wilson-worldsheet.svg` (artık sayfaya gömülü).
