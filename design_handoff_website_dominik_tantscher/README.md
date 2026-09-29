# Handoff: Website Dominik Tantscher (KI-Beratung)

## Überblick
Mehrseitige Website für ein neu gegründetes KI-Beratungsunternehmen (Einzelunternehmen Dominik Tantscher, 8121 Deutschfeistritz, AT). Zielgruppe: Klein- und Kleinstbetriebe. Hauptziel: Besucher zum Online-Fragebogen (Tally) oder zur Kontaktaufnahme führen.
Domain: https://dominik-tantscher.at · Hosting: World4You (Linz, Server in Österreich) · Umsetzung: Claude Code.

## Über die Design-Dateien
Die Dateien in `design/` sind **Design-Referenzen in HTML**: Sie zeigen Aussehen, Inhalte und Verhalten. Es ist kein Produktionscode zum Kopieren. Aufgabe ist, das Design als echte Website nachzubauen (Empfehlung unten).
`design/Website Dominik Tantscher.dc.html` im Browser öffnen: Das ist eine Canvas mit allen Seiten als Artboards 2a–2j. `support.js`, `DT Header.dc.html` und `DT Footer.dc.html` müssen im selben Ordner liegen. Alle Texte stehen dort 1:1, die Datenlisten im `<script>`-Block am Ende der Datei.

## Fidelity
**High-fidelity.** Farben, Typografie, Abstände, Zustände und Texte sind final und pixelgenau umzusetzen. Ausnahme: Datenschutz-Abschnitt 04 ist ein Textentwurf (siehe unten).

## Verbindliche Regeln für die Umsetzung
1. **Texte nicht verändern.** Quelle der Wahrheit sind die Dateien in `sources/` und die Design-Datei. Keine Umformulierungen, keine zusätzlichen Inhalte.
2. **Keine externen Requests beim Seitenaufruf**: keine Google Fonts, keine CDNs, kein Analytics, keine Tracking-Pixel, keine eingebetteten Dienste. Tally wird nur **verlinkt** (neuer Tab), nicht eingebettet. Grund: Die Datenschutzerklärung schließt das aus.
3. **Keine Cookies** außer technisch notwendigen (am besten gar keine). Kein Cookie-Banner.
4. Kontaktformular: **keine Datenbank, kein externer Formulardienst, kein reCAPTCHA**.
5. Keine Farbe außerhalb der Token-Liste. Radius überall 0, keine Schatten, keine Verläufe.

## Empfohlener Tech-Stack
- **Astro** (statischer Build, `output: 'static'`) mit **Vanilla CSS**. CSS Custom Properties aus den Tokens unten, ein globales Stylesheet plus komponentenweise Styles. Kein Tailwind nötig.
- JavaScript nur für: Mobilmenü (Toggle, Fokusfalle, ESC) und Formularvalidierung/-versand (progressive enhancement: Das Formular funktioniert auch ohne JS per normalem POST).
- **Formular-Backend: `public/kontakt.php`** (World4You unterstützt PHP). Ablauf: POST annehmen, Honeypot-Feld (`website`, versteckt) prüfen, Mindestzeit prüfen (Zeitstempel-Feld, < 3 s = Spam), serverseitig validieren, E-Mail an ki@dominik-tantscher.at senden (PHPMailer über SMTP, Zugangsdaten per Umgebungsvariable/Config außerhalb des Webroots; alternativ `mail()`), Reply-To = Absender-E-Mail. Antwort: JSON für den JS-Weg, Redirect auf `/kontakt?status=ok|fehler` für den No-JS-Weg. Nichts speichern, nichts loggen außer Standard-Serverlogs.
- Schriften: Archivo (400/600/700) und Space Mono (400/700) als WOFF2 selbst hosten (`public/fonts/`), Lizenz SIL OFL. Z. B. über das npm-Paket `@fontsource/archivo` und `@fontsource/space-mono`. Diese bündeln die Dateien lokal, ohne CDN. Preload für Archivo 700 und 400.
- Deployment: `astro build` → Inhalt von `dist/` + `kontakt.php` per SFTP zu World4You. HTTPS erzwingen, www → ohne www per `.htaccess`.
- Seitenstruktur: `/`, `/leistungen`, `/preise`, `/ueber-mich`, `/kontakt`, `/impressum`, `/datenschutz`, `404`. Die 404-Seite hat kein Design: Header + Footer, H1 „Seite nicht gefunden“ + Primärbutton zur Startseite, Text vorher mit dem Kunden abstimmen.
- Komponenten: `Header`, `MobileMenu`, `Footer`, `SectionLabel`, `Button` (primary/secondary), `CtaBox` (Fragebogen, kommt auf Start, Leistungen, Preise, Über mich vor), `CheckList`, `ServiceGrid`, `ServiceRows`, `ProcessSteps`, `BenefitBlock`, `PriceTable`, `ValueTable`, `ContactForm`, `LegalSection`. Inhalte als Daten (`src/content/*.json` oder Frontmatter), nicht in Komponenten hart codiert.
- Qualität: Lighthouse ≥ 95 in allen Kategorien, valides HTML, Tastatur voll bedienbar, sichtbarer Fokus (`:focus-visible`, 2 px `#849DFF`, Offset 3 px).

