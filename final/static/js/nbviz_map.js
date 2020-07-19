(function (nbviz) {
    'use strict';

    // a konténer méretei, valamint az SVG kontextus hozzáadása a DOM-hoz
    const mapContainer = d3.select('#nobel-map');
    const boundingRect = mapContainer.node().getBoundingClientRect();
    const width = boundingRect.width;
    const height = boundingRect.height;

    const svg = mapContainer.append('svg');

    // a scalefaktor lineárisan megfelel a kivetített pontok közötti távolsággal,
    // alapértelmezetten a magasság 480, míg a scalefaktor 153, a mi scalefaktorunk ennél nagyobb 193, és a magasságunk kisebb,
    // így kissé felnagyítsa ez a beállítás a térképet
    // a center a térképünk középpontját határozza meg, 15fok keletre és 15fok északra
    // a translate a projection középpontjának pixelkoordinátáit határozza meg, az alapértelmezett a 480 és 250
    // a precision az adaptive samplinget állítsa be
    const projection = d3.geoEquirectangular().scale(193 * (height / 480)).center([15, 15])
        .translate([width / 2, height / 2]).precision(.1);

    const path = d3.geoPath().projection(projection);

    // 20 fokonként fognak a hálórácsok elhelyezkedni, nem az alapértelmezett 10-esével
    const graticule = d3.geoGraticule().step([20, 20]);

    // kiválasztottuk a projection-t, létrehoztuk a path-et a kiválasztott projection-el, valamint hozzáadtuk a graticule-t is
    // a projection azt határozza meg, hogyan jelenítsük meg a térképet
    // a path a megjelenítésnek megfelelően fogja a JSON állomány koordinátáit SVG path-kké alakítani
    // a graticule a hálót adja hozzá a térképhez a path-nek megfelelően

    // datum(graticule) == datum([graticule])
    svg.append('path').datum(graticule)
        .attr('class', 'graticule').attr('d', path);

    const radiusScale = d3.scaleSqrt().range([nbviz.MIN_CENTROID_RADIUS, nbviz.MAX_CENTROID_RADIUS]);

    // egy objektum, amellyel az országnévnek egy GeoJSON objektumot feleltetünk meg
    const cnameToCountry = {};

    nbviz.initMap = function(world, countryNames) {
        // kinyerjük a földrészeket
        const land = topojson.feature(world, world.objects.land);
        // kinyerjük az országokat, arra használjuk a features mezőt, hogy kinyerjük a FeatureCollection egyenkénti Feature-jeit, mint tömb
        const countries = topojson.feature(world, world.objects.countries).features;
        // kinyerjük a határokat
        // amennyiben az a és b mértani objektum nem egyezik meg, abban az esetben közös határról beszélhetünk
        // amennyiben megegyezik, akkor külső határról
        const borders = topojson.mesh(world, world.objects.countries, function(a, b) {
            return a !== b;
        });

        // hozzáadja a világtérképet
        svg.insert('path', '.graticule').datum(land).attr('class', 'land').attr('d', path);

        // országpath-ek
        svg.insert('g', '.graticule').attr('class', 'countries');

        // az értékindikátorok, amelyek az ország nyerteseit fogják jelölni == piros körök
        svg.insert('g').attr('class', 'centroids');

        // határvonalak
        svg.insert('path', '.graticule') // beilleszti a graticule class-al rendelkező tag elé
            .datum(borders).attr('class', 'boundary').attr('d', path);

        // országnévnek GeoJSON shape-t megfeleltetni
        const idToCountry = {};

        countries.forEach(function (c) {
            idToCountry[c.id] = c;
        });

        countryNames.forEach(function (n) {
            cnameToCountry[n.name] = idToCountry[n.id];
        });

        // tehát, a fenti objektum, egy adott országnévnek megfelelteti a GeoJSON shape-jét
        // ez azt jelenti, hogy ha beadjuk például Ausztráliát, visszatéríti annak a GeoJSON megfelelőjét
    }

    nbviz.updateMap = function (data) {

    };

} (window.nbviz = window.nbviz || {}));