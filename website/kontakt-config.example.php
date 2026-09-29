<?php
// Vorlage für die SMTP-Zugangsdaten des Kontaktformulars.
// Als "kontakt-config.php" EINE EBENE ÜBER dem Webroot ablegen (nicht öffentlich abrufbar)
// und die Werte eintragen. Diese Datei nie ins Webroot und nie in ein Repository legen.
return [
    'smtp_host'   => '',          // SMTP-Server des Postfachs
    'smtp_port'   => 587,         // 587 = STARTTLS, 465 = SSL
    'smtp_secure' => 'tls',       // 'tls' (STARTTLS), 'ssl' oder 'none' (nur für lokale Tests)
    'smtp_user'   => '',          // SMTP-Benutzername
    'smtp_pass'   => '',          // SMTP-Passwort / App-Passwort
    'from_email'  => '',          // Absender, muss zum SMTP-Konto passen
    'from_name'   => 'Website dominik-tantscher.at',
    'to_email'    => 'ki@dominik-tantscher.at',
];
