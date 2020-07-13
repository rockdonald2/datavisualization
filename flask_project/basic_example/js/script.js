let loadWinnersJson = d3.json('../data/winners_cleaned.json', function (error) {
    if (error) {
        console.log(error); // ha hibát észlel írja ki a console-ba
    }
}).then(function(data) {
    d3.select('h2#data-title').text('All the Nobel-winners');
    // kiválasztjuk a h2 tag-et és megváltoztatjuk annak belső tartalmát
    d3.select('div#data pre').html(JSON.stringify(data, null, 4));
    // a stringify egy hasznos függvény, 
    // amellyel egy JS objectet alakítunk outputolhatová
    // kiválasztjuk a div tag-et és megváltoztatjuk annak belső tartalmát
    // az adatunk tartalmára, a null paraméterrel azt határozzuk meg, hogy nincs egy függvény, amely átalakítja a tartalmat,
    // a 4-es paraméterrel pedig annak indentációját állítjuk be, szóközökben pontosítva, a könnyebb olvashatóság miatt
});

let loadWinnersCountryJson = function(country) {
    d3.json('../data/winners_by_country/' + country + '.json', function(error) {
        if (error) {
            console.log(error);
        }
    }).then(function (data) {
        d3.select('h2#data-title').text('All the Nobel-winners from ' + country);
        d3.select('div#data pre').html(JSON.stringify(data, null, 4));
    })
}

// egyszerűen a függvénnyel lehívhatjuk az érdekelt ország Nobel-adatait
loadWinnersCountryJson('Saint Lucia');