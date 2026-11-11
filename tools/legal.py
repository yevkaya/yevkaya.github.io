# -*- coding: utf-8 -*-
"""Build the legal pages (Impressum / legal notice and privacy policy) in German, English and Turkish.

  python3 tools/legal.py   → writes legal-notice.html, privacy.html, de/impressum.html, de/datenschutz.html,
                             tr/kunye.html, tr/gizlilik.html

German is the binding version; the English and Turkish pages are translations and say so.
Edit the texts below, not the generated HTML. Every norm cited in the texts is listed with its official
source under "Rechtsquellen" / "Legal sources" / "Hukuki kaynaklar" at the end of each page.

Switches:
  ADDRESS          serviceable address (ladungsfähige Anschrift), e.g. a c/o address of a mail-forwarding service;
                   empty → only the city is shown
  CHECKDOMAIN_AVV  set to True once the data processing agreement (Art. 28 Abs. 3 DSGVO) with checkdomain has been
                   concluded (customer area → "Meine Daten" → "Auftragsverarbeitung"); adds the sentence to the policy
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = next(os.path.abspath(p) for p in (os.path.join(HERE, ".."), os.path.join(HERE, "..", "Portfolio"))
            if os.path.exists(os.path.join(p, "index.html")))
BASE = "https://yevkaya.com"
STAND = {"de": "11. November 2026", "en": "11 November 2026", "tr": "11 Kasım 2026"}

ADDRESS = []                 # e.g. ["c/o Beispiel-Zustelldienst GmbH", "Musterstraße 1", "80331 München"]
CHECKDOMAIN_AVV = False

# shown under the provider in the Impressum while ADDRESS is empty
ADDRESS_PENDING = {
    "de": "Eine ladungsfähige Zustellanschrift (c/o-Anschrift) wird derzeit eingerichtet und an dieser Stelle umgehend ergänzt. Bis dahin ist der Anbieter unter der nachstehenden E-Mail-Adresse erreichbar.",
    "en": "A postal address suitable for the service of documents (c/o address) is currently being set up and will be added here without delay. Until then, the provider can be reached at the email address below.",
    "tr": "Tebligata elverişli bir posta adresi (c/o adresi) şu anda temin edilmekte olup en kısa sürede buraya eklenecektir. O zamana kadar site sahibine aşağıdaki e-posta adresinden ulaşılabilir.",
}

MAIL = '<a href="mailto:yaman&#64;yevkaya.com">yaman&#64;yevkaya.com</a>'

PATHS = {
    "imprint": {"en": "legal-notice.html", "de": "de/impressum.html", "tr": "tr/kunye.html"},
    "privacy": {"en": "privacy.html", "de": "de/datenschutz.html", "tr": "tr/gizlilik.html"},
}
HOME = {"en": "", "de": "de/", "tr": "tr/"}
LOCALE = {"en": "en_US", "de": "de_DE", "tr": "tr_TR"}

GII = "https://www.gesetze-im-internet.de"
URL = {
    "mstv18": "https://www.gesetze-bayern.de/Content/Document/MStV-18",
    "ddg5": GII + "/ddg/__5.html",
    "bgb14": GII + "/bgb/__14.html",
    "vsbg36": GII + "/vsbg/__36.html",
    "urhg": GII + "/urhg/BJNR012730965.html",
    "bdsg": GII + "/bdsg_2018/BJNR209710017.html",
    "tdddg25": GII + "/ttdsg/__25.html",
    "baydsg18": "https://www.gesetze-bayern.de/Content/Document/BayDSG-18",
    "gh_priv": "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement",
    "gh_pages": "https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection",
    "gh_sub": "https://docs.github.com/en/site-policy/privacy-policies/github-subprocessors",
    "dpf_list": "https://www.dataprivacyframework.gov/list",
    "lda": "https://www.lda.bayern.de",
    "fastly_dpf": "https://www.fastly.com/data-privacy-framework",
}

UI = {
    "en": {"imprint": "Legal notice (Impressum)", "privacy": "Privacy policy", "back": "Back to the site",
           "kicker": "Legal", "stand": "Last updated", "lang": "Language", "skip": "Skip to content",
           "toc": "Contents", "privlink": "privacy policy",
           "note": "This is a translation provided for convenience. Only the <a href=\"[[DE]]\">German version</a> is legally binding."},
    "de": {"imprint": "Impressum", "privacy": "Datenschutzerklärung", "back": "Zurück zur Website",
           "kicker": "Rechtliches", "stand": "Stand", "lang": "Sprache", "skip": "Zum Inhalt springen",
           "toc": "Inhalt", "privlink": "Datenschutzerklärung", "note": ""},
    "tr": {"imprint": "Künye (Impressum)", "privacy": "Gizlilik politikası", "back": "Siteye dön",
           "kicker": "Yasal bilgiler", "stand": "Son güncelleme", "lang": "Dil", "skip": "İçeriğe geç",
           "toc": "İçindekiler", "privlink": "Gizlilik politikası",
           "note": "Bu metin bilgilendirme amaçlı bir çeviridir; hukuken bağlayıcı olan yalnızca <a href=\"[[DE]]\">Almanca metindir</a>. "
                   "Alman mevzuatına yapılan atıflar orijinal biçimleriyle verilmiştir (Abs. = fıkra, Nr. = bent, Satz = cümle); "
                   "AB mevzuatına yapılan atıflar “Art. 6(1)(f)” biçimindedir (madde, fıkra, bent)."},
}

AVV = {
    "de": " Mit der checkdomain GmbH besteht ein Vertrag zur Auftragsverarbeitung nach Art. 28 Abs. 3 DSGVO.",
    "en": " A data processing agreement pursuant to Art. 28(3) GDPR has been concluded with checkdomain GmbH.",
    "tr": " checkdomain GmbH ile GDPR Art. 28(3) uyarınca bir veri işleme sözleşmesi yapılmıştır.",
}


def eurlex(celex, lang):
    return "https://eur-lex.europa.eu/legal-content/%s/TXT/?uri=CELEX:%s" % ("DE" if lang == "de" else "EN", celex)


def addr(lang):
    city = {"de": "München, Deutschland", "en": "Munich, Germany", "tr": "Münih, Almanya"}[lang]
    return "<br />".join(["Yaman Evkaya"] + (ADDRESS if ADDRESS else [city]))


# ============================================================================================ IMPRESSUM
IMPRINT = {}

IMPRINT["de"] = """
<p class="lead">Angaben gemäß § 18 Abs. 1 Medienstaatsvertrag (MStV) sowie – soweit anwendbar – gemäß § 5 Abs. 1 Digitale-Dienste-Gesetz (DDG)</p>

<h2>Diensteanbieter</h2>
<p>[[ADDR]]</p>[[ADDRNOTE]]

<h2>Kontakt</h2>
<p>E-Mail: [[MAIL]]</p>
<p class="fine">Angabe zur schnellen elektronischen Kontaktaufnahme und unmittelbaren Kommunikation (§ 5 Abs. 1 Nr. 2 DDG).</p>

<h2>Inhaltlich verantwortlich</h2>
<p>Yaman Evkaya (freiwillige Angabe; Kontakt wie vorstehend)</p>

<h2>Art des Angebots und rechtliche Einordnung</h2>
<p>yevkaya.com ist die persönliche, nicht kommerzielle Website eines Physikers zur Darstellung von Ausbildung, Forschungsinteressen und Projekten. Über die Website werden weder Waren noch Dienstleistungen gegen Entgelt angeboten; sie enthält keine Werbung und keine Affiliate-Links.</p>
<p>Angaben nach § 5 Abs. 1 Nr. 3 bis 8 DDG (zuständige Aufsichtsbehörde, Register und Registernummer, berufsrechtliche Angaben, Umsatzsteuer- oder Wirtschafts-Identifikationsnummer, Abwicklung oder Liquidation, audiovisuelle Mediendienste) entfallen, da die jeweiligen Voraussetzungen nicht vorliegen.</p>

<h2>Verbraucherstreitbeilegung</h2>
<p>Über diese Website werden keine Verträge mit Verbrauchern geschlossen; der Anbieter handelt insoweit nicht als Unternehmer im Sinne von § 14 Abs. 1 Bürgerliches Gesetzbuch (BGB). Informationspflichten nach §§ 36, 37 Verbraucherstreitbeilegungsgesetz (VSBG) bestehen daher nicht.</p>
<p>Ein Hinweis auf die Europäische Plattform zur Online-Streitbeilegung entfällt: Die Plattform wurde eingestellt, und die Verordnung (EU) Nr. 524/2013 ist durch Art. 1 der Verordnung (EU) 2024/3228 mit Wirkung vom 20. Juli 2025 aufgehoben.</p>

<h2>Urheberrecht</h2>
<p>Die Texte dieser Website (Sprachwerke, § 2 Abs. 1 Nr. 1 Urheberrechtsgesetz – UrhG) sowie ihre Abbildungen, insbesondere Abb.&#8201;1 und Abb.&#8201;2 (Darstellungen wissenschaftlicher oder technischer Art, § 2 Abs. 1 Nr. 7 UrhG), wurden von Yaman Evkaya geschaffen und sind urheberrechtlich geschützt, soweit sie persönliche geistige Schöpfungen im Sinne von § 2 Abs. 2 UrhG darstellen. Jede Verwertung außerhalb der gesetzlich erlaubten Nutzungen (§§ 44a bis 63a UrhG), insbesondere die Vervielfältigung, Verbreitung oder öffentliche Zugänglichmachung (§§ 16, 17, 19a UrhG), bedarf der vorherigen Zustimmung. Zitate sind im Rahmen des § 51 UrhG unter Angabe der Quelle (§ 63 UrhG) zulässig.</p>
<p>Veröffentlichte Fachartikel werden ausschließlich über ihren Digital Object Identifier (DOI) verlinkt; Verlagsfassungen werden auf dieser Website nicht bereitgestellt. Die Rechte an diesen Veröffentlichungen liegen bei den jeweiligen Rechteinhabern.</p>
<p>Die verwendeten Schriftarten Cormorant Garamond, Newsreader, IBM Plex Mono und STIX Two werden über diese Website selbst ausgeliefert (kein externer Schriftendienst) und auf Grundlage der SIL Open Font License, Version 1.1, genutzt; die Lizenztexte sind im Verzeichnis <code>/assets/fonts/</code> hinterlegt.</p>

<h2>Verweise auf fremde Websites</h2>
<p>Diese Website enthält Verweise (Hyperlinks) auf Angebote Dritter, etwa LinkedIn, GitHub und doi.org. Deren Inhalte mache ich mir nicht zu eigen; für sie ist ausschließlich der jeweilige Anbieter verantwortlich. Zum Zeitpunkt der Verlinkung waren Rechtsverstöße auf den verlinkten Seiten nicht erkennbar. Eine fortlaufende Kontrolle der verlinkten Inhalte ist ohne konkrete Anhaltspunkte für eine Rechtsverletzung nicht geschuldet (vgl. BGH, Urteil vom 18. Juni 2015 – I ZR 74/14, Haftung für Hyperlink; EuGH, Urteil vom 8. September 2016 – C‑160/15, GS Media). Wird mir eine Rechtsverletzung bekannt, entferne ich den betreffenden Link unverzüglich.</p>

<h2>Hinweise auf Rechtsverletzungen</h2>
<p>Sollten Inhalte dieser Website nach Ihrer Auffassung Rechte Dritter oder gesetzliche Vorschriften verletzen, bitte ich um eine Nachricht an die oben genannte E-Mail-Adresse. Begründete Hinweise werden unverzüglich geprüft; rechtsverletzende Inhalte werden umgehend entfernt.</p>

<h2>Datenschutz</h2>
<p>Informationen zur Verarbeitung personenbezogener Daten nach Art. 13 DSGVO enthält die [[PRIV]].</p>

<h2>Sprachfassungen</h2>
<p>Diese Angaben stehen zusätzlich in englischer und türkischer Sprache zur Verfügung. Rechtlich maßgeblich ist ausschließlich die deutsche Fassung.</p>
"""

IMPRINT["en"] = """
<p class="lead">Information pursuant to § 18(1) of the Interstate Media Treaty (Medienstaatsvertrag, MStV) and, where applicable, § 5(1) of the German Digital Services Act (Digitale-Dienste-Gesetz, DDG)</p>

<h2>Service provider</h2>
<p>[[ADDR]]</p>[[ADDRNOTE]]

