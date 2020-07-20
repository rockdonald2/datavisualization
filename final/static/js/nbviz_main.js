const query_winners = 'winners?projection=' + JSON.stringify({"mini_bio": 0, "bio_image": 0});

d3.queue()
    /* a statikus fájlok magukba foglalnak egy világtérképet, némi országadatot, 
    valamint egy dinamikus lehívást a Python Eve RESTful API-nkon keresztül a győztes-adatokra, kihagyva az életrajzot */
    .defer(d3.json, "../static/data/world-110m.json")
    .defer(d3.csv, "../static/data/world-country-names-nobel.csv")
    /* a fenti egy topojson-nál megkapható térkép, 1:110millióhoz skálával */
    .defer(d3.json, "../static/data/winning_country_data.json")
    .defer(nbviz.getDataFromAPI, query_winners)
    .await(ready);

function ready(error, worldMap, countryNames, countryData, winnersData) {
    // logulunk bármiféle hibát a console-ra
    if (error) {
        return console.warn(error);
    }

    // tároljuk az országadat adatsorunkat
    nbviz.data.countryData = countryData;
    // létrehozzuk a szűrönket és annak dimenzióit
    nbviz.makeFilterAndDimensions(winnersData);
    // inicializáljuk a menüt és a térképet
    nbviz.initMenu();
    nbviz.initMap(worldMap, countryNames);
    // triggereljük a frissítést a teljes győztes adatsorral
    nbviz.onDataChange();
}