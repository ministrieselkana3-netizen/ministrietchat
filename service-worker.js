const CACHE_NAME = "el-kana-ministries-v1";
 
const FILES_TO_CACHE = [
  "./",
  "./index.html",
  "./style.css",
  "./app.js",
  "./manifest.json"
];
 
self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.addAll(FILES_TO_CACHE);
    })
  );
 
  self.skipWaiting();
});
 
self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (cacheNames) {
      return Promise.all(
        cacheNames
          .filter(function (name) {
            return name !== CACHE_NAME;
          })
          .map(function (name) {
            return caches.delete(name);
          })
      );
    })
  );
 
  self.clients.claim();
});
 
self.addEventListener("fetch", function (event) {
  if (event.request.method !== "GET") {
    return;
  }
 
  event.respondWith(
    caches.match(event.request).then(function (cachedResponse) {
      if (cachedResponse) {
        return cachedResponse;
      }
 
      return fetch(event.request).catch(function () {
        return caches.match("./index.html");
      });
    })
  );
});
