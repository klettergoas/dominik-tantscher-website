#!/usr/bin/env bash
# Baut die Website und lädt sie per SFTP/rsync zu World4You hoch.
# Server-Angaben kommen aus .env.deploy (nicht versioniert, Vorlage: .env.deploy.example).
# Die Zugangsdaten private/kontakt-config.php am Server werden nie überschrieben oder gelöscht.
set -euo pipefail
cd "$(dirname "$0")/.."

[ -f .env.deploy ] || { echo "Fehlt: .env.deploy (Vorlage: .env.deploy.example)"; exit 1; }
# shellcheck disable=SC1091
source .env.deploy
KEY="${DEPLOY_KEY/#\~/$HOME}"
SSH=(ssh -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=15)

npm run build
rsync -rlt --delete --exclude='.DS_Store' --exclude='kontakt-config.php' \
  -e "${SSH[*]}" dist/ "$DEPLOY_HOST:$DEPLOY_PATH/"
"${SSH[@]}" "$DEPLOY_HOST" "cd '$DEPLOY_PATH' && find . -type d -exec chmod 755 {} + && find . -type f ! -name kontakt-config.php -exec chmod 644 {} +"
echo "Online: https://dominik-tantscher.at"
