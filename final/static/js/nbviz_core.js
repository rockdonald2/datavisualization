/* globális namespace, _, crossfilter, d3 hivatkozások */

(function(nbviz) {
    'use strict';

    nbviz.data = {} // a fő adatobjektumunk
    nbviz.valuePerCapita = 0; // mutató flag-ünk
    nbviz.activeCountry = null; 
    nbviz.ALL_CATS = 'All Categories' // konstans
    nbviz.TRANS_DURATION = 2000; // milliszekundumban meghatározott hossza az animációknak
    nbviz.MAX_CENTROID_RADIUS = 30;
    nbviz.MIN_CENTROID_RADIUS = 2;
    nbviz.COLORS = {palegold: '#E6BE8A'};  // bármely olyan szín, amelynek nevet akarunk adni és később használni
    $EVE_API = 'http://localhost:5000/api/';

    nbviz.CATEGORIES = [
        "Chemistry", "Economics", "Literature", "Peace", "Physics", "Physiology or Medicine"
    ];

    nbviz.categoryFill = function(category) {
        let i = nbviz.CATEGORIES.indexOf(category);
        return d3.hcl(i / nbviz.CATEGORIES.length * 360, 60, 70);
    };

    /* elfogad egy resource-t (pl. winners?projection={'mini_bio': 0, ...}) 
    és egy callback függvényt, amelyet akkor hívunk le, amikor az API hívás már megoldódott*/
    nbviz.getDataFromAPI = function(resource, callback) {
        d3.json($EVE_API + resource, function(error) {
            if (error) {
                return callback(error);
            }
        }).then(function(data) {
            /* ha a válaszul kapott adatnak van 'items' mezője, akkor abban az esetben több győztessel van dolgunk */
            if ('_items' in data) {
                callback(null, data._items);
            } else {
                callback(null, data); /* ellenkező esetben csakis egyetlen győztesről szóló adatot kértünk le */
            }
            /* a callback függvény bevesz egy error, és data argumentumot, ezért szükséges a null */
        });
    };

    /* az üres részek a kontextusuk során lesznek tartalommal feltöltve */
    let nestDataByYear = function(entries) {
        // ...
    };

    nbviz.makeFilterAndDimensions = function(winnersData) {
        // ...
    };

    nbviz.filterByCountries = function(countryNames) {
        // ...
    };

    nbviz.filterByCategory = function(cat) {
        // ...
    };

    nbviz.getCountryData = function() {
        // ...
    };

    /* ez a függvény kerül lehívásra, amikor az adatsor megváltozik, hogy frissítődjenek a vizualizációs elemek */
    nbviz.onDataChange = function() {
        let data = nbviz.getCountryData();
        nbviz.updateBarChart(data);
        nbviz.updateMap(data);
        nbviz.updateList(nbviz.countryDim.top(Infinity));
        data = nestDataByYear(nbviz.countryDim.top(Infinity));
        nbviz.updateTimeChart(data);
    };

} (window.nbviz = window.nbviz || {}));