<h2>Contact</h2>
<p>Email: [[MAIL]]</p>
<p class="fine">Details enabling rapid electronic contact and direct communication (§ 5(1) no. 2 DDG).</p>

<h2>Responsible for the content</h2>
<p>Yaman Evkaya (voluntary information; contact as above)</p>

<h2>Nature of the website and legal classification</h2>
<p>yevkaya.com is the personal, non-commercial website of a physicist presenting his education, research interests and projects. No goods or services are offered for payment through the website; it contains no advertising and no affiliate links.</p>
<p>The information required by § 5(1) nos. 3 to 8 DDG (competent supervisory authority, register and registration number, professional-law details, VAT or business identification number, winding-up or liquidation, audiovisual media services) does not apply, as the respective conditions are not met.</p>

<h2>Consumer dispute resolution</h2>
<p>No contracts with consumers are concluded via this website, and the provider does not act as a trader (Unternehmer) within the meaning of § 14(1) of the German Civil Code (BGB) in this respect. Consequently, there are no information obligations under §§ 36 and 37 of the Consumer Dispute Resolution Act (VSBG).</p>
<p>No reference to the European Online Dispute Resolution platform is required: the platform has been discontinued, and Regulation (EU) No 524/2013 was repealed with effect from 20 July 2025 by Article 1 of Regulation (EU) 2024/3228.</p>

<h2>Copyright</h2>
<p>The texts on this website (literary works, § 2(1) no. 1 of the German Copyright Act, UrhG) and its figures, in particular Fig.&#8201;1 and Fig.&#8201;2 (representations of a scientific or technical nature, § 2(1) no. 7 UrhG), were created by Yaman Evkaya and are protected by copyright insofar as they constitute personal intellectual creations within the meaning of § 2(2) UrhG. Any use beyond the uses permitted by law (§§ 44a to 63a UrhG), in particular reproduction, distribution or making available to the public (§§ 16, 17, 19a UrhG), requires prior consent. Quotation is permitted within the limits of § 51 UrhG, with the source acknowledged (§ 63 UrhG).</p>
<p>Published journal articles are linked exclusively via their Digital Object Identifier (DOI); publisher versions are not provided on this website. The rights to these publications remain with the respective rights holders.</p>
<p>The typefaces Cormorant Garamond, Newsreader, IBM Plex Mono and STIX Two are delivered by this website itself (no external font service) and used under the SIL Open Font License, Version 1.1; the licence texts are stored in <code>/assets/fonts/</code>.</p>

<h2>Links to third-party websites</h2>
<p>This website contains hyperlinks to third-party services such as LinkedIn, GitHub and doi.org. I do not adopt their content as my own; the respective provider alone is responsible for it. No legal violations on the linked pages were apparent at the time the links were set. Without concrete indications of an infringement, continuous monitoring of linked content is not required (cf. Federal Court of Justice (BGH), judgment of 18 June 2015 – I ZR 74/14, Haftung für Hyperlink; Court of Justice of the EU, judgment of 8 September 2016 – C‑160/15, GS Media). Should an infringement become known to me, I will remove the link concerned without delay.</p>

<h2>Notification of infringements</h2>
<p>If you believe that content on this website infringes the rights of third parties or statutory provisions, please notify me at the email address above. Substantiated notices will be examined without delay; infringing content will be removed promptly.</p>

<h2>Data protection</h2>
<p>Information on the processing of personal data under Art. 13 GDPR is provided in the [[PRIV]].</p>

<h2>Language versions</h2>
<p>This notice is also available in German and Turkish. Only the German version is legally binding.</p>
"""

IMPRINT["tr"] = """
<p class="lead">§ 18 Abs. 1 Eyaletlerarası Medya Antlaşması (Medienstaatsvertrag, MStV) ve – uygulanabildiği ölçüde – § 5 Abs. 1 Dijital Hizmetler Kanunu (Digitale-Dienste-Gesetz, DDG) uyarınca bilgiler</p>

<h2>Hizmet sağlayıcı</h2>
<p>[[ADDR]]</p>[[ADDRNOTE]]

<h2>İletişim</h2>
<p>E-posta: [[MAIL]]</p>
<p class="fine">Hızlı elektronik temas ve doğrudan iletişim kurulmasını sağlayan bilgi (§ 5 Abs. 1 Nr. 2 DDG).</p>

<h2>İçerikten sorumlu kişi</h2>
<p>Yaman Evkaya (gönüllü olarak verilen bilgi; iletişim bilgileri yukarıdadır)</p>

<h2>Sitenin niteliği ve hukuki değerlendirme</h2>
<p>yevkaya.com, bir fizikçinin eğitimini, araştırma ilgi alanlarını ve projelerini tanıtan kişisel ve ticari olmayan bir web sitesidir. Site üzerinden ücret karşılığı mal veya hizmet sunulmaz; sitede reklam ve satış ortaklığı (affiliate) bağlantısı bulunmaz.</p>
<p>§ 5 Abs. 1 Nr. 3–8 DDG kapsamındaki bilgiler (yetkili denetim makamı, sicil ve sicil numarası, meslek hukukuna ilişkin bilgiler, KDV veya ekonomik kimlik numarası, tasfiye, görsel-işitsel medya hizmetleri) ilgili koşullar mevcut olmadığından yer almamaktadır.</p>

<h2>Tüketici uyuşmazlıklarının çözümü</h2>
<p>Bu site üzerinden tüketicilerle sözleşme kurulmaz; site sahibi bu bakımdan § 14 Abs. 1 Alman Medeni Kanunu (BGB) anlamında girişimci (Unternehmer) sıfatıyla hareket etmez. Bu nedenle §§ 36, 37 Tüketici Uyuşmazlıklarının Çözümü Kanunu (VSBG) kapsamında bilgilendirme yükümlülüğü bulunmamaktadır.</p>
<p>Avrupa Çevrimiçi Uyuşmazlık Çözümü Platformu’na atıf yapılması gerekmez: Platform kapatılmış ve (AB) 524/2013 sayılı Tüzük, (AB) 2024/3228 sayılı Tüzük’ün 1. maddesiyle 20 Temmuz 2025 tarihinden itibaren yürürlükten kaldırılmıştır.</p>

<h2>Telif hakkı</h2>
<p>Bu sitedeki metinler (dil eserleri, § 2 Abs. 1 Nr. 1 Telif Hakkı Kanunu – UrhG) ve şekiller, özellikle Şek.&#8201;1 ve Şek.&#8201;2 (bilimsel veya teknik nitelikteki tasvirler, § 2 Abs. 1 Nr. 7 UrhG), Yaman Evkaya tarafından oluşturulmuştur ve § 2 Abs. 2 UrhG anlamında kişisel fikrî yaratım niteliği taşıdıkları ölçüde telif hakkıyla korunur. Kanunen izin verilen kullanımlar (§§ 44a–63a UrhG) dışındaki her türlü kullanım, özellikle çoğaltma, yayma veya kamuya erişilebilir kılma (§§ 16, 17, 19a UrhG), önceden izin alınmasını gerektirir. Alıntı, § 51 UrhG sınırları içinde ve kaynak gösterilerek (§ 63 UrhG) serbesttir.</p>
<p>Yayımlanmış makalelere yalnızca Dijital Nesne Tanımlayıcısı (DOI) üzerinden bağlantı verilir; yayınevi sürümleri bu sitede sunulmaz. Bu yayınlar üzerindeki haklar ilgili hak sahiplerine aittir.</p>
<p>Cormorant Garamond, Newsreader, IBM Plex Mono ve STIX Two yazı tipleri doğrudan bu site üzerinden sunulur (harici yazı tipi hizmeti kullanılmaz) ve SIL Open Font License, Sürüm 1.1 kapsamında kullanılır; lisans metinleri <code>/assets/fonts/</code> klasöründedir.</p>

<h2>Üçüncü taraf sitelere bağlantılar</h2>
<p>Bu site LinkedIn, GitHub ve doi.org gibi üçüncü taraf hizmetlere bağlantılar (hyperlink) içerir. Bu sitelerin içeriğini benimsemem; içerikten yalnızca ilgili sağlayıcı sorumludur. Bağlantı verildiği tarihte bağlantı verilen sayfalarda hukuka aykırılık fark edilebilir durumda değildi. Somut bir ihlal belirtisi olmadıkça bağlantı verilen içeriklerin sürekli denetlenmesi gerekmez (bkz. Alman Federal Yüksek Mahkemesi (BGH), 18 Haziran 2015 tarihli karar – I ZR 74/14, Haftung für Hyperlink; Avrupa Birliği Adalet Divanı (ABAD), 8 Eylül 2016 tarihli karar – C‑160/15, GS Media). Bir hukuka aykırılık öğrenildiğinde ilgili bağlantı derhal kaldırılır.</p>

<h2>Hak ihlali bildirimleri</h2>
<p>Bu sitedeki içeriklerin üçüncü kişilerin haklarını veya yasal düzenlemeleri ihlal ettiğini düşünüyorsanız lütfen yukarıdaki e-posta adresine bildirin. Gerekçeli bildirimler gecikmeksizin incelenir; hukuka aykırı içerikler derhal kaldırılır.</p>

<h2>Veri koruma</h2>
<p>Kişisel verilerin işlenmesine ilişkin GDPR Art. 13 kapsamındaki bilgiler [[PRIV]] sayfasında yer almaktadır.</p>

