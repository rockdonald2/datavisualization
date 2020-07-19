/* globális namespace, _, crossfilter, d3 hivatkozások */

(function (nbviz) {
    'use strict';

    nbviz.data = {} // a fő adatobjektumunk
    nbviz.valuePerCapita = 0; // mutató flag-ünk
    nbviz.activeCountry = null;
    nbviz.ALL_CATS = 'All Categories' // konstans
    nbviz.TRANS_DURATION = 2000; // milliszekundumban meghatározott hossza az animációknak
    nbviz.MAX_CENTROID_RADIUS = 30;
    nbviz.MIN_CENTROID_RADIUS = 2;
    nbviz.COLORS = {
        palegold: '#E6BE8A'
    }; // bármely olyan szín, amelynek nevet akarunk adni és később használni
    const $EVE_API = 'http://localhost:5000/api/';

    nbviz.CATEGORIES = [
        "Physiology or Medicine", "Chemistry", "Economics", "Literature", "Peace", "Physics"
    ];

    nbviz.categoryFill = function (category) {
        let i = nbviz.CATEGORIES.indexOf(category);
        return d3.hcl(i / nbviz.CATEGORIES.length * 360, 60, 70);
    };

    /* elfogad egy resource-t (pl. winners?projection={'mini_bio': 0, ...}) 
    és egy callback függvényt, amelyet akkor hívunk le, amikor az API hívás már megoldódott*/
    nbviz.getDataFromAPI = function (resource, callback) {
        d3.json($EVE_API + resource, function (error, data) {
            if (error) {
                return callback(error);
            }

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
    let nestDataByYear = function (entries) {
        return nbviz.data.years = d3.nest()
            .key(function (w) {
                return w.year;
            })
            .entries(entries);
    };

    nbviz.makeFilterAndDimensions = function (winnersData) {
        nbviz.filter = crossfilter(winnersData);

        nbviz.countryDim = nbviz.filter.dimension(function (o) {
            return o.country;
        });

        nbviz.categoryDim = nbviz.filter.dimension(function (o) {
            return o.category;
        });

        nbviz.genderDim = nbviz.filter.dimension(function (o) {
            return o.gender;
        });
    };

    nbviz.filterByCountries = function (countryNames) {
        // ...
    };

    nbviz.filterByCategory = function (cat) {
        // ...
    };

    nbviz.getCountryData = function () {
        // a countryDim az egyik Crossfilter dimenziónk lesz
        let countryGroups = nbviz.countryDim.group().all();

        // előállítjuk a fő adathalmazt
        // használjuk a tömb map metódusát, hogy létrehozzunk egy új tömböt a hozzáadott elemekkel az országadatsorunkból
        let data = countryGroups.map(function (c) {
                // lekéri az adatot felhasználva a csoportkulcsot, pl. 'Australia'
                let cData = nbviz.data.countryData[c.key];
                let value = c.value;
                // ha az egy főre jutó flag bevan állítva, akkor osztjuk a lakossággal
                if (nbviz.valuePerCapita) {
                    value = value / cData.population;
                }

                return {
                    key: c.key, // pl. Németország
                    value: value, // pl. 16 díj
                    code: cData.alpha3Code, // pl. DEU
                };
            })
            .sort(function (a, b) {
                return b.value - a.value; // csökkenő sorrend
            });

        return data;
    };

    /* ez a függvény kerül lehívásra, amikor az adatsor megváltozik, hogy frissítődjenek a vizualizációs elemek */
    nbviz.onDataChange = function () {
        let data = nbviz.getCountryData();
        nbviz.updateBarChart(data);
        nbviz.updateMap(data);
        /* nbviz.updateList(nbviz.countryDim.top(Infinity)); */
        data = nestDataByYear(nbviz.countryDim.top(Infinity));
        nbviz.updateTimeChart(data);
    };

}(window.nbviz = window.nbviz || {}));