## Interaktionen und Zustände
- Navigation: aktive Seite `aria-current="page"` → Farbe `#F0F2F5` + 2 px Unterstrich `#69D98D` (Padding 6 px 0). Header `position: sticky; top: 0; z-index: 10`.
- Unter 1024 px: Navigation und Header-Button ausblenden, Menü-Button (44 × 44, drei Striche 24/24/16 px, 2 px, der letzte `#69D98D`, Abstand 6 px). Das Menü öffnet als Vollbild-Overlay (Artboard 2i), `body` scrollt dann nicht.
- Hover-Transitions: `color, background-color, border-color 150ms ease`. Mit `prefers-reduced-motion: reduce` keine Transitions.
- Formular: Validierung beim `blur` und beim Absenden. Button während des Sendens deaktiviert, Text bleibt. Erfolg: Formular ersetzen durch Erfolgsbox (`role="status"`, Fokus auf die Box). Fehler: Fehlerbox über dem Button (`role="alert"`), Eingaben bleiben erhalten.
- Externe Links (Tally): `target="_blank" rel="noopener"`.

---

# Designdokumentation

Stand: 26.09.2026 · Designdatei: `Website Dominik Tantscher.dc.html` (Artboards 2a–2j) · Basis: CI-Manual V1.0 (09/2026), Richtung 1a „Raster“ (freigegeben)

Quellen (Texte 1:1 übernommen, nicht verändert):
- `uploads/Onepager_Dominik_Tantscher_0926.pdf` → Startseite
- `uploads/Leistungen_und_Preise_0926.pdf` → Preise
- Über-mich-Text aus dem Chat → Über mich
- `uploads/Impressum.docx` → Impressum
- `uploads/Datenschutzerklaerung.pdf` → Datenschutz

Vom Kunden freigegebene Textänderungen:
- Anfahrt „ab 8181 Deutschfeistritz“ → **8121**
- Über mich, letzter Satz: Punkt ergänzt
- Datenschutz: neuer Abschnitt **04 Kontaktformular** (Entwurf, siehe 6), bisherige Abschnitte 04–08 → 05–09

Domain: **dominik-tantscher.at** (bestätigt).
Claim-Schreibweise laut Kunde mit Gedankenstrich: „KI – maßgeschneidert auf Ihre Bedürfnisse.“

---

## 1 Grundentscheidungen

| Entscheidung | Festlegung | Begründung |
|---|---|---|
| Richtung | 1a „Raster“, durchgehend dunkel | Kundenwahl |
| Porträtfoto | **Kein Foto** auf der gesamten Website | Kundenwunsch („möchte ich nicht“) |
| Struktur | Mehrseitig: Start, Leistungen, Preise, Über mich, Kontakt + Impressum, Datenschutz | Kundenwahl |
| Primäre Handlung | „FRAGEBOGEN AUSFÜLLEN →“ → `https://tally.so/r/5BRD2d` (neuer Tab) | Onepager-CTA, Link vom Kunden |
| Kontaktwege | Telefon (tel-Link), E-Mail (mailto-Link), Kontaktformular | Kundenwahl |
| Nicht umgesetzt | Online-Terminbuchung, LinkedIn, WhatsApp | Kunde: vorerst weglassen |
| Tracking | Keines. Nur technisch notwendige Cookies | Datenschutzerklärung Abschnitt 05 |
| Schriften | **Selbst hosten** (kein Google-Fonts-CDN) | Google Fonts wird in der Datenschutzerklärung nicht genannt; Abruf vom Google-CDN würde IP-Adressen übertragen |
| Hosting | World4You, Server in Österreich | Datenschutzerklärung Abschnitt 02 |

