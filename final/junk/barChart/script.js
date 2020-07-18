const nobelData = [{
        key: 'United States',
        value: 336
    },
    {
        key: 'United Kingdom',
        value: 98
    },
    {
        key: 'Germany',
        value: 79
    },
    {
        key: 'France',
        value: 60
    },
    {
        key: 'Sweden',
        value: 29
    },
    {
        key: 'Switzerland',
        value: 23
    },
    {
        key: 'Japan',
        value: 21
    },
    {
        key: 'Russia',
        value: 19
    },
    {
        key: 'Netherlands',
        value: 17
    },
    {
        key: 'Austria',
        value: 14
    }
];

let buildCrudeBarChart = function () {
    let chartHolder = d3.select('#nobel-bar');

    let margin = {
        top: 20,
        right: 20,
        bottom: 30,
        left: 40
    };

    let boundingRect = chartHolder.node().getBoundingClientRect();

    let width = boundingRect.width - margin.left - margin.right;
    let height = boundingRect.height - margin.top - margin.bottom;

    let barWidth = width / nobelData.length;

    let svg = chartHolder.append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g').classed('chart', true)
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    nobelData.forEach(function (d, i) {
        svg.append('rect').classed('bar', true)
            .attr('height', d.value)
            .attr('width', barWidth)
            .attr('y', height - d.value)
            .attr('x', i * (barWidth));
    });
}

// megszerezzük a chart méreteit
let chartHolder = d3.select('#nobel-bar');
const margin = {
    top: 20,
    right: 20,
    bottom: 30,
    left: 40
};

const X_PADDING_LEFT = 20;

const boundingRect = chartHolder.node().getBoundingClientRect();
const width = boundingRect.width - margin.left - margin.right;
const height = boundingRect.height - margin.top - margin.bottom;

// létrehozzuk a skáláinkat
/* const xScale = d3.scaleBand().rangeRound([0, width]).padding(0.1); */
const xScale = d3.scaleBand().rangeRound([X_PADDING_LEFT, width]).padding(0.1);
const yScale = d3.scaleLinear().rangeRound([height, 0]);

// létrehozzuk a diagramtartó csoportot
let svg = chartHolder.append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g').classed('chart', true)
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

// az update metódusunk, amely az adatokkal való frissítést végzi el a mintának megfelelően
let update = function (data) {
    console.log(data);

    // frissítjük a skáláink tartományát az adatnak megfelelően
    /* xScale.domain(d3.range(data.length)); */
    xScale.domain(data.map(function (d) {
        return d.code;
    }));
    yScale.domain([0, d3.max(data.map(function (d) {
        return d.value;
    }))]);

    // hozzákötjük az adatot az oszlopcsoporthoz
    /* let bars = svg.selectAll('.bar').data(data); */
    let bars = svg.selectAll('.bar').data(data, function (d) {
        return d.code;
    });

    // létrehozzuk az új oszlopokat és frissítjük az összes attribútumját
    bars.enter().append('rect').classed('bar', true);

    svg.selectAll('.bar').transition().duration(2000).attr('height', function (d, i) {
            return height - yScale(d.value);
        }).attr('width', xScale.bandwidth())
        .attr('y', function (d) {
            return yScale(d.value);
        }).attr('x', function (d, i) {
            /* return xScale(i); */
            return xScale(d.code);
        });

    // kitöröljük a felesleges oszlopokat
    bars.exit().remove();
};

// létrehozzuk az x tengelyt, az x skálát reprezentálva vele, az orientációt már a lehívásban megkell határozni
let xAxis = d3.axisBottom().scale(xScale);
// beállitjuk az y tengely tickjeit 10-esével, és a tickFormat-ra azért van szükség, mert az egy főre jutó
// mutatót exponenciális alakra akarjuk hozni, hiszen azok viszonylag kicsi számok
let yAxis = d3.axisLeft().scale(yScale).ticks(10).tickFormat(function (d) {
    /* if (nbviz.valuePerCapita) {
        return d.toExponential();
    } */

    return d;
});

const query_winners = 'winners?projection=' + JSON.stringify({
    "mini_bio": 0,
    "bio_image": 0
});
const query = 'http://localhost:5000/api/' + query_winners;

d3.queue().defer(d3.json, "winning_country_data.json").defer(d3.json, query).await(ready);

let filter = null;
let countryDim = null;
let countryGroups = null;
let data = null;

