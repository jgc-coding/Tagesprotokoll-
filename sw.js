const CACHE = 'protokoll-v5';
const ASSETS = [
  '/Tagesprotokoll-/',
  '/Tagesprotokoll-/index.html',
  '/Tagesprotokoll-/manifest.json',
  '/Tagesprotokoll-/icon-192.png',
  '/Tagesprotokoll-/icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ));
  self.clients.claim();
});

// HTML: network-first, damit App-Updates sofort durchkommen.
// Andere Assets: cache-first, damit App offline lauffähig bleibt.
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const isHtml = req.mode === 'navigate' ||
                 req.destination === 'document' ||
                 (req.headers.get('accept') || '').includes('text/html');

  if (isHtml) {
    e.respondWith(
      fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
        return res;
      }).catch(() =>
        caches.match(req).then(r => r || caches.match('/Tagesprotokoll-/index.html'))
      )
    );
  } else {
    e.respondWith(caches.match(req).then(r => r || fetch(req)));
  }
});
