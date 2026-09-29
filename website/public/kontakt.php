<?php
/**
 * Kontaktformular: nimmt den POST entgegen, prüft Spamschutz und Eingaben
 * und sendet die Nachricht per SMTP an das Postfach. Es wird nichts gespeichert
 * und nichts protokolliert (außer den Standard-Serverlogs des Hosters).
 *
 * Zugangsdaten: kontakt-config.php eine Ebene ÜBER dem Webroot oder, wenn das
 * beim Hoster nicht möglich ist, im gesperrten Ordner private/ (Vorlage:
 * kontakt-config.example.php im Projekt). Alternativ Umgebungsvariablen.
 */

declare(strict_types=1);

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception as MailException;

require __DIR__ . '/lib/phpmailer/Exception.php';
require __DIR__ . '/lib/phpmailer/PHPMailer.php';
require __DIR__ . '/lib/phpmailer/SMTP.php';

const MIN_SECONDS = 3;

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function respond(bool $ok, bool $wantsJson, array $errors = []): never
{
    if ($wantsJson) {
        http_response_code($ok ? 200 : ($errors ? 422 : 500));
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: no-store');
        echo json_encode(['ok' => $ok, 'errors' => $errors], JSON_UNESCAPED_UNICODE);
    } else {
        header('Location: /kontakt?status=' . ($ok ? 'ok#gesendet' : 'fehler#sendefehler'), true, 303);
    }
    exit;
}

function field(string $name, int $max, bool $multiline = false): string
{
    $value = $_POST[$name] ?? '';
    if (!is_string($value)) {
        return '';
    }
    $value = trim($value);
    // Steuerzeichen entfernen (bei einzeiligen Feldern auch Zeilenumbrüche)
    $value = $multiline
        ? preg_replace('/[^\P{C}\n\t]/u', '', str_replace("\r\n", "\n", $value))
        : preg_replace('/\p{C}/u', '', $value);
    return mb_substr((string) $value, 0, $max);
}

function config(): array
{
    $cfg = [];
    foreach ([dirname(__DIR__) . '/kontakt-config.php', __DIR__ . '/private/kontakt-config.php'] as $file) {
        if (is_file($file)) {
            $cfg = require $file;
            break;
        }
    }
    $env = fn(string $key, $default = '') => getenv($key) !== false ? getenv($key) : $default;
    return [
        'smtp_host' => $cfg['smtp_host'] ?? $env('SMTP_HOST'),
        'smtp_port' => (int) ($cfg['smtp_port'] ?? $env('SMTP_PORT', 587)),
        'smtp_secure' => $cfg['smtp_secure'] ?? $env('SMTP_SECURE', 'tls'),
        'smtp_user' => $cfg['smtp_user'] ?? $env('SMTP_USER'),
        'smtp_pass' => $cfg['smtp_pass'] ?? $env('SMTP_PASS'),
        'from_email' => $cfg['from_email'] ?? $env('MAIL_FROM'),
        'from_name' => $cfg['from_name'] ?? $env('MAIL_FROM_NAME', 'Website dominik-tantscher.at'),
        'to_email' => $cfg['to_email'] ?? $env('MAIL_TO', 'ki@dominik-tantscher.at'),
    ];
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /kontakt', true, 303);
    exit;
}

// Spamschutz: Honeypot muss leer sein, Ausfülldauer (per JS) mindestens 3 Sekunden.
// Verdächtige Anfragen erhalten eine Erfolgsmeldung, werden aber nicht versendet.
$honeypot = $_POST['website'] ?? '';
$dauer = $_POST['dauer'] ?? '';
if ($honeypot !== '' || ($dauer !== '' && (!ctype_digit((string) $dauer) || (int) $dauer < MIN_SECONDS))) {
    respond(true, $wantsJson);
}

$name = field('name', 200);
$firma = field('firma', 200);
$email = field('email', 254);
$telefon = field('telefon', 50);
$nachricht = field('nachricht', 5000, true);

$errors = [];
if ($name === '') {
    $errors['name'] = 'Bitte geben Sie Ihren Namen an.';
}
if (filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
    $errors['email'] = 'Bitte geben Sie eine gültige E-Mail-Adresse an.';
}
if ($nachricht === '') {
    $errors['nachricht'] = 'Bitte schreiben Sie kurz, worum es geht.';
}
if ($errors) {
    respond(false, $wantsJson, $errors);
}

$cfg = config();
if ($cfg['smtp_host'] === '' || $cfg['from_email'] === '') {
    respond(false, $wantsJson);
}

$body = "Neue Nachricht über das Kontaktformular auf dominik-tantscher.at\n\n"
    . "Name: {$name}\n"
    . 'Betrieb / Firma: ' . ($firma !== '' ? $firma : '–') . "\n"
    . "E-Mail: {$email}\n"
    . 'Telefon: ' . ($telefon !== '' ? $telefon : '–') . "\n\n"
    . "Nachricht:\n{$nachricht}\n";

$mail = new PHPMailer(true);
try {
    $mail->isSMTP();
    $mail->Host = $cfg['smtp_host'];
    $mail->Port = $cfg['smtp_port'];
    $mail->SMTPAuth = $cfg['smtp_user'] !== '';
    $mail->Username = $cfg['smtp_user'];
    $mail->Password = $cfg['smtp_pass'];
    if ($cfg['smtp_secure'] === 'none') {
        $mail->SMTPSecure = '';
        $mail->SMTPAutoTLS = false;
    } else {
        $mail->SMTPSecure = $cfg['smtp_secure'] === 'ssl' ? PHPMailer::ENCRYPTION_SMTPS : PHPMailer::ENCRYPTION_STARTTLS;
    }
    $mail->Timeout = 15;
    $mail->CharSet = PHPMailer::CHARSET_UTF8;

    $mail->setFrom($cfg['from_email'], $cfg['from_name']);
    $mail->addAddress($cfg['to_email']);
    $mail->addReplyTo($email, $name);
    $mail->Subject = 'Kontaktformular: ' . $name;
    $mail->Body = $body;
    $mail->isHTML(false);

    $mail->send();
} catch (MailException $e) {
    respond(false, $wantsJson);
}

respond(true, $wantsJson);
