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

`assets-source/portrait-original.png` wird freigestellt zu `public/assets/portrait.webp` (macOS nötig, Vision-Framework):

```bash
swift scripts/portrait-mask.swift assets-source/portrait-original.png /tmp/mask.png
python3 scripts/portrait-cutout.py assets-source/portrait-original.png /tmp/mask.png public/assets/portrait.webp
```

Die Pixel der Person bleiben unverändert; nur die Randzone zum Originalhintergrund wird neu berechnet.

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
