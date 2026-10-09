import site from '../content/site.json';

const paths = ['/', '/leistungen', '/praxisbeispiele', '/referenzen', '/ueber-mich', '/kontakt', '/impressum', '/datenschutz'];

export function GET() {
  const urls = paths.map((p) => `  <url><loc>${site.url}${p}</loc></url>`).join('\n');
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml' } });
}
