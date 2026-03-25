const CACHE_NAME = 'suaranusa-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/static/css/style.min.css',
  '/static/images/logo.jpg',
  '/manifest.json'
];

// Install Event
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// Activate Event
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

// Fetch Event: Stale-While-Revalidate Strategy
self.addEventListener('fetch', (event) => {
  // Only handle GET requests for our own origin
  if (event.request.method !== 'GET' || !event.request.url.startsWith(self.location.origin)) {
    return;
  }

  event.respondWith(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.match(event.request).then((cachedResponse) => {
        const fetchPromise = fetch(event.request).then((networkResponse) => {
          // Clone the response and update the cache
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        }).catch(() => {
          // Fallback if offline and no cache match
          return cachedResponse;
        });

        // Return the cached version if available, but fetch updated version anyway
        return cachedResponse || fetchPromise;
      });
    })
  );
});