---

## 2 Farben (CI 04 – ausschließlich diese Werte)

| Token | Hex | Einsatz auf der Website |
|---|---|---|
| `bg` | `#0A0C11` | Seitenhintergrund, Header, Footer, Button-Text auf Grün |
| `surface` | `#15171E` | Karten, CTA-Box, Pilotpreis-Spalte, Formularfelder, feines Hintergrundraster im Hero |
| `border` | `#2D3038` | Alle Trennlinien (1 px), Kartenrahmen, Sekundär-Button-Rahmen |
| `accent` | `#69D98D` | Primärbutton, Section-Labels, Häkchen, „10 Std.“, Akzentwörter in H1, aktive Navigation (Unterstrich), Pilotpreise |
| `state` | `#849DFF` | **Nur Zustände**: Fokusrahmen (Tastatur + Formularfeld), KI-Schritt im Ablaufdiagramm („2 · IHRE KI“), Offen-Markierungen im Design |
| `text` | `#F0F2F5` | Überschriften, Fließtext hervorgehoben, Hover-Hintergrund Primärbutton |
| `accent-light` | `#22864A` | Auf dieser dunklen Website nicht verwendet (nur für helle Flächen) |
| `text-2` | `#A2A4AC` | Fließtext, Beschreibungen, Nav default, Tabellenlabels |
| `error` (CI-Ergänzung) | `#FF7B7B` | **Nur** Formularfehler: Feldrahmen, Fehlermeldung, Sendefehler-Box. Immer mit „!“-Symbol und Text, nie Farbe allein |

Begründung Fehlerfarbe: Das CI enthält keine Fehlerfarbe. Empfehlung: ein helles Korallrot mit ähnlicher Helligkeit wie das Primärgrün, damit es auf `#0A0C11` gleich stark wirkt und sich trotzdem klar vom Grün unterscheidet. Kontrast auf `#0A0C11` ≈ 7,6:1.

Kontraste (auf `#0A0C11`): `#F0F2F5` ≈ 17,6:1 · `#A2A4AC` ≈ 7,9:1 · `#69D98D` ≈ 11,4:1 · `#849DFF` ≈ 7,6:1. `#0A0C11` auf `#69D98D` ≈ 11,4:1. Alle erfüllen WCAG AA.

Nicht verwenden: Verläufe, Transparenzen auf Text, zusätzliche Farben.

---

## 3 Typografie (CI 05)

Schriften: **Archivo** 400 / 600 / 700 · **Space Mono** 400 / 700. Lokal als WOFF2 einbinden, `font-display: swap`. Fallback: `Archivo, system-ui, sans-serif` / `"Space Mono", ui-monospace, monospace`.

| Token | Schrift | Desktop (px) | Mobil (px) | Zeilenhöhe | Laufweite | Einsatz |
|---|---|---|---|---|---|---|
| `display` | Archivo 700 | 160 („10“) + 48 („Std.“) | 112 + 36 | 0.9 | -0.04em | Kennzahl „10 Std.“ |
| `h1` | Archivo 700 | 76 | 42 | 1.02 / 1.05 | -0.02em | Seitentitel Start, Preise, Über mich, Kontakt |
| `h1-legal` | Archivo 700 | 56 | 36 | 1.05 | -0.02em | Impressum, Datenschutz |
| `h2-cta` | Archivo 700 | 44 | 28 | 1.1 | 0 | „Welcher Ablauf kostet Sie am meisten Zeit?“ |
| `h2` | Archivo 700 | 40 | 28 | 1.12 / 1.15 | 0 | Section-Überschriften |
| `h3` | Archivo 700 | 24–32 | 20–24 | 1.15–1.2 | 0 | Leistungs-/Pakettitel, Tabellenüberschriften, Datenschutz-Abschnitte (28) |
| `quote` | Archivo 400, Anfang 700 grün | 28 | 21 | 1.4 | 0 | „Maßgeschneidert statt von der Stange …“, Über-mich-Einstieg |
| `lead` | Archivo 400 | 20 | 17 | 1.55 | 0 | Einleitungstext unter H1 |
| `body` | Archivo 400 | 18 (Standard), 16 (Karten) | 17 / 16 | 1.6 / 1.55 | 0 | Fließtext |
| `small` | Archivo 400 | 15 / 14 | 15 / 14 | 1.55 | 0 | Rechenbeispiel, Preis-Fußnote |
| `label` | Space Mono 400 | 13 | 12 | 1.6 | 0.2em, VERSAL | Section-Labels „01 — WARUM ICH“, Tags |
| `label-s` | Space Mono 400 | 12 | 12 | – | 0.18em, VERSAL | Karten-Labels, Formularlabels, Preis-Labels |
| `button` | Space Mono 700 | 14 (Header: 13) | 14 | – | 0.12em, VERSAL | Buttons |
| `nav` | Space Mono 400 | 13 | Mobilmenü: Archivo 700, 30 | – | 0.12em | Navigation |

