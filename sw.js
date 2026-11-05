var C="coc-reminder-v1";
var F=["./","index.html","manifest.json","icon-192.png","icon-512.png"];
self.addEventListener("install",function(e){e.waitUntil(caches.open(C).then(function(c){return c.addAll(F)}));self.skipWaiting()});
self.addEventListener("activate",function(e){e.waitUntil(self.clients.claim())});
self.addEventListener("fetch",function(e){e.respondWith(fetch(e.request).catch(function(){return caches.match(e.request)}))});
