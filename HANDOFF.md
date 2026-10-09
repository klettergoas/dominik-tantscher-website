# HANDOFF – Umbau „zwei Angebotslinien“

Stand: 2026-10-09 · Branch: `feature/zwei-angebotslinien` · Basis: `main` (9d5ee88) · Ausführung: Claude Code
Auftrag: WEBSITE_BRIEFING.md (2026-10-07), präzisiert durch Dominik am 2026-10-07 und 2026-10-09.
Nicht gemergt, nicht deployt – Merge macht Dominik nach dem Review.

## Entscheidungen Dominik

- **Unterscheidung nach Leistung, nicht nach Unternehmensgröße.** Die zwei Bereiche heißen überall **KI-Implementierung** und **KI-Beratung**.
- **Eine Leistungsübersicht:** `/leistungen` mit Umschalter zwischen beiden Bereichen. Die Preise stehen dort, es gibt keine eigene Preisseite und keinen Menüpunkt „Preise“ mehr.
- **Schulung** steht in beiden Bereichen mit unverändertem Umfang; bei KI-Beratung zusätzlich der Hinweis auf weiterführende Enablement-Formate nach Absprache.
- **Startseite:** „Zwei Wege“ bleibt, die vier alten Leistungsspalten entfallen.
- Unverändert bleiben: Fragebogen (Tally), Seite „Referenzen“, „Über mich“, die bestehenden Formularfelder. Anfahrt ab **8121**.

## Stand der Seiten

| Seite | Inhalt |
| --- | --- |
| `/` | Hero, „Zwei Wege“ (KI-Implementierung / KI-Beratung), 01 Warum ich, 02 Haken-Liste, Ablaufbeispiel, 03 Ihr Nutzen, Maßgeschneidert, „Was mich unterscheidet“, Praxis-Teaser, Abschluss-CTA, Fragebogen-Box |
| `/leistungen` | Umschalter. **KI-Implementierung:** vier Leistungen, Ablaufbeispiel, Ihr Nutzen, Preistabelle, Was darüber hinausgeht, Anfahrt, Wartungspauschale, Pilotpreise, Fußnote. **KI-Beratung:** Anzeichen, Standortbestimmung, Governance-Sprint, Schulung und Enablement, Projektablauf, Preis-Hinweis, Abgrenzung zur Rechtsberatung. |
| `/praxisbeispiele` | Vier Beispielszenarien, Tags „KI-Implementierung“ / „KI-Beratung“ |
| `/kontakt` | Zusätzlich Pflichtauswahl „Anliegen“ (KI-Implementierung, KI-Beratung, Schulung, Etwas anderes), Vorbelegung über `?anliegen=prozess|organisation|schulung|sonstiges` |
| `/referenzen`, `/ueber-mich`, `/impressum`, `/datenschutz` | unverändert |

**Menü:** Start, Leistungen, Praxisbeispiele, Referenzen, Über mich, Kontakt – ab 1140 px in der Kopfzeile, darunter Menü-Symbol.
**Umschalter:** Adresse merkt den Bereich (`/leistungen#ki-implementierung`, `/leistungen#ki-beratung`). Ohne JavaScript sind beide Bereiche untereinander sichtbar.
**Weiterleitung:** `/preise` → `/leistungen#ki-implementierung` (301, `.htaccess`).
**Preise an einer Stelle:** `website/src/content/preise.json`.

## Von Claude formuliert oder geändert – bitte prüfen

Startseite (bisher freigegebene Texte, wegen „nicht nach Unternehmensgröße“ angepasst):

| Stelle | vorher | jetzt |
| --- | --- | --- |
| Seitentitel | KI-Einrichtung für Kleinbetriebe · Dominik Tantscher | KI-Implementierung und KI-Beratung · Dominik Tantscher |
| Meta-Beschreibung | Ich richte KI persönlich in Ihrem Betrieb ein – passend zu Ihren Abläufen, sicher mit Ihren Daten. Vor Ort oder online. | Ich bringe KI wirksam in den Arbeitsalltag: von der konkreten Prozesslösung bis zu Standortbestimmung, Governance und Schulung. Vor Ort oder online. |
| Label im Hero | KI-EINRICHTUNG FÜR KLEINBETRIEBE | KI-IMPLEMENTIERUNG UND KI-BERATUNG |
| 01 Überschrift | KI ist da. Nur in kleinen Betrieben arbeitet sie noch nicht. | KI ist da. Nur im Arbeitsalltag arbeitet sie oft noch nicht. |
| 01 Text | Konzerne nutzen KI längst im Alltag, Kleinbetrieben fehlt dafür die Zeit. Beratungen sind auf Großunternehmen zugeschnitten, der Selbstversuch endet oft in einem Chatfenster. … | Werkzeuge gibt es genug, im Alltag fehlt die Zeit, sie einzurichten. Viele Beratungen bleiben beim Konzept, der Selbstversuch endet oft in einem Chatfenster. … |
| Maßgeschneidert | … und mache dieses Wissen für kleine Betriebe nutzbar. | … und mache dieses Wissen für Ihren Betrieb nutzbar. |
| Zwei Wege, Einleitung | Von der konkreten Prozesslösung im kleinen Betrieb bis zu Strategie, Governance und Befähigung in Organisationen. | Von der konkreten Prozesslösung bis zu Strategie, Governance und Befähigung. |
| Zwei Wege, Unterzeilen | Für kleine Unternehmen, Handwerk und Freiberufler / Für Organisationen, in denen KI genutzt wird oder werden soll | KI-Implementierung / KI-Beratung |
| Label Nutzen | 04 — IHR NUTZEN | 03 — IHR NUTZEN |