Regeln: `text-wrap: pretty` für Fließtext; Versalien per CSS (`text-transform: uppercase`) nur bei Labels, deren Quelltext in Versalien steht. Sonst den Quelltext unverändert lassen.

---

## 4 Raster, Abstände, Breakpoints

| | Desktop ≥ 1280 | Tablet 768–1279 | Mobil < 768 |
|---|---|---|---|
| Max. Inhaltsbreite | 1152 px (1280 − 2 × 64) | fluid | fluid |
| Seitenrand | 64 px | 40 px | 20 px |
| Spalten / Gutter | 12 / 24 px | 8 / 24 px | 4 / 16 px |
| Section-Padding vertikal | 96 px | 80 px | 56 px |
| Header-Höhe | 80 px | 72 px | 64 px |

Über 1280 px: Inhalt zentriert, max-width 1280 px, Hintergrund `#0A0C11` vollflächig.
Tablet wurde nicht gezeichnet. Regel: Layouts der Desktop-Version, 4-Spalter werden 2-Spalter, 2-Spalter bleiben; ab < 1024 px Mobilnavigation.

Abstandsskala (px): 4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64 · 96.
Radien: **0** überall (eckig, wie Raster/Signet). Schatten: keine.

Wiederkehrendes Section-Muster (Desktop): Label in Spalte 1–3, Inhalt in Spalte 4–12. Sections sind durch 1 px `#2D3038` getrennt.
Hero Start: dezentes vertikales Spaltenraster als Hintergrund (1 px Linien `#15171E`, eine pro Spalte), rein dekorativ.

---

## 5 Komponenten (siehe Artboard 2j)