<h2>Dil sürümleri</h2>
<p>Bu bilgiler Almanca ve İngilizce olarak da mevcuttur. Hukuken bağlayıcı olan yalnızca Almanca metindir.</p>
"""

IMPRINT_SOURCES = {
    "de": [
        ("[[U:mstv18]]", "Medienstaatsvertrag (MStV) vom 23. April 2020 (GVBl. S. 450, 451, 2021 S. 14, BayRS 02-33-S)", "§ 18"),
        ("[[U:ddg5]]", "Digitale-Dienste-Gesetz (DDG) vom 6. Mai 2024 (BGBl. 2024 I Nr. 149)", "§ 5"),
        ("[[U:bgb14]]", "Bürgerliches Gesetzbuch (BGB) in der Fassung der Bekanntmachung vom 2. Januar 2002 (BGBl. I S. 42, 2909; 2003 I S. 738)", "§ 14"),
        ("[[U:vsbg36]]", "Verbraucherstreitbeilegungsgesetz (VSBG) vom 19. Februar 2016 (BGBl. I S. 254, 1039)", "§§ 36, 37"),
        ("[[U:urhg]]", "Urheberrechtsgesetz (UrhG) vom 9. September 1965 (BGBl. I S. 1273)", "§§ 2, 16, 17, 19a, 44a–63a, 51, 63"),
        ("[[EU:32024R3228]]", "Verordnung (EU) 2024/3228 des Europäischen Parlaments und des Rates vom 19. Dezember 2024 zur Aufhebung der Verordnung (EU) Nr. 524/2013 und zur Änderung der Verordnungen (EU) 2017/2394 und (EU) 2018/1724 im Hinblick auf die Einstellung der Europäischen Plattform für Online-Streitbeilegung, ABl. L, 2024/3228, 30.12.2024", "Art. 1"),
        (None, "BGH, Urteil vom 18. Juni 2015 – I ZR 74/14 (Haftung für Hyperlink)", ""),
        (None, "EuGH, Urteil vom 8. September 2016 – C‑160/15 (GS Media), ECLI:EU:C:2016:644", ""),
    ],
    "en": [
        ("[[U:mstv18]]", "Medienstaatsvertrag (MStV) [Interstate Media Treaty] of 23 April 2020 (GVBl. S. 450, 451, 2021 S. 14, BayRS 02-33-S)", "§ 18"),
        ("[[U:ddg5]]", "Digitale-Dienste-Gesetz (DDG) [German Digital Services Act] of 6 May 2024 (BGBl. 2024 I Nr. 149)", "§ 5"),
        ("[[U:bgb14]]", "Bürgerliches Gesetzbuch (BGB) [Civil Code], as promulgated on 2 January 2002 (BGBl. I S. 42, 2909; 2003 I S. 738)", "§ 14"),
        ("[[U:vsbg36]]", "Verbraucherstreitbeilegungsgesetz (VSBG) [Consumer Dispute Resolution Act] of 19 February 2016 (BGBl. I S. 254, 1039)", "§§ 36, 37"),
        ("[[U:urhg]]", "Urheberrechtsgesetz (UrhG) [Copyright Act] of 9 September 1965 (BGBl. I S. 1273)", "§§ 2, 16, 17, 19a, 44a–63a, 51, 63"),
        ("[[EU:32024R3228]]", "Regulation (EU) 2024/3228 of the European Parliament and of the Council of 19 December 2024 repealing Regulation (EU) No 524/2013, and amending Regulations (EU) 2017/2394 and (EU) 2018/1724 with regard to the discontinuation of the European Online Dispute Resolution Platform, OJ L, 2024/3228, 30.12.2024", "Art. 1"),
        (None, "Federal Court of Justice (BGH), judgment of 18 June 2015 – I ZR 74/14 (Haftung für Hyperlink)", ""),
        (None, "Court of Justice of the EU, judgment of 8 September 2016 – C‑160/15 (GS Media), ECLI:EU:C:2016:644", ""),
    ],
    "tr": [
        ("[[U:mstv18]]", "Medienstaatsvertrag (MStV) [Eyaletlerarası Medya Antlaşması], 23 Nisan 2020 (GVBl. S. 450, 451, 2021 S. 14, BayRS 02-33-S)", "§ 18"),
        ("[[U:ddg5]]", "Digitale-Dienste-Gesetz (DDG) [Dijital Hizmetler Kanunu], 6 Mayıs 2024 (BGBl. 2024 I Nr. 149)", "§ 5"),
        ("[[U:bgb14]]", "Bürgerliches Gesetzbuch (BGB) [Alman Medeni Kanunu], 2 Ocak 2002 tarihli ilan metni (BGBl. I S. 42, 2909; 2003 I S. 738)", "§ 14"),
        ("[[U:vsbg36]]", "Verbraucherstreitbeilegungsgesetz (VSBG) [Tüketici Uyuşmazlıklarının Çözümü Kanunu], 19 Şubat 2016 (BGBl. I S. 254, 1039)", "§§ 36, 37"),
        ("[[U:urhg]]", "Urheberrechtsgesetz (UrhG) [Telif Hakkı Kanunu], 9 Eylül 1965 (BGBl. I S. 1273)", "§§ 2, 16, 17, 19a, 44a–63a, 51, 63"),
        ("[[EU:32024R3228]]", "Regulation (EU) 2024/3228 of the European Parliament and of the Council of 19 December 2024 repealing Regulation (EU) No 524/2013, and amending Regulations (EU) 2017/2394 and (EU) 2018/1724 with regard to the discontinuation of the European Online Dispute Resolution Platform, OJ L, 2024/3228, 30.12.2024", "Art. 1"),
        (None, "BGH, 18 Haziran 2015 tarihli karar – I ZR 74/14 (Haftung für Hyperlink)", ""),
        (None, "ABAD, 8 Eylül 2016 tarihli karar – C‑160/15 (GS Media), ECLI:EU:C:2016:644", ""),
    ],
}

# ============================================================================================ DATENSCHUTZ
PRIVACY = {}

PRIVACY["de"] = """
<p class="lead">Informationen nach Art. 13 der Datenschutz-Grundverordnung (Verordnung (EU) 2016/679, DSGVO) über die Verarbeitung personenbezogener Daten beim Besuch dieser Website und bei einer Kontaktaufnahme. Die verwendeten Begriffe – etwa „personenbezogene Daten“, „Verarbeitung“, „Verantwortlicher“, „Auftragsverarbeiter“ und „Empfänger“ – sind im Sinne von Art. 4 DSGVO zu verstehen.</p>

[[TOC]]

<h2 id="s1">1. Verantwortlicher</h2>
<p>Verantwortlicher im Sinne von Art. 4 Nr. 7 DSGVO ist:</p>
<p>[[ADDR]]<br />E-Mail: [[MAIL]]</p>
<p>Der Verantwortliche ist eine natürliche Person und damit nichtöffentliche Stelle im Sinne von § 2 Abs. 4 Satz 1 Bundesdatenschutzgesetz (BDSG). Ein Datenschutzbeauftragter ist nicht benannt; die Voraussetzungen einer Benennungspflicht nach Art. 37 Abs. 1 DSGVO und § 38 Abs. 1 BDSG liegen nicht vor.</p>

<h2 id="s2">2. Übersicht der Verarbeitungen</h2>
<div class="lg-table-wrap"><table class="lg-table">
<thead><tr><th>Verarbeitung und Daten</th><th>Zweck</th><th>Rechtsgrundlage</th><th>Speicherdauer</th><th>Empfänger, Drittland</th></tr></thead>
<tbody>
<tr><td><strong>Bereitstellung der Website</strong> (Ziff. 3): IP-Adresse, Zeitpunkt, angeforderte Datei, Browserangaben, Referrer</td><td>Auslieferung, Stabilität und Sicherheit der Website</td><td>Art. 6 Abs. 1 UAbs. 1 lit. f DSGVO</td><td>nach den Kriterien von GitHub (Ziff. 3)</td><td>GitHub, Inc.; Fastly, Inc. (CDN); Verarbeitung auch in den USA – Art. 45 Abs. 1 DSGVO i.&#8239;V.&#8239;m. Durchführungsbeschluss (EU) 2023/1795</td></tr>
<tr><td><strong>Kontakt per E-Mail</strong> (Ziff. 6): E-Mail-Adresse, Name, Inhalt, Metadaten</td><td>Bearbeitung und Beantwortung der Anfrage</td><td>Art. 6 Abs. 1 UAbs. 1 lit. b bzw. lit. f DSGVO</td><td>bis zur Zweckerreichung; ohne fortbestehende Zusammenarbeit spätestens zwei Jahre nach der letzten Nachricht (Ziff. 6)</td><td>checkdomain GmbH (Auftragsverarbeiter), Deutschland; keine Drittlandübermittlung</td></tr>
</tbody></table></div>
<p>Cookies sowie Analyse-, Tracking- und Werbedienste werden nicht eingesetzt (Ziff. 4).</p>

