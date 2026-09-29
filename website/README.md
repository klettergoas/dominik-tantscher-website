# Website dominik-tantscher.at

Statische Website (Astro, Vanilla CSS) nach `../design_handoff_website_dominik_tantscher/README.md`.
Keine externen Requests, keine Cookies, kein Tracking. Kontaktformular über `kontakt.php` (PHPMailer/SMTP).

## Entwicklung

```bash
npm install
npm run dev        # http://localhost:4321 (kontakt.php läuft hier nicht, Versand zeigt die Fehlerbox)
npm run build      # Ergebnis in dist/
npm run assets     # nur nötig, wenn Logo oder Schriften sich ändern (Favicons, OG-Bild, WOFF2)
```

## Inhalte

Alle Texte liegen in `src/content/*.json` (1:1 aus den Kundenunterlagen). Komponenten in `src/components/`, Seiten in `src/pages/`.

## Porträt (Über mich)

`public/assets/portrait.webp` ist das Originalfoto, unverändert eingebunden. Der Hintergrund läuft über eine Transparenzmaske (`public/assets/portrait-mask.png`) weich in die Seite aus; die Person bleibt voll deckend. Maske neu erzeugen (macOS nötig, Vision-Framework):

```bash
swift scripts/portrait-mask.swift public/assets/portrait.webp /tmp/silhouette.png
python3 scripts/portrait-fade-mask.py /tmp/silhouette.png public/assets/portrait-mask.png
```

## Deployment (World4You)

Einmalig: `.env.deploy.example` als `.env.deploy` kopieren und die SSH/SFTP-Angaben aus dem World4You-Kundenbereich eintragen; den eigenen Public Key dort unter „SSH / SFTP → Public-Key hinzufügen“ hinterlegen.

```bash
npm run deploy     # baut und lädt dist/ hoch
```

Hinweise:
- Das SSH-Startverzeichnis ist das Webroot. Die SMTP-Zugangsdaten liegen am Server in `private/kontakt-config.php` (Ordner per `.htaccess` gesperrt) und werden beim Deployment nie angefasst. Vorlage: `kontakt-config.example.php`.
- Manche Netzwerke blockieren Port 22 – dann z. B. über einen Handy-Hotspot deployen.
- PHP-Version am Webhosting: 8.1 oder neuer.
- Die `.htaccess` erzwingt HTTPS (inkl. HSTS), leitet `www.` auf die Domain ohne www um, liefert `/leistungen` aus `leistungen.html` aus und setzt Sicherheits-Header (CSP u. a.). Das SSL-Zertifikat läuft bis 27.03.2027 und wird von World4You verlängert.

## Spamschutz

Honeypot-Feld `website` + Ausfülldauer `dauer` (per JS, < 3 s = Spam). Spam erhält eine Erfolgsmeldung, wird aber nicht versendet. Ohne JS greift nur der Honeypot.
