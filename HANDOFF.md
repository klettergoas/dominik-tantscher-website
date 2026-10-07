# HANDOFF – Umbau „zwei Angebotslinien“

Stand: 2026-10-07 · Branch: `feature/zwei-angebotslinien` · Basis: `main` (9d5ee88) · Ausführung: Claude Code
Auftrag: WEBSITE_BRIEFING.md (2026-10-07). Nicht gemergt, nicht deployt – Merge macht Dominik nach dem Review.

## Grundsatz (Entscheidung Dominik, 2026-10-07)

Alles aus dem Briefing kommt **zusätzlich**. Bestehende Seiten, Abschnitte, Texte, der Fragebogen (Tally) und die Seite „Referenzen“ bleiben unverändert.

## Umgesetzt

| Briefing | Umsetzung |
| --- | --- |
| 4.1 Startseite | Zusätzliche Abschnitte: „Zwei Wege“ (direkt nach dem Hero), „Was mich unterscheidet“, Praxis-Teaser (je Linie das erste Beispiel), Abschluss-CTA. Bestehender Hero, Titel und Meta bleiben. |
| 4.2 KI-Umsetzung | Neue Seite `/ki-umsetzung`: vier Paket-Karten, Pilotpreise, Wartung und Weiterentwicklung, Gut zu wissen, Anfahrt. |
| 4.3 KI-Strategie & Governance | Neue Seite `/ki-strategie-governance`, ohne Preise, mit Abgrenzungshinweis zur Rechtsberatung. |
| 4.4 Schulung & Enablement | Neue Seite `/schulung-enablement` mit `#kleine-teams` (Preise) und `#organisationen` (ohne Preise). |
| 4.5 Praxisbeispiele | Neue Seite `/praxisbeispiele`, vier Beispielszenarien als Datenliste (`src/content/praxisbeispiele.json`). |
| 4.6 Über mich | Unverändert (Entscheidung Dominik). |
| 4.7 Kontakt | Zusätzlich: Pflichtauswahl „Anliegen“, Vorbelegung über `?anliegen=`, Einleitung „Worum geht es?“, Hinweis zu vertraulichen Unterlagen. Bestehende Felder bleiben. |
| Navigation | Zehn Punkte: Start, KI-Umsetzung, KI-Strategie & Governance, Schulung & Enablement, Leistungen, Preise, Praxisbeispiele, Referenzen, Über mich, Kontakt. |

**Preise an einer Stelle:** `website/src/content/preise.json`. Daraus lesen `/preise`, `/ki-umsetzung` und `/schulung-enablement`. Anfahrt ab **8121** Deutschfeistritz (Entscheidung Dominik; ANGEBOT.md nennt 8181).

## Von Claude formuliert – bitte prüfen

- Wartungspauschale in Ich-Form (`preise.json` → `maintenance.bullets`), aus ANGEBOT.md abgeleitet.
- Kontaktformular: Feldname „ANLIEGEN *“, Platzhalter „Bitte wählen“, Fehlermeldung „Bitte wählen Sie ein Anliegen aus.“
- Meta-Beschreibung Praxisbeispiele: die ersten zwei Sätze des Seiten-Intros.
- Link-Texte „Alle Praxisbeispiele ansehen“ und Abschnittstitel „Praxisbeispiele“ auf der Startseite.
- Reihenfolge der zehn Menüpunkte.

## Abweichungen vom Briefing

- **Menü:** Zehn Punkte passen nicht in die Kopfzeile. Das Menü-Symbol öffnet deshalb in jeder Breite das Overlay; der Fragebogen-Button bleibt in der Kopfzeile sichtbar (ab 900 px). Ohne JavaScript erscheint die Navigation als Linkzeile.
- **Startseite:** H1, Title und Meta aus dem Briefing wurden nicht übernommen, weil der bestehende Hero bleibt. Die Briefing-Überschrift steht als H2 über den zwei Wegen.
- **Kontakt:** H1 bleibt „Kontakt“; „Worum geht es?“ steht als H2 über dem Formular.
- **Paket-Texte:** die bestehenden Website-Texte in Ich-Form, nicht der gekürzte Wortlaut aus ANGEBOT.md. Preise stimmen mit ANGEBOT.md überein.
- **Weiterleitungen:** keine nötig, es hat sich keine URL geändert.
- **Buttons:** per CSS in Versalien (CI), Briefing-Texte sind gemischt geschrieben.

## Geprüft

- Build ohne Fehler, keine kaputten internen Links (inkl. Anker).
- Kein „€“ auf `/ki-strategie-governance` und im Abschnitt `#organisationen`.
- Lighthouse (mobil) 100 in allen Kategorien auf Start, KI-Umsetzung, KI-Strategie & Governance, Schulung & Enablement, Praxisbeispiele und Kontakt.
- Kein seitliches Überlaufen bei 320 / 375 / 768 / 1024 / 1280 px auf zehn Seiten.
- Kontaktformular: `?anliegen=` belegt vor; `kontakt.php` lokal mit Testdaten gegen einen Test-Mailserver geprüft (fehlendes und ungültiges Anliegen → Fehler, gültig → E-Mail mit Zeile „Anliegen“).
- Wir-Form: Treffer nur in Kundenzitat („Wir müssen KI …“) und im gemeinsamen Wir mit dem Kunden („Wir klären Ziel …“, „Die besprechen wir …“, „Wir gehen Ihren Büroalltag durch“).

## Offene Punkte

1. **Datenschutzerklärung §04** nennt die Formularfelder ohne „Anliegen“. Nicht geändert (Briefing Regel 6) – bitte bei der anstehenden rechtlichen Prüfung ergänzen lassen.
2. **Impressum, Unternehmensgegenstand** nennt nur „Klein- und Kleinstunternehmen“; Linie 2 richtet sich an Organisationen. Nicht geändert.
3. **Menü am Desktop** nur über das Menü-Symbol – Alternative wäre eine gruppierte Navigation (z. B. „Leistungen“ mit Unterpunkten). Entscheidung offen.
4. **Dopplungen:** `/leistungen` und `/preise` überschneiden sich inhaltlich mit `/ki-umsetzung`; die Startseite hat jetzt zwei Leistungsübersichten und zwei Abschluss-Aufrufe (Kontakt und Fragebogen).
5. **Wartungspauschale** steht nur auf `/ki-umsetzung`, nicht auf `/preise` (dort unverändert).
6. **Nach dem Merge deployen:** `npm run deploy` in `website/`. Das neue `kontakt.php` verlangt das Feld „Anliegen“; Formular und Skript müssen gemeinsam live gehen. Danach einen Live-Test mit Testnachricht machen.
7. **Kontextdateien:** CODE.md, ROLES.md und der DECISIONS-Eintrag vom 2026-10-07 lagen nicht vor; laut Dominik sind die Widersprüche dort (Ausschluss „strategische Beratung“) überholt.
8. Im Repo gibt es weder AGENTS.md noch CLAUDE.md.