**Button primär**: bg `#69D98D`, Text `#0A0C11`, Space Mono 700 14 px, +0.12em, Padding 18 × 24 (groß 20 × 28, Header 12 × 18). Hover: bg `#F0F2F5`. Fokus: `outline: 2px solid #849DFF; outline-offset: 3px`. Transition 150 ms ease.
**Button sekundär**: transparent, Rahmen 1 px `#2D3038`, Text `#F0F2F5`, Padding 17 × 24. Hover: Rahmen + Text `#69D98D`.
**Textlink**: `#69D98D`, Hover `#F0F2F5`. Footer-/Kontaktlinks: `#F0F2F5`, Hover `#69D98D`.
**Navigation**: default `#A2A4AC`; Hover `#F0F2F5`; aktiv `#F0F2F5` + 2 px Unterstrich `#69D98D`. Impressum/Datenschutz: kein Punkt aktiv.
**Karte**: bg `#15171E`, Rahmen 1 px `#2D3038`, Padding 24–64.
**Häkchen-Liste**: 20 × 20 Quadrat, 2 px Rahmen `#69D98D`, „✓“ 13 px 700 grün.
**Ablaufdiagramm** (Beispiel Anfrage → Angebot): 3 Karten + Pfeil „→“ (mobil „↓“); KI-Schritt mit Rahmen und Label in `#849DFF`, Sie-Schritte in `#69D98D`.
**Preistabelle**: Spalten 72 px · flexibel · 208 · 208. Pilotpreis-Spalte bg `#15171E`, Kopf mit 2 px Oberkante `#69D98D`, Preise 36 px 700 grün; Präfix „ab“ 18 px 600.
**Wertetabelle** (Was darüber hinausgeht / Anfahrt): Zeilen mit 1 px Trennlinie, Wert rechtsbündig in Space Mono 700.
**Formularfeld**: Höhe 56, bg `#15171E`, Rahmen 1 px `#2D3038`, Text 17 px `#F0F2F5`, Label Space Mono 12 px über dem Feld. Fokus: Rahmen `#849DFF` + 1 px Ring. Fehler: Rahmen `#FF7B7B` + 1 px Ring, darunter Meldung 14 px `#FF7B7B` mit „!“-Kreis 16 px. Validierung beim Verlassen des Felds und beim Absenden, Fokus springt aufs erste fehlerhafte Feld, `aria-invalid` + `aria-describedby`.
**Formular-Rückmeldung**: ersetzt nach dem Absenden das Formular (Erfolg: Rahmen `#69D98D`, ✓-Quadrat) bzw. steht über dem Button (Fehler: Rahmen `#FF7B7B`). `role="status"` bzw. `role="alert"`.
**Header**: Lockup `dt-lockup.svg` 36 px hoch · Navigation mittig · Primärbutton rechts. Sticky beim Scrollen.
**Footer**: E-Mail, Telefon links; Impressum, Datenschutz, „DOMINIK TANTSCHER“ rechts; Space Mono 13 px.
**Mobilmenü** (2i): Vollbild-Overlay `#0A0C11`, Einträge Archivo 700 30 px mit Nummer rechts, Trennlinien, unten Primärbutton + Telefon/E-Mail. Button 44 × 44, `aria-expanded`, Fokus bleibt im Overlay, ESC schließt.

Mindest-Klickfläche mobil: 44 × 44 px.

---

## 6 Seiten und Inhalte

**2a Start** (Onepager, vollständig und in Reihenfolge): Hero (Label, H1 mit zweiter Zeile grün, Lead, Primär- + Sekundärbutton „LEISTUNGEN UND PREISE“ → Preise) · 01 Warum ich + „Mein Ziel“-Karte · 02 Kommt Ihnen das bekannt vor? (6 Punkte, 2-spaltig) · 03 Leistungen (4 Spalten) + Ablaufbeispiel · 04 Ihr Nutzen (Kennzahl links, 4 Vorteile rechts) · Maßgeschneidert-Absatz · CTA-Box.
**2b Leistungen** (Kunde: Inhalte aus dem Onepager): Hero (Label „LEISTUNGEN · ALLES AUS EINER HAND“, H1 „Leistungen“) · 4 Leistungen als Zeilen (Nummer 64 px `#2D3038` · Titel H2 36 px + Tag · Text 19 px) · Ablaufbeispiel · Ihr Nutzen · CTA-Box mit Primärbutton und Sekundärbutton „LEISTUNGEN UND PREISE“ → Preise.
**2c Preise** (Preisliste vollständig): Hero · Leistungspakete-Tabelle · Was darüber hinausgeht / Anfahrt (2-spaltig) · Pilotpreise (Box mit 1 px grünem Rahmen) · CTA-Box · Preis-Fußnote.
**2d Über mich**: H1, erster Absatz als Einstieg (28 px), Absätze 2–4 in Spalte 4–10, „Was ich nicht mache:“ fett hell, letzter Absatz als hervorgehobene Karte · CTA-Box.
**2e Kontakt**: H1 · Formular (Spalte 1–7) · rechts (Spalte 9–12): E-Mail, Telefon, Fragebogen-Box.

Kontaktformular (Empfehlung, vom Kunden delegiert):

| Feld | Typ | Pflicht | autocomplete | Fehlermeldung |
|---|---|---|---|---|
| NAME * | text | ja | name | Bitte geben Sie Ihren Namen an. |
| BETRIEB / FIRMA | text | nein | organization | – |
| E-MAIL * | email | ja | email | Bitte geben Sie eine gültige E-Mail-Adresse an. |
| TELEFON | tel | nein | tel | – |
| NACHRICHT * | textarea, 7 Zeilen | ja | – | Bitte schreiben Sie kurz, worum es geht. |