Leistungen:

- Einleitung KI-Implementierung: „Wenn die Büroarbeit neben der eigentlichen Arbeit zu viel Zeit frisst: Ich löse einen konkreten Arbeitsprozess und bringe die Lösung tatsächlich in den Betrieb.“ (Briefing nannte Handwerker, Freiberufler und kleine Unternehmen)
- Meta-Beschreibung: „KI-Implementierung mit festen Paketen und Preisen sowie KI-Beratung mit Standortbestimmung, Governance und Schulung – alles aus einer Hand.“
- Hinweis bei Schulung (KI-Beratung): „Weiterführende und umfassendere Enablement-Formate sind nach Absprache möglich, zum Beispiel:“ – darunter die fünf Formate aus dem Briefing.
- Preis-Hinweis: „Für Standortbestimmung und Governance-Sprint gibt es keine Paketpreise, weil sich Vorhaben stark unterscheiden. Nach einer kurzen Abgrenzung erhalten Sie ein projektbezogenes Angebot.“
- Wartungspauschale in Ich-Form (`preise.json` → `maintenance.bullets`).

Kontakt: Feldname „ANLIEGEN *“, Platzhalter „Bitte wählen“, Fehlermeldung „Bitte wählen Sie ein Anliegen aus.“
Praxisbeispiele: Meta-Beschreibung aus den ersten zwei Sätzen des Intros.

## Abweichungen vom Briefing

- Keine eigenen Seiten `/ki-umsetzung`, `/ki-strategie-governance`, `/schulung-enablement`; ihre Inhalte stehen auf `/leistungen` (Entscheidung Dominik).
- **Im Bereich KI-Beratung stehen Preise**, nämlich die des Pakets „Schulung und Begleitung“ (Entscheidung Dominik: Schulung in beiden Bereichen, Umfang unverändert). Das Briefing verlangte dort keine Preise.
- H1 der Startseite und von Kontakt bleiben; die Briefing-Überschriften stehen als Zwischenüberschriften.
- Paket-Texte sind die bestehenden Website-Texte in Ich-Form, nicht der gekürzte Wortlaut aus ANGEBOT.md. Preise stimmen mit ANGEBOT.md überein.
- Buttons per CSS in Versalien (CI).

## Geprüft

- Build ohne Fehler, keine kaputten internen Links (inkl. Anker).
- Lighthouse (mobil) 100 in allen Kategorien auf Start, Leistungen, Praxisbeispiele, Kontakt.
- Kein seitliches Überlaufen bei 320 / 375 / 768 / 1024 / 1280 px.
- Umschalter: Klick, Direktlink mit `#ki-beratung`, Links von der Startseite.
- Kontaktformular: Vorbelegung; `kontakt.php` am 2026-10-07 lokal mit Testdaten gegen einen Test-Mailserver geprüft. Seither wurden nur die zwei Bezeichnungen in der E-Mail geändert.
- **Nicht geprüft:** die 301-Weiterleitung von `/preise` (greift erst auf dem Apache-Server).

## Offene Punkte

1. **Größenbezug bleibt an drei Stellen:** „Über mich“ („was in einem kleinen Betrieb trägt“, auch in der Meta-Beschreibung – Seite sollte unverändert bleiben), die Titel der Praxisbeispiele (Handwerksbetrieb, Freiberuflerin, Mittelständisches Unternehmen, Organisation – Szenariobeschreibungen aus dem Briefing) und der Unternehmensgegenstand im Impressum.
2. **Seitentitel Leistungen** lautet weiter „Leistungen: Analyse, Einrichtung, Schulung · Dominik Tantscher“ und nennt die KI-Beratung nicht.
3. **Datenschutzerklärung §04** nennt die Formularfelder ohne „Anliegen“. Nicht geändert – bei der rechtlichen Prüfung ergänzen lassen.
4. **Impressum, Unternehmensgegenstand** nennt nur „Klein- und Kleinstunternehmen“. Nicht geändert.
5. **Nach dem Merge deployen:** `npm run deploy` in `website/`. Formular und `kontakt.php` müssen gemeinsam live gehen (neues Pflichtfeld). Danach Live-Test: Testnachricht senden und `/preise` aufrufen.
6. **Kontextdateien:** CODE.md, ROLES.md und der DECISIONS-Eintrag vom 2026-10-07 lagen nicht vor; im Repo gibt es weder AGENTS.md noch CLAUDE.md.
