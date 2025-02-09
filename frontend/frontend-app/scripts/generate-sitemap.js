import fs from 'fs-extra'; // File system module to write files
import { SitemapStream, streamToPromise } from 'sitemap';

const BASE_URL = 'https://dananddrumpersonalizedsongs.com';

// Define static pages
const pages = [
  '/',
  '/personalized-song-levels',
];

(async () => {
  const sitemap = new SitemapStream({ hostname: BASE_URL });

  // Add static pages
  pages.forEach((page) => {
    sitemap.write({ url: page, changefreq: 'weekly', priority: 0.8 });
  });

  sitemap.end();

  // Convert to XML and save to the public folder
  const sitemapXML = await streamToPromise(sitemap).then((data) => data.toString());
  fs.writeFileSync('public/sitemap.xml', sitemapXML);

  console.log('✅ Sitemap successfully generated at public/sitemap.xml');
})();