- Hinweis neben dem Button: „* Pflichtfeld. Ihre Angaben verwende ich nur zur Bearbeitung Ihrer Anfrage. Details in der Datenschutzerklärung.“ (Link)
- **Keine Einwilligungs-Checkbox**: Rechtsgrundlage ist Art. 6 Abs. 1 lit. b/f DSGVO (wie bei E-Mail), nicht Einwilligung. Eine Checkbox würde eine Einwilligung als Grundlage nahelegen.
- Button: „NACHRICHT SENDEN →“
- Erfolg: „Danke, Ihre Nachricht ist angekommen.“ / „Ich melde mich persönlich bei Ihnen.“
- Sendefehler: „Die Nachricht konnte nicht gesendet werden. Bitte versuchen Sie es erneut oder schreiben Sie direkt an ki@dominik-tantscher.at.“
- Technik (muss zur Datenschutzerklärung 04 passen): Versand serverseitig per E-Mail an ki@dominik-tantscher.at, **keine Datenbank-Speicherung**, kein externer Formulardienst, Spamschutz per Honeypot-Feld + Zeitprüfung (kein reCAPTCHA, da nicht in der Datenschutzerklärung).
**2f Impressum**: Text laut Docx, Tabelle Label/Wert.
**2g Datenschutz**: Text laut PDF, Abschnitte 01–09 mit Zweck/Rechtsgrundlage/Speicherdauer als Tabelle. Abschnitt **04 Kontaktformular ist neu und von mir formuliert** (nach Muster von Abschnitt 03). Im Design mit „NEU · ENTWURF“ markiert. Vor Veröffentlichung rechtlich prüfen lassen, dann Markierung entfernen und „Stand“-Datum aktualisieren.
**2h/2i**: Mobilversion Start und Mobilmenü. Unterseiten mobil nach denselben Regeln (einspaltig, Tabellen → gestapelte Zeilen: Titel, Text, dann Pilot/Regulär nebeneinander).

Technisches:
- Sprache `lang="de-AT"`. Telefon-Link `tel:+436645077100`.
- Tally-Links mit `target="_blank" rel="noopener"`.
- SEO-Texte: siehe Abschnitt 8.
- Favicon/App-Icon: Signet (CI 02 „App-Icon · klein“), Quelldatei fehlt als Vektor.
- Semantik: je Seite genau eine H1; Section-Labels sind keine Überschriften (`<p>`), H2 folgt.
- Keine Animationen außer Hover-Transitions (150 ms). `prefers-reduced-motion` respektieren.

---

## 7 Assets

| Datei | Zustand | Hinweis |
|---|---|---|
| `assets/dt-signet.svg` | **verwenden** · Primär auf dunkel | Aus dem CI-PDF extrahiert (Seite 1/2). viewBox 100 × 100, transparent. T: `M0 5L60 5M30 5L30 100`, `#69D98D`. D: `M60 5A35 45 0 0 1 60 95L35 95`, `#F0F2F5`. Beide stroke-width 10 (= 10 % Strich laut CI), butt caps, miter |
| `assets/dt-signet-hell.svg` | Auf hell | T `#22864A`, D `#0A0C11` (CI 02 „Auf hell“) |
| `assets/dt-lockup.svg` | **verwenden** · Header | Signet + Wortmarke „Dominik Tantscher“ (Glyphen als Pfade aus dem CI-Lockup, Proportionen 1:1). viewBox 177,43 × 33. **Ohne Claim** |
| `assets/dt-lockup-hell.svg` | Auf hell | Wie oben, Farben „auf hell“ |
| `assets/dt-signet.png`, `dt-lockup.png`, Uploads `logo_dt*.svg` | nicht verwenden | Raster bzw. Pixel-Nachzeichnung mit eingebackenem Hintergrund |

Header: `dt-lockup.svg`, Höhe 36 px (Desktop) / 28 px (mobil), Breite automatisch. Favicon: `dt-signet.svg` (SVG-Favicon) + daraus PNG 32/180/512 auf `#0A0C11` exportieren.
Claim-Variante des Lockups: Im CI-PDF steht der Claim mit Bindestrich. Freigegeben ist der Gedankenstrich, deshalb gibt es keine Lockup-Datei mit Claim. Wo der Claim nötig ist, als Live-Text setzen (Archivo 400, `#A2A4AC`).

