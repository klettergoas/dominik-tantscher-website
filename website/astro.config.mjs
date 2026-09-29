import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://dominik-tantscher.at',
  output: 'static',
  trailingSlash: 'never',
  // Scope-Klasse wird an Komponenten weitergereicht (z. B. <SectionLabel class=…>)
  scopedStyleStrategy: 'class',
  build: {
    // /leistungen → leistungen.html (Auslieferung ohne Endung per .htaccess)
    format: 'file',
    inlineStylesheets: 'always',
  },
  devToolbar: { enabled: false },
});