<h2 id="s3">3. Bereitstellung der Website (Hosting über GitHub Pages)</h2>
<p><strong>Anbieter.</strong> Die Website wird über GitHub Pages der GitHub, Inc., 88 Colin P. Kelly Jr. St., San Francisco, CA 94107, USA, bereitgestellt. GitHub liefert die Seiten über das Content-Delivery-Netzwerk der Fastly, Inc., USA, aus (GitHub führt Fastly in seiner <a href="[[U:gh_sub]]" rel="noopener">Liste der Unterauftragsverarbeiter</a> als „Content delivery service“).</p>
<p><strong>Verarbeitete Daten.</strong> Bei jedem Aufruf verarbeitet GitHub die für die Auslieferung erforderlichen Verbindungsdaten, insbesondere die IP-Adresse Ihres Endgeräts, Datum und Uhrzeit der Anfrage, die angeforderte Datei sowie die von Ihrem Browser übermittelten Angaben (z.&#8239;B. Browsertyp und -version, Betriebssystem, Referrer-URL). Nach eigenen Angaben protokolliert und speichert GitHub die IP-Adressen der Besucher von GitHub-Pages-Websites zu Sicherheitszwecken (<a href="[[U:gh_pages]]" rel="noopener">GitHub Docs, „Data collection“</a>). IP-Adressen werden als personenbezogene Daten behandelt (Art. 4 Nr. 1 DSGVO; vgl. EuGH, Urteil vom 19. Oktober 2016 – C‑582/14, Breyer).</p>
<p><strong>Zweck und Rechtsgrundlage (Art. 13 Abs. 1 lit. c und d DSGVO).</strong> Die Verarbeitung dient der Auslieferung der Website, der Gewährleistung ihrer Stabilität und Sicherheit sowie der Erkennung und Abwehr von Angriffen und Missbrauch. Rechtsgrundlage ist Art. 6 Abs. 1 UAbs. 1 lit. f DSGVO. Das berechtigte Interesse liegt in der sicheren und funktionsfähigen Bereitstellung dieser Website (vgl. Erwägungsgrund 49 DSGVO; EuGH, C‑582/14, Breyer).</p>
<p><strong>Speicherdauer (Art. 13 Abs. 2 lit. a DSGVO).</strong> Eine feste Frist für GitHub-Pages-Protokolle nennt GitHub nicht (Stand: November 2026). Nach dem GitHub General Privacy Statement richtet sich die Speicherdauer nach dem Zweck der Erhebung und nach gesetzlichen Pflichten; Daten werden aufbewahrt, soweit dies zur Erfüllung vertraglicher Pflichten, zur Einhaltung gesetzlicher Vorgaben, zur Beilegung von Streitigkeiten und zur Durchsetzung von Vereinbarungen erforderlich ist. Ich selbst habe keinen Zugriff auf diese Protokolle, erhalte keine Besucherstatistiken und kann einzelne Besucher nicht identifizieren.</p>
<p><strong>Empfänger (Art. 13 Abs. 1 lit. e DSGVO).</strong> GitHub, Inc. sowie die Fastly, Inc. als von GitHub eingesetzter Dienstleister. Soweit GitHub die Verbindungsdaten zu eigenen Zwecken verarbeitet, insbesondere zur Sicherheit seiner Dienste, tritt GitHub nach seinen Datenschutzhinweisen selbst als Verantwortlicher auf (GitHub, Inc. bzw. GitHub B.V., Prins Bernhardplein 200, 1097 JB Amsterdam, Niederlande); insoweit gilt das <a href="[[U:gh_priv]]" rel="noopener">GitHub General Privacy Statement</a>.</p>
<p><strong>Übermittlung in die USA (Art. 13 Abs. 1 lit. f DSGVO).</strong> Die Daten werden auch in den USA verarbeitet. Die Übermittlung an die GitHub, Inc. und die Fastly, Inc. stützt sich auf den Angemessenheitsbeschluss der Europäischen Kommission zum EU-US-Datenschutzrahmen (Art. 45 Abs. 1 DSGVO in Verbindung mit dem Durchführungsbeschluss (EU) 2023/1795 vom 10. Juli 2023). Beide Unternehmen sind nach eigenen Angaben (<a href="[[U:gh_priv]]" rel="noopener">GitHub</a>, <a href="[[U:fastly_dpf]]" rel="noopener">Fastly</a>) nach dem EU-U.S. Data Privacy Framework zertifiziert; die Zertifizierungen sind in der <a href="[[U:dpf_list]]" rel="noopener">Data Privacy Framework List</a> des US-Handelsministeriums einsehbar. Für Übermittlungen in Drittländer ohne Angemessenheitsbeschluss stützt sich GitHub nach eigenen Angaben auf die Standardvertragsklauseln der Europäischen Kommission (Art. 46 Abs. 2 lit. c DSGVO in Verbindung mit dem Durchführungsbeschluss (EU) 2021/914 vom 4. Juni 2021); diese sind über EUR-Lex abrufbar (siehe Ziff. 15). Das Gericht der Europäischen Union hat die Nichtigkeitsklage gegen den Angemessenheitsbeschluss mit Urteil vom 3. September 2025 (Rs. T‑553/23, Latombe/Kommission) abgewiesen; hiergegen ist ein Rechtsmittel beim Gerichtshof anhängig (Rs. C‑703/25 P). Ändert sich die Rechtslage, wird diese Erklärung angepasst.</p>

<h2 id="s4">4. Cookies, Tracking und Zugriff auf Endeinrichtungen</h2>
<p>Diese Website setzt keine Cookies, bindet keine Analyse-, Reichweitenmess-, Tracking- oder Werbedienste ein und betreibt kein Profiling. Schriftarten, Skripte und Grafiken werden ausschließlich über diese Website selbst (GitHub Pages, Ziff. 3) und nicht über Drittanbieter ausgeliefert; Inhalte Dritter – etwa Webfont-Dienste, externe Skriptbibliotheken, Social-Media-Plugins, eingebettete Videos oder Karten – werden nicht eingebunden.</p>
<p>Die Website speichert keine Informationen in Ihrer Endeinrichtung; insbesondere werden weder Cookies noch Local Storage oder Session Storage verwendet. Skripte der Website werten lediglich lokal in Ihrem Browser Darstellungsmerkmale aus (etwa Fenstergröße, Pixeldichte und die Einstellung „Bewegung reduzieren“), ohne diese Informationen zu übermitteln. Soweit darin oder in der Zwischenspeicherung abgerufener Dateien durch Ihren Browser (Browser-Cache) ein Zugriff auf Informationen oder deren Speicherung im Sinne von § 25 Abs. 1 Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz (TDDDG) läge, wäre dies nach § 25 Abs. 2 Nr. 2 TDDDG zulässig, weil es unbedingt erforderlich ist, um den von Ihnen ausdrücklich gewünschten digitalen Dienst zur Verfügung zu stellen. Eine Einwilligung ist daher nicht erforderlich; ein Einwilligungsbanner wird nicht verwendet.</p>

<h2 id="s5">5. Domain und Namensauflösung</h2>
<p>Die Domain yevkaya.com ist bei der checkdomain GmbH, Große Burgstraße 27/29, 23552 Lübeck, registriert, deren Nameserver den Domainnamen in die Serveradressen von GitHub übersetzen. Bei dieser Namensauflösung wird regelmäßig nicht die IP-Adresse Ihres Endgeräts übermittelt, sondern die Ihres DNS-Resolvers (meist Ihres Internetzugangsanbieters).</p>

<h2 id="s6">6. Kontaktaufnahme per E-Mail</h2>
<p><strong>Verarbeitete Daten und Zweck.</strong> Wenn Sie mir eine E-Mail schreiben, verarbeite ich Ihre E-Mail-Adresse, Ihren Namen (sofern angegeben), den Inhalt Ihrer Nachricht einschließlich etwaiger Anhänge sowie die zugehörigen Metadaten (z.&#8239;B. Zeitpunkt des Versands), um Ihre Anfrage zu bearbeiten und zu beantworten.</p>
<p><strong>Rechtsgrundlage.</strong> Art. 6 Abs. 1 UAbs. 1 lit. b DSGVO, soweit Sie selbst Vertragspartei eines mit mir angestrebten oder bestehenden Vertrags sind. Schreiben Sie im Namen einer Organisation (etwa einer Hochschule oder eines Unternehmens, z.&#8239;B. wegen einer Stelle) oder liegt ein sonstiger Fall vor, ist Rechtsgrundlage Art. 6 Abs. 1 UAbs. 1 lit. f DSGVO; das berechtigte Interesse liegt in der sachgerechten Beantwortung der an mich gerichteten Anfragen.</p>
<p><strong>Auftragsverarbeiter.</strong> Das E-Mail-Postfach wird von der checkdomain GmbH, Große Burgstraße 27/29, 23552 Lübeck, als Auftragsverarbeiter (Art. 4 Nr. 8 DSGVO) auf Servern in Deutschland betrieben.[[AVV]] Eine Übermittlung in Drittländer findet insoweit nicht statt.</p>
<p><strong>Speicherdauer.</strong> Die Daten werden gelöscht, sobald sie für die Bearbeitung der Anfrage und eine sich daraus ergebende Zusammenarbeit nicht mehr erforderlich sind (Art. 17 Abs. 1 lit. a DSGVO); Korrespondenz ohne fortbestehende Zusammenarbeit wird spätestens zwei Jahre nach der letzten Nachricht gelöscht. Dies gilt nicht, soweit die weitere Speicherung zur Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen erforderlich ist (Art. 17 Abs. 3 lit. e DSGVO).</p>
<p><strong>Vertraulichkeit.</strong> E-Mails werden zwischen den beteiligten Servern in der Regel transportverschlüsselt (TLS) übertragen, sind jedoch nicht Ende-zu-Ende-verschlüsselt. Bitte übermitteln Sie keine besonderen Kategorien personenbezogener Daten (Art. 9 Abs. 1 DSGVO) per E-Mail.</p>

<h2 id="s7">7. Abruf des Lebenslaufs</h2>
<p>Der Lebenslauf wird als statische PDF-Datei über diese Website selbst (GitHub Pages) ausgeliefert; dabei fallen ausschließlich die unter Ziffer 3 beschriebenen Verbindungsdaten an. Die Datei enthält keine Skripte und lädt keine externen Inhalte nach; sie enthält lediglich anklickbare Verweise.</p>

<h2 id="s8">8. Links auf andere Websites</h2>
<p>Die Website enthält Links auf externe Angebote (z.&#8239;B. LinkedIn, GitHub, doi.org und Verlagsseiten). Eine Verbindung zum jeweiligen Anbieter wird erst hergestellt, wenn Sie einen solchen Link anklicken; zuvor werden an diesen keine Daten übermittelt. Beim Anklicken übermittelt Ihr Browser nach seinen Voreinstellungen in der Regel die Herkunftsadresse dieser Website (Referrer). Für die anschließende Verarbeitung ist der jeweilige Anbieter verantwortlich.</p>

<h2 id="s9">9. Datensicherheit</h2>
<p>Die Website wird ausschließlich über eine verschlüsselte Verbindung (HTTPS/TLS) ausgeliefert; unverschlüsselte Aufrufe werden auf HTTPS umgeleitet. Dies ist Teil der technischen und organisatorischen Maßnahmen nach Art. 32 Abs. 1 DSGVO.</p>

<h2 id="s10">10. Ihre Rechte</h2>
<p>Ihnen stehen nach Maßgabe der gesetzlichen Voraussetzungen folgende Rechte zu (Art. 13 Abs. 2 lit. b DSGVO):</p>
<ul>
<li>Auskunft über die Sie betreffenden Daten einschließlich einer Kopie (Art. 15 DSGVO),</li>
<li>Berichtigung unrichtiger Daten (Art. 16 DSGVO),</li>
<li>Löschung (Art. 17 DSGVO),</li>
<li>Einschränkung der Verarbeitung (Art. 18 DSGVO),</li>
<li>Mitteilung einer Berichtigung, Löschung oder Einschränkung an die Empfänger sowie auf Verlangen Unterrichtung über diese Empfänger (Art. 19 DSGVO),</li>
<li>Datenübertragbarkeit, soweit die Verarbeitung auf Art. 6 Abs. 1 UAbs. 1 lit. b DSGVO beruht und mithilfe automatisierter Verfahren erfolgt (Art. 20 DSGVO),</li>
<li>Widerspruch gegen die Verarbeitung (Art. 21 DSGVO, siehe Ziffer 11).</li>
</ul>
<p>Anträge können formlos per E-Mail an [[MAIL]] gestellt werden. Sie werden unverzüglich, spätestens innerhalb eines Monats nach Eingang beantwortet; diese Frist kann unter den Voraussetzungen des Art. 12 Abs. 3 Satz 2 DSGVO um weitere zwei Monate verlängert werden. Die Bearbeitung ist grundsätzlich unentgeltlich (Art. 12 Abs. 5 DSGVO). Bei begründeten Zweifeln an der Identität der antragstellenden Person können zusätzliche Informationen zu deren Bestätigung angefordert werden (Art. 12 Abs. 6 DSGVO).</p>
<p>Da keine Verarbeitung auf einer Einwilligung beruht, besteht kein Widerrufsrecht im Sinne von Art. 7 Abs. 3 DSGVO (Art. 13 Abs. 2 lit. c DSGVO).</p>

<h2 id="s11">11. Widerspruchsrecht nach Art. 21 DSGVO</h2>
<div class="callout">
<p><strong>Sie haben das Recht, aus Gründen, die sich aus Ihrer besonderen Situation ergeben, jederzeit gegen die Verarbeitung Sie betreffender personenbezogener Daten, die auf Grundlage von Art. 6 Abs. 1 UAbs. 1 lit. f DSGVO erfolgt, Widerspruch einzulegen (Art. 21 Abs. 1 DSGVO).</strong></p>
<p>Die Daten werden dann nicht mehr verarbeitet, es sei denn, es können zwingende schutzwürdige Gründe für die Verarbeitung nachgewiesen werden, die Ihre Interessen, Rechte und Freiheiten überwiegen, oder die Verarbeitung dient der Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen. Der Widerspruch kann formlos an [[MAIL]] gerichtet werden. Da ich auf die Server-Protokolle von GitHub keinen Zugriff habe, kann ein Widerspruch gegen diese Verarbeitung zusätzlich unmittelbar gegenüber GitHub erklärt werden.</p>
</div>

<h2 id="s12">12. Beschwerderecht und gerichtlicher Rechtsbehelf</h2>
<p>Unbeschadet eines anderweitigen verwaltungsrechtlichen oder gerichtlichen Rechtsbehelfs haben Sie das Recht auf Beschwerde bei einer Aufsichtsbehörde, insbesondere in dem Mitgliedstaat Ihres gewöhnlichen Aufenthaltsorts, Ihres Arbeitsplatzes oder des Orts des mutmaßlichen Verstoßes (Art. 77 Abs. 1 DSGVO). Für den Verantwortlichen zuständig ist das Bayerische Landesamt für Datenschutzaufsicht (BayLDA), Promenade 18, 91522 Ansbach, <a href="[[U:lda]]" rel="noopener">www.lda.bayern.de</a> (Art. 51, Art. 55 Abs. 1 DSGVO; § 40 Abs. 1 BDSG in Verbindung mit Art. 18 Abs. 1 Satz 1 Bayerisches Datenschutzgesetz – BayDSG). Zudem steht Ihnen der Weg zu den Gerichten offen (Art. 79 DSGVO).</p>

<h2 id="s13">13. Bereitstellungspflicht und automatisierte Entscheidungen</h2>
<p>Die Bereitstellung personenbezogener Daten ist weder gesetzlich noch vertraglich vorgeschrieben; Sie sind zur Bereitstellung nicht verpflichtet. Ohne Verarbeitung Ihrer IP-Adresse kann die Website jedoch technisch nicht ausgeliefert werden; ohne Angabe einer E-Mail-Adresse kann eine Anfrage – auch eine auf einen Vertragsschluss gerichtete – nicht beantwortet werden (Art. 13 Abs. 2 lit. e DSGVO). Eine automatisierte Entscheidungsfindung einschließlich Profiling im Sinne von Art. 22 Abs. 1 und 4 DSGVO findet nicht statt (Art. 13 Abs. 2 lit. f DSGVO).</p>

<h2 id="s14">14. Zweckänderung, Aktualisierung und Sprachfassungen</h2>
<p>Eine Weiterverarbeitung der Daten zu anderen als den hier genannten Zwecken ist nicht vorgesehen; sollte sie beabsichtigt sein, werden Sie zuvor nach Art. 13 Abs. 3 DSGVO informiert. Diese Datenschutzerklärung wird angepasst, sobald sich die Website, die eingesetzten Dienste oder die Rechtslage ändern. Sie steht zusätzlich in englischer und türkischer Sprache zur Verfügung; rechtlich maßgeblich ist ausschließlich die deutsche Fassung.</p>
"""

PRIVACY["en"] = """
<p class="lead">Information pursuant to Article 13 of the General Data Protection Regulation (Regulation (EU) 2016/679, GDPR) on the processing of personal data when you visit this website or contact me. Terms such as “personal data”, “processing”, “controller”, “processor” and “recipient” are used as defined in Art. 4 GDPR.</p>

[[TOC]]

<h2 id="s1">1. Controller</h2>
<p>The controller within the meaning of Art. 4(7) GDPR is:</p>
<p>[[ADDR]]<br />Email: [[MAIL]]</p>
<p>The controller is a natural person and therefore a non-public body within the meaning of § 2(4), first sentence, of the Federal Data Protection Act (BDSG). No data protection officer has been designated; the conditions for a designation obligation under Art. 37(1) GDPR and § 38(1) BDSG are not met.</p>

<h2 id="s2">2. Overview of processing operations</h2>
<div class="lg-table-wrap"><table class="lg-table">
<thead><tr><th>Processing and data</th><th>Purpose</th><th>Legal basis</th><th>Retention</th><th>Recipients, third country</th></tr></thead>
<tbody>
<tr><td><strong>Provision of the website</strong> (section 3): IP address, time, requested file, browser details, referrer</td><td>Delivery, stability and security of the website</td><td>Art. 6(1)(f) GDPR</td><td>according to GitHub’s criteria (section 3)</td><td>GitHub, Inc.; Fastly, Inc. (CDN); processing also in the USA – Art. 45(1) GDPR in conjunction with Implementing Decision (EU) 2023/1795</td></tr>
<tr><td><strong>Contact by email</strong> (section 6): email address, name, content, metadata</td><td>Handling and answering your enquiry</td><td>Art. 6(1)(b) or (f) GDPR</td><td>until the purpose is fulfilled; without an ongoing collaboration, at the latest two years after the last message (section 6)</td><td>checkdomain GmbH (processor), Germany; no third-country transfer</td></tr>
</tbody></table></div>
<p>No cookies and no analytics, tracking or advertising services are used (section 4).</p>

<h2 id="s3">3. Provision of the website (hosting on GitHub Pages)</h2>
<p><strong>Provider.</strong> The website is provided via GitHub Pages by GitHub, Inc., 88 Colin P. Kelly Jr. St., San Francisco, CA 94107, USA. GitHub delivers the pages through the content delivery network of Fastly, Inc., USA (GitHub lists Fastly as a “Content delivery service” in its <a href="[[U:gh_sub]]" rel="noopener">list of subprocessors</a>).</p>
<p><strong>Data processed.</strong> With every request, GitHub processes the connection data required for delivery, in particular the IP address of your device, the date and time of the request, the requested file and the details transmitted by your browser (e.g. browser type and version, operating system, referrer URL). According to GitHub, the IP addresses of visitors to GitHub Pages sites are logged and stored for security purposes (<a href="[[U:gh_pages]]" rel="noopener">GitHub Docs, “Data collection”</a>). IP addresses are treated as personal data (Art. 4(1) GDPR; cf. Court of Justice of the EU, judgment of 19 October 2016 – C‑582/14, Breyer).</p>
<p><strong>Purpose and legal basis (Art. 13(1)(c) and (d) GDPR).</strong> The processing serves to deliver the website, to ensure its stability and security, and to detect and prevent attacks and abuse. The legal basis is Art. 6(1)(f) GDPR; the legitimate interest lies in the secure and functional provision of this website (cf. Recital 49 GDPR; Court of Justice of the EU, C‑582/14, Breyer).</p>
<p><strong>Retention (Art. 13(2)(a) GDPR).</strong> GitHub does not specify a fixed period for GitHub Pages logs (as of November 2026). According to the GitHub General Privacy Statement, the retention period depends on the purpose of collection and on legal obligations; data are kept as needed to fulfil contractual obligations, comply with legal requirements, resolve disputes and enforce agreements. I have no access to these logs, receive no visitor statistics and cannot identify individual visitors.</p>
<p><strong>Recipients (Art. 13(1)(e) GDPR).</strong> GitHub, Inc. and Fastly, Inc. as a service provider engaged by GitHub. Insofar as GitHub processes the connection data for its own purposes, in particular the security of its services, GitHub acts as a controller in its own right according to its privacy information (GitHub, Inc. or GitHub B.V., Prins Bernhardplein 200, 1097 JB Amsterdam, the Netherlands); to that extent the <a href="[[U:gh_priv]]" rel="noopener">GitHub General Privacy Statement</a> applies.</p>
<p><strong>Transfer to the USA (Art. 13(1)(f) GDPR).</strong> The data are also processed in the USA. The transfer to GitHub, Inc. and Fastly, Inc. is based on the European Commission’s adequacy decision for the EU-U.S. Data Privacy Framework (Art. 45(1) GDPR in conjunction with Implementing Decision (EU) 2023/1795 of 10 July 2023). According to their own statements (<a href="[[U:gh_priv]]" rel="noopener">GitHub</a>, <a href="[[U:fastly_dpf]]" rel="noopener">Fastly</a>), both companies are certified under the EU-U.S. Data Privacy Framework; the certifications can be viewed in the U.S. Department of Commerce’s <a href="[[U:dpf_list]]" rel="noopener">Data Privacy Framework List</a>. For transfers to third countries without an adequacy decision, GitHub states that it relies on the European Commission’s standard contractual clauses (Art. 46(2)(c) GDPR in conjunction with Implementing Decision (EU) 2021/914 of 4 June 2021), which are available on EUR-Lex (see section 15). The General Court of the European Union dismissed the action for annulment of the adequacy decision by judgment of 3 September 2025 (Case T‑553/23, Latombe v Commission); an appeal is pending before the Court of Justice (Case C‑703/25 P). This policy will be updated should the legal situation change.</p>

<h2 id="s4">4. Cookies, tracking and access to terminal equipment</h2>
<p>This website sets no cookies, uses no analytics, audience-measurement, tracking or advertising services and carries out no profiling. Typefaces, scripts and graphics are delivered exclusively by this website itself (GitHub Pages, section 3) and not by third-party providers; no third-party content – such as web-font services, external script libraries, social-media plugins, embedded videos or maps – is embedded.</p>
<p>The website stores no information on your terminal equipment; in particular, neither cookies nor local storage or session storage are used. The website’s scripts merely evaluate display characteristics locally in your browser (such as window size, pixel density and the “reduce motion” setting) without transmitting this information. Insofar as this, or the caching of retrieved files by your browser (browser cache), constituted access to or storage of information within the meaning of § 25(1) of the Telecommunications Digital Services Data Protection Act (TDDDG), it would be permitted under § 25(2) no. 2 TDDDG, because it is strictly necessary to provide the digital service you have expressly requested. Consent is therefore not required, and no consent banner is used.</p>

<h2 id="s5">5. Domain and name resolution</h2>
<p>The domain yevkaya.com is registered with checkdomain GmbH, Große Burgstraße 27/29, 23552 Lübeck, Germany, whose name servers translate the domain name into GitHub’s server addresses. This lookup normally transmits the IP address of your DNS resolver (usually your internet access provider), not that of your device.</p>

<h2 id="s6">6. Contact by email</h2>
<p><strong>Data processed and purpose.</strong> If you email me, I process your email address, your name (if given), the content of your message including any attachments, and the related metadata (e.g. time of sending) in order to handle and answer your enquiry.</p>
<p><strong>Legal basis.</strong> Art. 6(1)(b) GDPR insofar as you yourself are a party to a contract with me that is envisaged or already exists. If you write on behalf of an organisation (such as a university or a company, e.g. regarding a position) or in any other case, the legal basis is Art. 6(1)(f) GDPR; the legitimate interest lies in properly answering the enquiries addressed to me.</p>
<p><strong>Processor.</strong> The mailbox is operated by checkdomain GmbH, Große Burgstraße 27/29, 23552 Lübeck, Germany, as processor (Art. 4(8) GDPR) on servers in Germany.[[AVV]] No transfer to third countries takes place in this respect.</p>
<p><strong>Retention.</strong> The data are erased once they are no longer necessary for handling the enquiry and any resulting collaboration (Art. 17(1)(a) GDPR); correspondence without an ongoing collaboration is erased at the latest two years after the last message. This does not apply where further storage is necessary for the establishment, exercise or defence of legal claims (Art. 17(3)(e) GDPR).</p>
<p><strong>Confidentiality.</strong> Emails are normally transport-encrypted (TLS) between the servers involved but are not end-to-end encrypted. Please do not send special categories of personal data (Art. 9(1) GDPR) by email.</p>

<h2 id="s7">7. Downloading the CV</h2>
<p>The CV is delivered as a static PDF file by this website itself (GitHub Pages); only the connection data described in section 3 are processed. The file contains no scripts and loads no external content; it contains only clickable links.</p>

<h2 id="s8">8. Links to other websites</h2>
<p>The website contains links to external services (e.g. LinkedIn, GitHub, doi.org and publisher pages). A connection to the provider concerned is established only when you click such a link; no data are transmitted to it beforehand. When you click, your browser normally transmits the address of this website (referrer) according to its default settings. The respective provider is responsible for any subsequent processing.</p>

<h2 id="s9">9. Data security</h2>
<p>The website is delivered exclusively over an encrypted connection (HTTPS/TLS); unencrypted requests are redirected to HTTPS. This forms part of the technical and organisational measures under Art. 32(1) GDPR.</p>

<h2 id="s10">10. Your rights</h2>
<p>Subject to the statutory conditions, you have the following rights (Art. 13(2)(b) GDPR):</p>
<ul>
<li>access to the data concerning you, including a copy (Art. 15 GDPR),</li>
<li>rectification of inaccurate data (Art. 16 GDPR),</li>
<li>erasure (Art. 17 GDPR),</li>
<li>restriction of processing (Art. 18 GDPR),</li>
<li>notification of any rectification, erasure or restriction to recipients and, on request, information about those recipients (Art. 19 GDPR),</li>
<li>data portability, where processing is based on Art. 6(1)(b) GDPR and carried out by automated means (Art. 20 GDPR),</li>
<li>objection to processing (Art. 21 GDPR, see section 11).</li>
</ul>
<p>Requests may be made informally by email to [[MAIL]]. They will be answered without undue delay and in any event within one month of receipt; this period may be extended by two further months under the conditions of Art. 12(3), second sentence, GDPR. Handling is in principle free of charge (Art. 12(5) GDPR). Where there are reasonable doubts as to the identity of the requesting person, additional information necessary to confirm their identity may be requested (Art. 12(6) GDPR).</p>
<p>As no processing is based on consent, there is no right of withdrawal within the meaning of Art. 7(3) GDPR (Art. 13(2)(c) GDPR).</p>

<h2 id="s11">11. Right to object under Art. 21 GDPR</h2>
<div class="callout">
<p><strong>You have the right to object at any time, on grounds relating to your particular situation, to the processing of personal data concerning you which is based on Art. 6(1)(f) GDPR (Art. 21(1) GDPR).</strong></p>
<p>The data will then no longer be processed unless compelling legitimate grounds for the processing can be demonstrated which override your interests, rights and freedoms, or the processing serves the establishment, exercise or defence of legal claims. The objection may be sent informally to [[MAIL]]. As I have no access to GitHub’s server logs, an objection to that processing may additionally be addressed directly to GitHub.</p>
</div>

<h2 id="s12">12. Right to lodge a complaint and judicial remedy</h2>
<p>Without prejudice to any other administrative or judicial remedy, you have the right to lodge a complaint with a supervisory authority, in particular in the Member State of your habitual residence, place of work or place of the alleged infringement (Art. 77(1) GDPR). The authority competent for the controller is the Bavarian Data Protection Authority (Bayerisches Landesamt für Datenschutzaufsicht, BayLDA), Promenade 18, 91522 Ansbach, Germany, <a href="[[U:lda]]" rel="noopener">www.lda.bayern.de</a> (Art. 51 and Art. 55(1) GDPR; § 40(1) BDSG in conjunction with Art. 18(1), first sentence, of the Bavarian Data Protection Act, BayDSG). You also have the right to an effective judicial remedy (Art. 79 GDPR).</p>

<h2 id="s13">13. Obligation to provide data and automated decision-making</h2>
<p>The provision of personal data is neither a statutory nor a contractual requirement; you are not obliged to provide personal data. Without processing your IP address, however, the website cannot be delivered; without an email address, an enquiry – including one aimed at concluding a contract – cannot be answered (Art. 13(2)(e) GDPR). No automated decision-making, including profiling, within the meaning of Art. 22(1) and (4) GDPR takes place (Art. 13(2)(f) GDPR).</p>

<h2 id="s14">14. Change of purpose, updates and language versions</h2>
<p>Further processing of the data for purposes other than those stated here is not intended; should it be intended, you will be informed beforehand in accordance with Art. 13(3) GDPR. This policy will be updated whenever the website, the services used or the legal situation change. It is also available in German and Turkish; only the German version is legally binding.</p>
"""

PRIVACY["tr"] = """
<p class="lead">Bu siteyi ziyaret ettiğinizde ve benimle iletişime geçtiğinizde kişisel verilerinizin işlenmesine ilişkin, Genel Veri Koruma Tüzüğü’nün ((AB) 2016/679 sayılı Tüzük, GDPR) 13. maddesi uyarınca bilgilendirme. “Kişisel veri”, “işleme”, “veri sorumlusu”, “veri işleyen” ve “alıcı” gibi kavramlar GDPR Art. 4’teki tanımlarıyla kullanılmıştır.</p>

[[TOC]]

<h2 id="s1">1. Veri sorumlusu</h2>
<p>GDPR Art. 4(7) anlamında veri sorumlusu:</p>
<p>[[ADDR]]<br />E-posta: [[MAIL]]</p>
<p>Veri sorumlusu bir gerçek kişidir ve bu nedenle § 2 Abs. 4 Satz 1 Federal Veri Koruma Kanunu (BDSG) anlamında kamu dışı bir birimdir (nichtöffentliche Stelle). Veri koruma görevlisi atanmamıştır; GDPR Art. 37(1) ve § 38 Abs. 1 BDSG kapsamındaki atama yükümlülüğünün koşulları mevcut değildir.</p>

<h2 id="s2">2. Veri işleme faaliyetlerine genel bakış</h2>
<div class="lg-table-wrap"><table class="lg-table">
<thead><tr><th>İşleme ve veriler</th><th>Amaç</th><th>Hukuki dayanak</th><th>Saklama süresi</th><th>Alıcılar, üçüncü ülke</th></tr></thead>
<tbody>
<tr><td><strong>Sitenin sunulması</strong> (madde 3): IP adresi, zaman, istenen dosya, tarayıcı bilgileri, yönlendiren adres</td><td>Sitenin iletimi, kararlılığı ve güvenliği</td><td>GDPR Art. 6(1)(f)</td><td>GitHub’ın kriterlerine göre (madde 3)</td><td>GitHub, Inc.; Fastly, Inc. (CDN); işleme ABD’de de yapılır – GDPR Art. 45(1) ile bağlantılı olarak (AB) 2023/1795 sayılı Uygulama Kararı</td></tr>
<tr><td><strong>E-posta ile iletişim</strong> (madde 6): e-posta adresi, ad, içerik, üst veriler</td><td>Talebin işlenmesi ve yanıtlanması</td><td>GDPR Art. 6(1)(b) veya (f)</td><td>amaç gerçekleşene kadar; devam eden bir iş birliği yoksa en geç son mesajdan iki yıl sonra (madde 6)</td><td>checkdomain GmbH (veri işleyen), Almanya; üçüncü ülkeye aktarım yok</td></tr>
</tbody></table></div>
<p>Çerez ve analiz, takip veya reklam hizmetleri kullanılmaz (madde 4).</p>

<h2 id="s3">3. Sitenin sunulması (GitHub Pages üzerinden barındırma)</h2>
<p><strong>Sağlayıcı.</strong> Site, GitHub, Inc. (88 Colin P. Kelly Jr. St., San Francisco, CA 94107, ABD) tarafından GitHub Pages üzerinden sunulmaktadır. GitHub sayfaları Fastly, Inc. (ABD) şirketinin içerik dağıtım ağı (CDN) üzerinden iletir (GitHub, <a href="[[U:gh_sub]]" rel="noopener">alt veri işleyenler listesinde</a> Fastly’yi “Content delivery service” olarak gösterir).</p>
<p><strong>İşlenen veriler.</strong> Her erişimde GitHub, iletim için gerekli bağlantı verilerini, özellikle cihazınızın IP adresini, isteğin tarih ve saatini, istenen dosyayı ve tarayıcınızın ilettiği bilgileri (ör. tarayıcı türü ve sürümü, işletim sistemi, yönlendiren URL) işler. GitHub’ın kendi açıklamasına göre GitHub Pages sitelerini ziyaret edenlerin IP adresleri güvenlik amacıyla kaydedilir ve saklanır (<a href="[[U:gh_pages]]" rel="noopener">GitHub Docs, “Data collection”</a>). IP adresleri kişisel veri olarak değerlendirilir (GDPR Art. 4(1); bkz. ABAD, 19 Ekim 2016 tarihli karar – C‑582/14, Breyer).</p>
<p><strong>Amaç ve hukuki dayanak (GDPR Art. 13(1)(c) ve (d)).</strong> İşleme; sitenin iletilmesine, kararlılığının ve güvenliğinin sağlanmasına, saldırı ve kötüye kullanımın tespit edilip önlenmesine hizmet eder. Hukuki dayanak GDPR Art. 6(1)(f)’dir; meşru menfaat, bu sitenin güvenli ve işlevsel biçimde sunulmasıdır (bkz. GDPR Gerekçe 49; ABAD, C‑582/14, Breyer).</p>
<p><strong>Saklama süresi (GDPR Art. 13(2)(a)).</strong> GitHub, GitHub Pages kayıtları için sabit bir süre belirtmemektedir (Kasım 2026 itibarıyla). GitHub General Privacy Statement’a göre saklama süresi, toplama amacına ve yasal yükümlülüklere bağlıdır; veriler sözleşmeye dayalı yükümlülüklerin yerine getirilmesi, yasal gerekliliklere uyulması, uyuşmazlıkların çözülmesi ve sözleşmelerin uygulanması için gerekli olduğu sürece saklanır. Bu kayıtlara erişimim yoktur; ziyaretçi istatistikleri almam ve tek tek ziyaretçileri tanımlayamam.</p>
<p><strong>Alıcılar (GDPR Art. 13(1)(e)).</strong> GitHub, Inc. ve GitHub’ın kullandığı hizmet sağlayıcı olarak Fastly, Inc. GitHub bağlantı verilerini kendi amaçları için, özellikle hizmetlerinin güvenliği için işlediği ölçüde, kendi veri koruma açıklamalarına göre bizzat veri sorumlusu sıfatıyla hareket eder (GitHub, Inc. veya GitHub B.V., Prins Bernhardplein 200, 1097 JB Amsterdam, Hollanda); bu kapsamda <a href="[[U:gh_priv]]" rel="noopener">GitHub General Privacy Statement</a> geçerlidir.</p>
<p><strong>ABD’ye aktarım (GDPR Art. 13(1)(f)).</strong> Veriler ABD’de de işlenir. GitHub, Inc. ve Fastly, Inc.’e aktarım, Avrupa Komisyonu’nun AB-ABD Veri Gizliliği Çerçevesi’ne ilişkin yeterlilik kararına dayanır (GDPR Art. 45(1) ile bağlantılı olarak 10 Temmuz 2023 tarihli (AB) 2023/1795 sayılı Uygulama Kararı). Her iki şirket de kendi açıklamalarına göre (<a href="[[U:gh_priv]]" rel="noopener">GitHub</a>, <a href="[[U:fastly_dpf]]" rel="noopener">Fastly</a>) EU-U.S. Data Privacy Framework kapsamında sertifikalıdır; sertifikalar ABD Ticaret Bakanlığı’nın <a href="[[U:dpf_list]]" rel="noopener">Data Privacy Framework List</a> adlı listesinde görülebilir. GitHub, yeterlilik kararı bulunmayan üçüncü ülkelere aktarımlarda kendi açıklamasına göre Avrupa Komisyonu’nun standart sözleşme maddelerine dayanır (GDPR Art. 46(2)(c) ile bağlantılı olarak 4 Haziran 2021 tarihli (AB) 2021/914 sayılı Uygulama Kararı); bu maddelere EUR-Lex üzerinden erişilebilir (bkz. madde 15). Avrupa Birliği Genel Mahkemesi, yeterlilik kararına karşı açılan iptal davasını 3 Eylül 2025 tarihli kararıyla (T‑553/23, Latombe/Komisyon) reddetmiştir; bu karara karşı Adalet Divanı nezdinde temyiz başvurusu derdesttir (C‑703/25 P). Hukuki durum değişirse bu metin güncellenecektir.</p>

<h2 id="s4">4. Çerezler, takip ve uç cihazlara erişim</h2>
<p>Bu site çerez kullanmaz; analiz, erişim ölçümü, takip veya reklam hizmetleri içermez ve profil oluşturmaz. Yazı tipleri, betikler ve grafikler yalnızca bu sitenin kendisi (GitHub Pages, madde 3) üzerinden sunulur, üçüncü taraf sağlayıcılar üzerinden sunulmaz; web yazı tipi hizmetleri, harici betik kütüphaneleri, sosyal medya eklentileri, gömülü videolar veya haritalar gibi üçüncü taraf içerikleri kullanılmaz.</p>
<p>Site uç cihazınızda bilgi saklamaz; özellikle çerez, local storage veya session storage kullanılmaz. Sitenin betikleri yalnızca tarayıcınızda yerel olarak görüntüleme özelliklerini (ör. pencere boyutu, piksel yoğunluğu ve “hareketi azalt” ayarı) değerlendirir ve bu bilgileri iletmez. Bu değerlendirme veya indirilen dosyaların tarayıcınız tarafından önbelleğe alınması (browser cache) § 25 Abs. 1 Telekomünikasyon ve Dijital Hizmetlerde Veri Koruma Kanunu (TDDDG) anlamında bilgiye erişim ya da bilgi saklama sayılsaydı bile, açıkça talep ettiğiniz dijital hizmetin sunulması için kesinlikle gerekli olduğundan § 25 Abs. 2 Nr. 2 TDDDG uyarınca izinli olurdu. Bu nedenle rıza alınması gerekmez ve rıza (çerez) bandı kullanılmaz.</p>

<h2 id="s5">5. Alan adı ve ad çözümleme</h2>
<p>yevkaya.com alan adı, checkdomain GmbH (Große Burgstraße 27/29, 23552 Lübeck, Almanya) nezdinde kayıtlıdır; bu şirketin ad sunucuları alan adını GitHub’ın sunucu adreslerine çevirir. Bu sorguda genellikle cihazınızın IP adresi değil, DNS çözümleyicinizin (çoğunlukla internet erişim sağlayıcınızın) IP adresi iletilir.</p>

<h2 id="s6">6. E-posta ile iletişim</h2>
<p><strong>İşlenen veriler ve amaç.</strong> Bana e-posta gönderirseniz talebinizi işlemek ve yanıtlamak için e-posta adresinizi, (belirttiyseniz) adınızı, varsa ekleri dâhil mesajınızın içeriğini ve ilgili üst verileri (ör. gönderim zamanı) işlerim.</p>
<p><strong>Hukuki dayanak.</strong> Benimle kurulması amaçlanan veya mevcut bir sözleşmenin tarafı bizzat sizseniz GDPR Art. 6(1)(b). Bir kurum adına yazıyorsanız (ör. bir üniversite veya şirket adına, örneğin bir pozisyonla ilgili) ya da başka bir durum söz konusuysa hukuki dayanak GDPR Art. 6(1)(f)’dir; meşru menfaat, bana yöneltilen taleplerin gereği gibi yanıtlanmasıdır.</p>
<p><strong>Veri işleyen.</strong> E-posta kutusu, checkdomain GmbH (Große Burgstraße 27/29, 23552 Lübeck) tarafından veri işleyen sıfatıyla (GDPR Art. 4(8)) Almanya’daki sunucularda işletilmektedir.[[AVV]] Bu kapsamda üçüncü ülkelere aktarım yapılmaz.</p>
<p><strong>Saklama süresi.</strong> Veriler, talebin işlenmesi ve bundan doğabilecek bir iş birliği için artık gerekli olmadığında silinir (GDPR Art. 17(1)(a)); devam eden bir iş birliği bulunmayan yazışmalar en geç son mesajdan iki yıl sonra silinir. Ancak hukuki taleplerin ileri sürülmesi, kullanılması veya savunulması için gerekli oldukları sürece veriler saklanabilir (GDPR Art. 17(3)(e)).</p>
<p><strong>Gizlilik.</strong> E-postalar ilgili sunucular arasında genellikle aktarım sırasında şifrelenir (TLS), ancak uçtan uca şifreli değildir. Lütfen özel nitelikli kişisel verileri (GDPR Art. 9(1)) e-posta ile göndermeyin.</p>

<h2 id="s7">7. Özgeçmişin indirilmesi</h2>
<p>Özgeçmiş, doğrudan bu site (GitHub Pages) üzerinden statik bir PDF dosyası olarak iletilir; bu sırada yalnızca 3. maddede açıklanan bağlantı verileri işlenir. Dosya betik içermez ve harici içerik yüklemez; yalnızca tıklanabilir bağlantılar içerir.</p>

<h2 id="s8">8. Diğer sitelere bağlantılar</h2>
<p>Site harici hizmetlere (ör. LinkedIn, GitHub, doi.org ve yayınevi sayfaları) bağlantılar içerir. İlgili sağlayıcıyla bağlantı ancak böyle bir bağlantıya tıkladığınızda kurulur; öncesinde ona hiçbir veri iletilmez. Tıkladığınızda tarayıcınız, varsayılan ayarlarına göre genellikle bu sitenin adresini (referrer) iletir. Sonraki işlemeden ilgili sağlayıcı sorumludur.</p>

<h2 id="s9">9. Veri güvenliği</h2>
<p>Site yalnızca şifreli bağlantı (HTTPS/TLS) üzerinden sunulur; şifresiz istekler HTTPS’e yönlendirilir. Bu, GDPR Art. 32(1) kapsamındaki teknik ve idari tedbirlerin bir parçasıdır.</p>

<h2 id="s10">10. Haklarınız</h2>
<p>Yasal koşullar çerçevesinde şu haklara sahipsiniz (GDPR Art. 13(2)(b)):</p>
<ul>
<li>sizinle ilgili verilere, bir kopyası dâhil, erişim (GDPR Art. 15),</li>
<li>yanlış verilerin düzeltilmesi (GDPR Art. 16),</li>
<li>silme (GDPR Art. 17),</li>
<li>işlemenin kısıtlanması (GDPR Art. 18),</li>
<li>düzeltme, silme veya kısıtlamanın alıcılara bildirilmesi ve talebiniz hâlinde bu alıcılar hakkında bilgilendirilme (GDPR Art. 19),</li>
<li>işleme GDPR Art. 6(1)(b)’ye dayandığı ve otomatik yollarla yapıldığı ölçüde veri taşınabilirliği (GDPR Art. 20),</li>
<li>işlemeye itiraz (GDPR Art. 21, bkz. madde 11).</li>
</ul>
<p>Talepler [[MAIL]] adresine gönderilecek basit bir e-postayla iletilebilir. Talepler gecikmeksizin, en geç alındıktan sonraki bir ay içinde yanıtlanır; bu süre GDPR Art. 12(3) ikinci cümlesindeki koşullarda iki ay daha uzatılabilir. İşlem kural olarak ücretsizdir (GDPR Art. 12(5)). Başvuru sahibinin kimliği konusunda makul şüphe bulunması hâlinde kimliğin doğrulanması için ek bilgi istenebilir (GDPR Art. 12(6)).</p>
<p>Hiçbir işleme rızaya dayanmadığından GDPR Art. 7(3) anlamında rızayı geri alma hakkı söz konusu değildir (GDPR Art. 13(2)(c)).</p>

<h2 id="s11">11. GDPR Art. 21 uyarınca itiraz hakkı</h2>
<div class="callout">
<p><strong>Sizinle ilgili kişisel verilerin GDPR Art. 6(1)(f)’ye dayanılarak işlenmesine, özel durumunuzdan kaynaklanan nedenlerle her zaman itiraz etme hakkına sahipsiniz (GDPR Art. 21(1)).</strong></p>
<p>Bu durumda, menfaatlerinizin, haklarınızın ve özgürlüklerinizin önüne geçen zorlayıcı meşru gerekçeler ispat edilemedikçe veya işleme hukuki taleplerin ileri sürülmesi, kullanılması ya da savunulması için gerekli olmadıkça veriler artık işlenmez. İtiraz [[MAIL]] adresine şekle bağlı olmaksızın iletilebilir. GitHub’ın sunucu kayıtlarına erişimim olmadığından bu işlemeye yönelik itiraz ayrıca doğrudan GitHub’a da yöneltilebilir.</p>
</div>

<h2 id="s12">12. Şikâyet hakkı ve yargı yolu</h2>
<p>Diğer idari veya yargısal başvuru yolları saklı kalmak kaydıyla, özellikle mutat meskeninizin, işyerinizin veya iddia edilen ihlalin gerçekleştiği yerin bulunduğu üye devlette bir denetim makamına şikâyette bulunma hakkına sahipsiniz (GDPR Art. 77(1)). Veri sorumlusu bakımından yetkili makam Bavyera Veri Koruma Denetim Dairesi’dir (Bayerisches Landesamt für Datenschutzaufsicht, BayLDA), Promenade 18, 91522 Ansbach, Almanya, <a href="[[U:lda]]" rel="noopener">www.lda.bayern.de</a> (GDPR Art. 51 ve Art. 55(1); Art. 18 Abs. 1 Satz 1 Bavyera Veri Koruma Kanunu – BayDSG ile bağlantılı olarak § 40 Abs. 1 BDSG). Ayrıca etkili bir yargısal başvuru hakkınız vardır (GDPR Art. 79).</p>

<h2 id="s13">13. Veri sağlama yükümlülüğü ve otomatik kararlar</h2>
<p>Kişisel veri sağlamak yasal bir gereklilik veya sözleşmeye dayalı bir gereklilik değildir; kişisel veri sağlamakla yükümlü değilsiniz. Ancak IP adresiniz işlenmeden site teknik olarak sunulamaz; bir e-posta adresi olmadan da – bir sözleşme kurulmasına yönelik olanlar dâhil – talepler yanıtlanamaz (GDPR Art. 13(2)(e)). GDPR Art. 22(1) ve (4) anlamında profilleme dâhil otomatik karar verme yapılmamaktadır (GDPR Art. 13(2)(f)).</p>

<h2 id="s14">14. Amaç değişikliği, güncelleme ve dil sürümleri</h2>
<p>Verilerin burada belirtilenler dışındaki amaçlarla işlenmesi öngörülmemektedir; böyle bir niyet olursa GDPR Art. 13(3) uyarınca önceden bilgilendirilirsiniz. Bu metin; site, kullanılan hizmetler veya mevzuat değiştiğinde güncellenir. Metin Almanca ve İngilizce olarak da mevcuttur; hukuken bağlayıcı olan yalnızca Almanca metindir.</p>
"""

PRIVACY_SOURCES = {
    "de": [
        ("[[EU:32016R0679]]", "Verordnung (EU) 2016/679 des Europäischen Parlaments und des Rates vom 27. April 2016 zum Schutz natürlicher Personen bei der Verarbeitung personenbezogener Daten, zum freien Datenverkehr und zur Aufhebung der Richtlinie 95/46/EG (Datenschutz-Grundverordnung), ABl. L 119 vom 4.5.2016, S. 1", ""),
        ("[[EU:32023D1795]]", "Durchführungsbeschluss (EU) 2023/1795 der Kommission vom 10. Juli 2023 gemäß der Verordnung (EU) 2016/679 des Europäischen Parlaments und des Rates über die Angemessenheit des Schutzniveaus für personenbezogene Daten nach dem Datenschutzrahmen EU-USA, ABl. L 231 vom 20.9.2023, S. 118", ""),
        ("[[EU:32021D0914]]", "Durchführungsbeschluss (EU) 2021/914 der Kommission vom 4. Juni 2021 über Standardvertragsklauseln für die Übermittlung personenbezogener Daten an Drittländer gemäß der Verordnung (EU) 2016/679 des Europäischen Parlaments und des Rates, ABl. L 199 vom 7.6.2021, S. 31", ""),
        ("[[U:bdsg]]", "Bundesdatenschutzgesetz (BDSG) vom 30. Juni 2017 (BGBl. I S. 2097)", "§§ 2, 38, 40"),
        ("[[U:tdddg25]]", "Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz (TDDDG) vom 23. Juni 2021 (BGBl. I S. 1982; 2022 I S. 1045)", "§ 25"),
        ("[[U:baydsg18]]", "Bayerisches Datenschutzgesetz (BayDSG) vom 15. Mai 2018 (GVBl. S. 230)", "Art. 18"),
        ("[[EU:62014CJ0582]]", "EuGH, Urteil vom 19. Oktober 2016 – C‑582/14 (Breyer), ECLI:EU:C:2016:779", ""),
        ("[[EU:62023TJ0553]]", "EuG, Urteil vom 3. September 2025 – T‑553/23 (Latombe/Kommission); Rechtsmittel anhängig: EuGH – C‑703/25 P", ""),
    ],
    "en": [
        ("[[EU:32016R0679]]", "Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation), OJ L 119, 4.5.2016, p. 1", ""),
        ("[[EU:32023D1795]]", "Commission Implementing Decision (EU) 2023/1795 of 10 July 2023 pursuant to Regulation (EU) 2016/679 of the European Parliament and of the Council on the adequate level of protection of personal data under the EU-US Data Privacy Framework, OJ L 231, 20.9.2023, p. 118", ""),
        ("[[EU:32021D0914]]", "Commission Implementing Decision (EU) 2021/914 of 4 June 2021 on standard contractual clauses for the transfer of personal data to third countries pursuant to Regulation (EU) 2016/679 of the European Parliament and of the Council, OJ L 199, 7.6.2021, p. 31", ""),
        ("[[U:bdsg]]", "Bundesdatenschutzgesetz (BDSG) [Federal Data Protection Act] of 30 June 2017 (BGBl. I S. 2097)", "§§ 2, 38, 40"),
        ("[[U:tdddg25]]", "Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz (TDDDG) [Telecommunications Digital Services Data Protection Act] of 23 June 2021 (BGBl. I S. 1982; 2022 I S. 1045)", "§ 25"),
        ("[[U:baydsg18]]", "Bayerisches Datenschutzgesetz (BayDSG) [Bavarian Data Protection Act] of 15 May 2018 (GVBl. S. 230)", "Art. 18"),
        ("[[EU:62014CJ0582]]", "Court of Justice of the EU, judgment of 19 October 2016 – C‑582/14 (Breyer), ECLI:EU:C:2016:779", ""),
        ("[[EU:62023TJ0553]]", "General Court of the EU, judgment of 3 September 2025 – T‑553/23 (Latombe v Commission); appeal pending: Court of Justice – C‑703/25 P", ""),
    ],
    "tr": [
        ("[[EU:32016R0679]]", "Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation), OJ L 119, 4.5.2016, p. 1", ""),
        ("[[EU:32023D1795]]", "Commission Implementing Decision (EU) 2023/1795 of 10 July 2023 pursuant to Regulation (EU) 2016/679 of the European Parliament and of the Council on the adequate level of protection of personal data under the EU-US Data Privacy Framework, OJ L 231, 20.9.2023, p. 118", ""),
        ("[[EU:32021D0914]]", "Commission Implementing Decision (EU) 2021/914 of 4 June 2021 on standard contractual clauses for the transfer of personal data to third countries pursuant to Regulation (EU) 2016/679 of the European Parliament and of the Council, OJ L 199, 7.6.2021, p. 31", ""),
        ("[[U:bdsg]]", "Bundesdatenschutzgesetz (BDSG) [Federal Veri Koruma Kanunu], 30 Haziran 2017 (BGBl. I S. 2097)", "§§ 2, 38, 40"),
        ("[[U:tdddg25]]", "Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz (TDDDG) [Telekomünikasyon ve Dijital Hizmetlerde Veri Koruma Kanunu], 23 Haziran 2021 (BGBl. I S. 1982; 2022 I S. 1045)", "§ 25"),
        ("[[U:baydsg18]]", "Bayerisches Datenschutzgesetz (BayDSG) [Bavyera Veri Koruma Kanunu], 15 Mayıs 2018 (GVBl. S. 230)", "Art. 18"),
        ("[[EU:62014CJ0582]]", "ABAD, 19 Ekim 2016 tarihli karar – C‑582/14 (Breyer), ECLI:EU:C:2016:779", ""),
        ("[[EU:62023TJ0553]]", "AB Genel Mahkemesi, 3 Eylül 2025 tarihli karar – T‑553/23 (Latombe/Komisyon); temyiz derdest: ABAD – C‑703/25 P", ""),
    ],
}

SOURCES_HEAD = {
    "de": ("Rechtsquellen", "Maßgeblich ist jeweils die geltende Fassung. Die Verweise führen zu den Rechtsportalen des Bundes (gesetze-im-internet.de) und des Freistaats Bayern (gesetze-bayern.de) sowie zu EUR-Lex; die dort bereitgestellten konsolidierten Fassungen sind nichtamtlich. Rechtlich maßgeblich sind allein die in den amtlichen Verkündungsblättern (BGBl., GVBl.) und im Amtsblatt der Europäischen Union veröffentlichten Texte."),
    "en": ("Legal sources", "In each case the version currently in force applies. The links lead to the legal information portals of the Federal Government (gesetze-im-internet.de) and the Free State of Bavaria (gesetze-bayern.de) and to EUR-Lex; the consolidated texts provided there are not official. Only the texts published in the official gazettes (BGBl., GVBl.) and in the Official Journal of the European Union are legally authoritative."),
    "tr": ("Hukuki kaynaklar", "Her durumda yürürlükteki sürüm esastır. Bağlantılar Federal Hükûmetin (gesetze-im-internet.de) ve Bavyera Eyaleti’nin (gesetze-bayern.de) hukuk portallarına ve EUR-Lex’e yönlendirir; buradaki konsolide metinler resmî değildir. Hukuken yalnızca resmî yayın organlarında (BGBl., GVBl.) ve Avrupa Birliği Resmî Gazetesi’nde yayımlanan metinler esastır."),
}


# ============================================================================================ page shell
STYLE = """
      body.legal { margin: 0; color: var(--ink); background: var(--paper); }
      .lg-header { position: sticky; top: 0; z-index: 5; display: flex; align-items: center; justify-content: space-between; gap: 16px; height: 72px; padding: 0 clamp(16px, 4vw, 48px); color: #eef6f1; background: #07100e; border-bottom: 1px solid var(--line-dark); }
      .lg-header .wordmark { display: inline-flex; align-items: center; gap: 12px; color: inherit; text-decoration: none; }
      .lg-header .wordmark-mark { display: grid; place-items: center; width: 34px; height: 34px; border: 1px solid rgba(121, 227, 225, 0.5); color: var(--mint); font-family: var(--display); font-size: 0.92rem; letter-spacing: 0.04em; }
      .lg-header .wordmark-text { font-family: var(--display); font-size: 1.12rem; letter-spacing: -0.01em; }
      .lg-tools { display: flex; align-items: center; gap: 22px; }
      .lg-back { color: #b9c7c0; font-family: var(--mono); font-size: 0.66rem; letter-spacing: 0.14em; text-transform: uppercase; text-decoration: none; }
      .lg-back:hover, .lg-back:focus-visible { color: var(--mint); }
      .lg-header .lang-switch { margin: 0; }
      .lg-header .lang-switch a { padding: 5px 8px; color: #eef6f1; font-family: var(--mono); font-size: 0.6rem; letter-spacing: 0.16em; text-decoration: none; opacity: 0.62; }
      .lg-header .lang-switch a:hover, .lg-header .lang-switch a:focus-visible { opacity: 1; }
      .lg-header .lang-switch a[aria-current="page"] { color: #04110e; background: var(--flux); opacity: 1; }
      .lg-main { width: min(820px, calc(100vw - 40px)); margin: 0 auto; padding: clamp(40px, 7vw, 88px) 0 72px; }
      .lg-kicker { margin: 0 0 18px; color: var(--mint-strong); font-family: var(--mono); font-size: 0.68rem; letter-spacing: 0.22em; text-transform: uppercase; }
      .lg-kicker::before { display: inline-block; width: 28px; height: 1px; margin: 0 12px 4px 0; content: ""; background: currentColor; vertical-align: middle; }
      .lg-main h1 { margin: 0 0 14px; font-family: var(--display); font-size: clamp(2.4rem, 5.4vw, 3.6rem); font-weight: 500; letter-spacing: -0.025em; line-height: 1.04; }
      .lg-main .lead { margin: 0 0 8px; color: var(--ink-soft); font-family: var(--text); font-size: 1.08rem; font-style: italic; line-height: 1.55; }
      .lg-note { margin: 22px 0 0; padding: 12px 16px; border-left: 2px solid var(--mint-strong); background: rgba(36, 184, 182, 0.07); color: var(--ink-soft); font-family: var(--text); font-size: 0.96rem; line-height: 1.55; }
      .lg-note a { color: #0f6e6c; }
      .lg-toc { margin: 30px 0 6px; padding: 18px 22px; border: 1px solid rgba(18, 32, 29, 0.14); background: var(--paper-bright); }
      .lg-toc p { margin: 0 0 8px; color: var(--ink-soft); font-family: var(--mono); font-size: 0.66rem; letter-spacing: 0.16em; text-transform: uppercase; }
      .lg-toc ol { margin: 0; padding: 0; columns: 2; column-gap: 28px; list-style: none; }
      .lg-toc li { margin: 0 0 5px; font-family: var(--text); font-size: 0.95rem; line-height: 1.4; break-inside: avoid; }
      .lg-body .lg-toc a { color: var(--ink); text-decoration: none; }
      .lg-body .lg-toc a:hover { color: #0f6e6c; text-decoration: underline; }
      .lg-body h2 { margin: 44px 0 12px; padding-top: 18px; border-top: 1px solid rgba(18, 32, 29, 0.12); font-family: var(--display); font-size: 1.55rem; font-weight: 600; letter-spacing: -0.01em; line-height: 1.2; scroll-margin-top: 90px; }
      .lg-body p, .lg-body li { font-family: var(--text); font-size: 1.04rem; line-height: 1.68; }
      .lg-body p { margin: 0 0 14px; }
      .lg-body p.fine { margin-top: -6px; color: var(--ink-soft); font-size: 0.92rem; }
      .lg-body ul { margin: 0 0 16px; padding-left: 1.2em; }
      .lg-body li { margin: 0 0 6px; }
      .lg-body a { color: #0f6e6c; text-decoration: underline; text-decoration-color: rgba(15, 110, 108, 0.4); text-underline-offset: 2px; overflow-wrap: anywhere; }
      .lg-body a:hover { text-decoration-color: currentColor; }
      .lg-body code { font-family: var(--mono); font-size: 0.86em; }
      .lg-body strong { font-weight: 600; }
      .lg-table-wrap { margin: 6px 0 14px; overflow-x: auto; border: 1px solid rgba(18, 32, 29, 0.16); background: var(--paper-bright); }
      .lg-table { width: 100%; min-width: 720px; border-collapse: collapse; font-family: var(--text); font-size: 0.9rem; line-height: 1.45; }
      .lg-table th { padding: 10px 12px; color: var(--ink-soft); font-family: var(--mono); font-size: 0.6rem; font-weight: 500; letter-spacing: 0.12em; text-align: left; text-transform: uppercase; vertical-align: bottom; border-bottom: 1px solid rgba(18, 32, 29, 0.2); }
      .lg-table td { padding: 10px 12px; vertical-align: top; border-bottom: 1px solid rgba(18, 32, 29, 0.1); }
      .lg-table tr:last-child td { border-bottom: 0; }
      .callout { margin: 18px 0 20px; padding: 16px 20px 4px; border: 1px solid rgba(18, 32, 29, 0.28); border-left: 3px solid var(--mint-strong); background: var(--paper-bright); }
      .lg-sources { margin: 0 0 16px; padding-left: 1.4em; }
      .lg-sources li { margin: 0 0 8px; font-size: 0.95rem; line-height: 1.5; }
      .lg-sources .norm { color: var(--ink-soft); font-family: var(--mono); font-size: 0.78rem; white-space: nowrap; }
      .lg-stand { margin: 48px 0 0; color: var(--ink-soft); font-family: var(--mono); font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase; }
      .lg-footer { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px 24px; padding: 24px clamp(16px, 4vw, 48px); color: #8f9d97; background: #07100e; font-family: var(--mono); font-size: 0.66rem; letter-spacing: 0.08em; text-transform: uppercase; }
      .lg-footer a { color: #becac4; text-decoration: none; }
      .lg-footer a:hover, .lg-footer a[aria-current] { color: var(--mint); }
      .lg-footer nav { display: flex; gap: 18px; }
      @media (max-width: 560px) { .lg-header .wordmark-text, .lg-back { display: none; } .lg-toc ol { columns: 1; } }
      @media print { .lg-header, .lg-footer, .lg-toc, .skip-link { display: none !important; } body.legal { background: #fff; } .lg-main { width: auto; padding: 0; } .lg-table { min-width: 0; } }
"""


def rel(frm, to):
    """relative link from page path frm to site path to"""
    depth = frm.count("/")
    return "../" * depth + to if to else ("../" * depth or "./")


def sources_html(items, lang):
    head, note = SOURCES_HEAD[lang]
    out = [f'<h2 id="src">{head}</h2>', f'<p class="fine">{note}</p>', '<ol class="lg-sources">']
    for url, title, norm in items:
        t = f'<a href="{url}" rel="noopener">{title}</a>' if url else title
        n = f' <span class="norm">– {norm}</span>' if norm else ""
        out.append(f"<li>{t}{n}</li>")
    out.append("</ol>")
    return "\n".join(out)


def fill(s, lang, me):
    s = s.replace("[[ADDRNOTE]]", "" if ADDRESS else f'\n<p class="fine">{ADDRESS_PENDING[lang]}</p>')
    s = s.replace("[[MAIL]]", MAIL).replace("[[ADDR]]", addr(lang))
    s = s.replace("[[AVV]]", AVV[lang] if CHECKDOMAIN_AVV else "")
    s = s.replace("[[PRIV]]", f'<a href="{rel(me, PATHS["privacy"][lang])}">{UI[lang]["privlink"]}</a>')
    s = re.sub(r"\[\[U:(\w+)\]\]", lambda m: URL[m.group(1)], s)
    s = re.sub(r"\[\[EU:(\w+)\]\]", lambda m: eurlex(m.group(1), lang), s)
    return s


def toc(body, lang):
    items = re.findall(r'<h2 id="(s\d+|src)">(.*?)</h2>', body)
    lis = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items)
    return f'<nav class="lg-toc" aria-label="{UI[lang]["toc"]}"><p>{UI[lang]["toc"]}</p><ol>{lis}</ol></nav>'


def page(kind, lang):
    me = PATHS[kind][lang]
    ui = UI[lang]
    up = "../" * me.count("/")
    title = ui[kind]
    if kind == "imprint":
        body = IMPRINT[lang] + sources_html(IMPRINT_SOURCES[lang], lang)
    else:
        src = sources_html(PRIVACY_SOURCES[lang], lang).replace('<h2 id="src">', '<h2 id="s15">15. ', 1)
        body = PRIVACY[lang] + src
        body = body.replace("[[TOC]]", toc(body, lang))
    body = fill(body, lang, me)
    cur = ' aria-current="page"'
    switch = "".join(
        f'<a href="{rel(me, PATHS[kind][c])}" lang="{c}" hreflang="{c}"{cur if c == lang else ""}>{c.upper()}</a>'
        for c in ("en", "tr", "de"))
    alts = "".join(f'    <link rel="alternate" hreflang="{c}" href="{BASE}/{PATHS[kind][c]}" />\n' for c in ("en", "tr", "de"))
    alts += f'    <link rel="alternate" hreflang="x-default" href="{BASE}/{PATHS[kind]["en"]}" />\n'
    note = f'<p class="lg-note">{ui["note"].replace("[[DE]]", rel(me, PATHS[kind]["de"]))}</p>' if ui["note"] else ""
    foot_links = "".join(
        f'<a href="{rel(me, PATHS[k][lang])}"{cur if k == kind else ""}>{UI[lang][k]}</a>'
        for k in ("imprint", "privacy"))
    home = rel(me, HOME[lang])
    return f"""<!doctype html>
<html lang="{lang}">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} — Yaman Evkaya</title>
    <meta name="description" content="{title} · yevkaya.com" />
    <link rel="canonical" href="{BASE}/{me}" />
{alts}    <meta property="og:locale" content="{LOCALE[lang]}" />
    <link rel="icon" href="{up}assets/images/favicon.svg" type="image/svg+xml" />
    <link rel="icon" href="{up}assets/images/favicon-32.png" sizes="32x32" />
    <link rel="stylesheet" href="{up}styles.css?v=20261111-1" />
    <style>{STYLE}    </style>
  </head>
  <body class="legal">
    <a class="skip-link" href="#main">{ui["skip"]}</a>
    <header class="lg-header">
      <a class="wordmark" href="{home}" aria-label="Yaman Evkaya">
        <span class="wordmark-mark" aria-hidden="true">YE</span>
        <span class="wordmark-text">Yaman Evkaya</span>
      </a>
      <div class="lg-tools">
        <a class="lg-back" href="{home}">← {ui["back"]}</a>
        <div class="lang-switch" aria-label="{ui["lang"]}">{switch}</div>
      </div>
    </header>
    <main class="lg-main" id="main">
      <p class="lg-kicker">{ui["kicker"]}</p>
      <h1>{title}</h1>
      {note}
      <div class="lg-body">{body}</div>
      <p class="lg-stand">{ui["stand"]}: {STAND[lang]}</p>
    </main>
    <footer class="lg-footer">
      <span>yevkaya.com · Yaman Evkaya</span>
      <nav aria-label="{ui["kicker"]}">{foot_links}</nav>
    </footer>
  </body>
</html>
"""


if __name__ == "__main__":
    for kind in PATHS:
        for lang in ("en", "de", "tr"):
            out = os.path.join(SITE, PATHS[kind][lang])
            os.makedirs(os.path.dirname(out), exist_ok=True)
            html = page(kind, lang)
            leftover = re.findall(r"\[\[[^\]]+\]\]", html)
            assert not leftover, (PATHS[kind][lang], leftover)
            open(out, "w", encoding="utf-8").write(html)
            print("written", PATHS[kind][lang])