---

## 8 SEO und Meta-Daten (vom Kunden beauftragt, von mir formuliert)

Titel max. ~60 Zeichen, Beschreibung max. ~155 Zeichen. Formulierungen aus den gelieferten Texten abgeleitet.

| Seite | URL | `<title>` | `<meta name="description">` |
|---|---|---|---|
| Start | `/` | KI-Einrichtung für Kleinbetriebe · Dominik Tantscher | Ich richte KI persönlich in Ihrem Betrieb ein – passend zu Ihren Abläufen, sicher mit Ihren Daten. Vor Ort in der Steiermark oder online. |
| Leistungen | `/leistungen` | Leistungen: Analyse, Einrichtung, Schulung · Dominik Tantscher | Analyse, Einrichtung von ChatGPT, Claude oder Gemini, eigene Lösungen und Schulungen nach EU AI Act – alles aus einer Hand für kleine Betriebe. |
| Preise | `/preise` | Leistungen und Preise · Dominik Tantscher | Feste Pakete zum Festpreis: Potenzialcheck, Einrichtung, eigene Lösung, Schulung. Pilotpreise für die ersten fünf Betriebe. |
| Über mich | `/ueber-mich` | Über mich · Dominik Tantscher | Seit über fünf Jahren mit KI beschäftigt, beruflich in der Industrie und privat. Ich setze KI dort ein, wo sie im Alltag eines kleinen Betriebs trägt. |
| Kontakt | `/kontakt` | Kontakt · Dominik Tantscher | Schreiben Sie mir, rufen Sie an unter 0664 50 77 100 oder beschreiben Sie Ihren Ablauf im Online-Fragebogen. |
| Impressum | `/impressum` | Impressum · Dominik Tantscher | – (`noindex` nicht nötig, Beschreibung optional) |
| Datenschutz | `/datenschutz` | Datenschutzerklärung · Dominik Tantscher | – |

Hinweis: „Steiermark“ in der Start-Beschreibung leitet sich aus dem Standort Deutschfeistritz ab. Bitte bestätigen oder streichen.

Weitere Meta-Angaben:
- `<html lang="de-AT">`, `<link rel="canonical">` je Seite, `https://dominik-tantscher.at` ohne www (Weiterleitung www → ohne).
- Open Graph: `og:title` = Title, `og:description` = Description, `og:locale` = de_AT, `og:image` = 1200 × 630, Signet + „Dominik Tantscher“ + Claim auf `#0A0C11` (anzulegen, sobald Vektor-Logo vorliegt).
- Strukturierte Daten (JSON-LD) auf der Startseite: `ProfessionalService` mit Name „Dominik Tantscher“, Adresse Am Flurweg 6, 8121 Deutschfeistritz, AT, Telefon +43 664 5077100, E-Mail, URL, `areaServed` Österreich.
- `sitemap.xml` und `robots.txt` (alles erlauben).

## 9 Offene Punkte

1. Logo: erledigt (aus dem CI-PDF extrahiert). OG-Bild 1200 × 630 noch anzulegen.
2. **Datenschutz Abschnitt 04 (Kontaktformular)** rechtlich prüfen lassen.
3. **Umsetzungsplattform** noch offen. Die technischen Vorgaben (Formularversand ohne Datenbank, selbst gehostete Schriften, keine Cookies außer technisch notwendigen) müssen mit der gewählten Plattform erfüllbar sein.
4. SEO: Bestätigung der Formulierung „Steiermark“.


## Dateien in diesem Paket
- `design/Website Dominik Tantscher.dc.html`: alle Seiten (Artboards 2a–2j)
- `design/DT Header.dc.html`, `design/DT Footer.dc.html`, `design/support.js`: werden von der Design-Datei geladen
- `design/assets/`: Logos (SVG), benötigt zur Anzeige der Design-Datei
- `assets/`: Produktions-Assets (Logo-SVGs)
- `sources/`: Originalunterlagen des Kunden (CI-Manual, Onepager, Preisliste, Impressum, Datenschutzerklärung, Über-mich-Text). Bei Abweichungen gelten diese Dateien, ausgenommen die oben unter „Vom Kunden freigegebene Textänderungen“ genannten Punkte.
