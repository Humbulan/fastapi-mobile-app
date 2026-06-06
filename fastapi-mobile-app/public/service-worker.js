const CACHE_NAME = 'fastapi-mobile-app-v1.2.0';
const STATIC_CACHE = 'static-cache-v1';
const API_CACHE = 'api-cache-v1';

// Files to cache immediately on install
const PRECACHE_URLS = [
  '/',
  '/static/css/styles.css',
  '/static/js/app.js',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  '/offline'
];

// Install event - cache essential files
self.addEventListener('install', (event) => {
  console.log('Service Worker installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Caching app shell');
        return cache.addAll(PRECACHE_URLS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('Service Worker activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME && cacheName !== STATIC_CACHE && cacheName !== API_CACHE) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - smart caching strategy
self.addEventListener('fetch', (event) => {
  const request = event.request;
  
  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // API calls - Network First, then Cache
  if (request.url.includes('/api/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Cache successful API responses
          if (response.status === 200) {
            const responseClone = response.clone();
            caches.open(API_CACHE)
              .then((cache) => cache.put(request, responseClone));
          }
          return response;
        })
        .catch(() => {
          return caches.match(request)
            .then((cachedResponse) => {
              return cachedResponse || new Response(JSON.stringify({error: 'You are offline'}), {
                headers: {'Content-Type': 'application/json'}
              });
            });
        })
    );
    return;
  }

  // Static assets - Cache First
  if (request.url.includes('/static/')) {
    event.respondWith(
      caches.match(request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          return fetch(request)
            .then((response) => {
              // Cache the new static resource
              const responseClone = response.clone();
              caches.open(STATIC_CACHE)
                .then((cache) => cache.put(request, responseClone));
              return response;
            })
            .catch(() => {
              // Return offline page for navigation requests
              if (request.destination === 'document') {
                return caches.match('/offline');
              }
            });
        })
    );
    return;
  }

  // HTML pages - Network First
  event.respondWith(
    fetch(request)
      .then((response) => response)
      .catch(() => caches.match(request))
  );
});

// Background sync for failed API requests
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    console.log('Background sync triggered');
    // Implement background sync logic here
  }
});