function ready(error, countryData, winnersData) {
    if (error) {
        return console.warn(error);
    }

    if ('_items' in winnersData) {
        winnersData = winnersData._items;
    }

    filter = crossfilter(winnersData);
    countryDim = filter.dimension(function (o) {
        return o.country;
    });
    countryGroups = countryDim.group().all();

    countryGroups.forEach(function (c) {
        if (c.key in countryData) {
            c['code'] = countryData[c.key]['alpha3Code'];
        }
    });

    data = countryGroups.filter(function (c) {
        return c.hasOwnProperty('code');
    });

    data.forEach(function (c) {
        c['population'] = countryData[c.key]['population'];
    });

    /* data.sort(function (a, b) {
        return b.value - a.value;
    }); */

    xScale.domain(data.map(function (d) {
        return d.code;
    }));

    // az elmozdításra azért van szükség, mert másképp az svg canvas tetején helyezkedne el
    svg.append('g').attr('class', 'xaxis').attr('transform', 'translate(0,' + height + ')');
    svg.append('g').attr('class', 'yaxis');

    update(data);

    setTimeout(function () {
        data.sort(function (a, b) {
            return b.value - a.value;
        });

        update(data);

        let updateAxis = function (data) {
            // elsőként frissítjük a skálatartományok az új adatnak megfelelően
            xScale.domain(data.map(function (d) {
                return d.code;
            }));
            yScale.domain([0, d3.max(data, function (d) {
                return +d.value;
            })]);

            // másodsorban pedig használjuk a tengelygenerátorokat
            svg.select('.xaxis').transition().duration(2000).call(xAxis)
                .selectAll('text').style('text-anchor', 'end').attr('dx', '-.8em')
                .attr('dy', '.15em').attr('transform', 'rotate(-65)');
            svg.select('.yaxis').transition().duration(2000).call(yAxis);
        };

        updateAxis(data);

        svg.append('g')
            .attr('class', 'yaxis')
            .append('text')
            .attr('id', 'y-axis-label')
            .attr('transform', 'rotate(-90)')
            .attr('y', 6)
            .attr('dy', '.71em')
            .style('text-anchor', 'end')
            .text('Number of Winners');

        // elrejtsük az alsó tengelyvonalat, csak a bejegyzések maradnak
        svg.select('.domain').style('display', 'none');
    }, 5000);

};

/* let height = 400;

// megkeressük a tömb legnagyobb értékét
let maxWinners = d3.max(nobelData, function(d) {
    return +d.value;
});

// létrehozzuk a skálánkat, a megfelelő tartománnyal és skálával,
// megfigyelhetjük a fordított sorrendet a skálában, hiszen lényegében egy eltólást jelöl lefelé,
// a max értéket nem kell eltólni, hiszen 400px helyet fog elfoglalni,
// míg a többi ennél kevesebbet és azokat a maradék pixel nagysággal lefelé tóljuk,
// ezt az eltólást határozza meg a skála nekünk
let yScale = d3.scaleLinear().domain([0, maxWinners]).range([height, 0]);

let numInt = d3.interpolate(400, 0);

numInt(1); // 0
numInt(0.5); // 200
numInt(0); // 400

let color = d3.scaleLinear().domain([-1, 0, 1]).range(['red', 'green', 'blue']);

color(-0.5); // zöld és piros közötti szín
color(0); // teljesen zöld
color(0.5); // zöld és kék közötti szín */

/* let oScale = d3.scaleOrdinal().domain(['a', 'b', 'c', 'd', 'e']).range([1, 2, 3, 4, 5]);

oScale('a'); // 1

let bScale = d3.scaleBand().domain([1, 2, 3, 4, 5]).rangeRound([0, 400]);

bScale(5); // 320 */

/* let oScale = d3.scaleBand().domain([1, 2]);

oScale.rangeRound([0, 100]);
oScale(2); // a 2-esnek az 50-et felelteti meg
oScale.bandwidth(); // 50, visszaadja minden band szélességét, padding-el együtt, jelen esetben az 0

// a paddinget törtrészként hatorázzuk meg: 0.1 * 50 = 5
oScale.padding(0.1);
oScale(2); // 52
oScale.bandwidth(); // 42, tehát 5-5 a padding, és 42 a valódi szélessége az oszlopnak */

/* let bScale = d3.scaleBand().domain(d3.range(nobelData.length)).rangeRound([0, 600]).padding(0.1); */

/* let margin = {
    top: 20,
    right: 20,
    bottom: 30,
    left: 40
};

let chartHolder = d3.select('#nobel-bar');
let boundingRect = chartHolder.node().getBoundingClientRect();

let width = boundingRect.width - margin.left - margin.right;
let height = boundingRect.height - margin.top - margin.bottom;

chartHolder.append('svg').attr('width', width + margin.left + margin.right).attr('height', height + margin.top + margin.bottom);
let svg = d3.select('#nobel-bar svg')
            .append('g').classed('chart', true).attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

let chart = d3.select('#nobel-bar .chart');
for (let i = 1; i <= 2; i++) {
    chart.append('rect').classed('bar', true);
} */

/* let bars = chart.selectAll('.bar').data(nobelData);

bars = bars.enter();

bars.append('rect').classed('bar', true).attr('width', 10).attr('height', function (d) { return d.value; })
    .attr('x', function(d, i) { return i * 12; }); */

/* bars.append('rect').classed('bar', true)
    .attr('width', 10).attr('height', function(d) { return d.value; })
    .attr('x', function(d, i) { return i * 12; })
    .attr('y', function(d) { return height - d.value; }) */

/* let bar = d3.select('#nobel-bar .bar');

bar.attr('name', function(d, i) {
    let sane_key = d.key.replace(/ /g, '_');
    
    console.log('__data__ is: ' + JSON.stringify(d) + ', index is ' + i);

    return 'bar__' + sane_key;
}); */

/* let maxWinners = d3.max(nobelData, function(d) {
    return +d.value;
});

let xScale = d3.scaleBand().domain(d3.range(nobelData.length)).rangeRound([0, width]).padding(0.1);
let yScale = d3.scaleLinear().domain([0, maxWinners]).range([height, 0]);

let bars = chart.selectAll('.bar').data(nobelData);

bars.enter().append('rect').classed('bar', true);

bars.attr('x', function(d, i) {
    return xScale(i);
}).attr('width', xScale.bandwidth()).attr('y', function(d) {
    return yScale(d.value);
}).attr('height', function(d) {
    return height - yScale(d.value);
});

bars.exit().remove(); */