(function (nbviz) {
    'use strict';

    const chartHolder = d3.select('#nobel-time');
    const margin = {
        top: 20,
        right: 20,
        bottom: 30,
        left: 40
    };

    const boundingRect = chartHolder.node().getBoundingClientRect();
    const width = boundingRect.width - margin.left - margin.right;
    const height = boundingRect.height - margin.top - margin.bottom;

    const svg = chartHolder.append('svg').attr('height', height + margin.top + margin.bottom)
        .attr('width', width + margin.left + margin.right).append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    const MAX_WINNERS_PER_YEAR = 15
    const xScale = d3.scaleBand().range([0, width]).padding(0.1).domain(d3.range(1900, 2021));
    const yScale = d3.scalePoint().range([height, 0]).domain(d3.range(MAX_WINNERS_PER_YEAR));

    const xAxis = d3.axisBottom().scale(xScale).tickValues(xScale.domain().filter(function (d, i) {
        return !(d % 10);
    }));

    setTimeout(function () {
        svg.append('g').attr('class', 'xaxis').attr('transform', 'translate(0,' + height + ')')
            .call(xAxis).call(function (g) {
                return g.select('.domain').remove();
            }).selectAll('text').style('text-anchor', 'end').attr('dx', '-.8em').attr('dy', '.15em')
            .attr('transform', 'rotate(-65)');

        const catLabels = chartHolder.select('svg').append('g')
            .attr('transform', 'translate(10, 10)').attr('class', 'labels')
            .selectAll('label').data(nbviz.CATEGORIES)
            .enter().append('g').attr('transform', function (d, i) {
                return 'translate(0,' + i * 10 + ')';
            });

        catLabels.append('circle')
            .attr('fill', nbviz.categoryFill)
            .attr('r', xScale.bandwidth() / 2);

        catLabels.append('text')
            .text(function (d) {
                return d;
            })
            .attr('dy', '.4em')
            .attr('x', 10)
            .style('font-size', 10);
    }, nbviz.TRANS_DURATION);

    nbviz.updateTimeChart = function (data) {
        // hozzákössük az adatot a neki megfelelő évoszlopnak, nem index, hanem év szerint, így az esetleges
        // hézagok nem okoznak megjelenítésbeli hibákat, amikoris az index megváltozik
        const years = svg.selectAll('.year')
            .data(data, function (d) {
                return d.key;
            });

        // a hozzákötött adatoknak megfelelően létrehozzuk az oszlopokat
        years.enter().append('g')
            .classed('year', true)
            .merge(years)
            .attr('name', function (d) {
                return d.key;
            })
            .attr('transform', function (year) {
                return "translate(" + xScale(+year.key) + ",-3)"; // azért használjuk a +year-t, hogy átalakítsuk az str-t int-té
            });

        // töröl minden olyan évoszlopot, amelyhez nem került adat hozzákötésre
        years.exit().remove();

        const winners = svg.selectAll('.year').selectAll('.winner').data(function (d) {
            return d.values;
        }, function (d) {
            return d.name;
        });

        winners.enter().append('circle').classed('winner', true).merge(winners)
            .attr('fill', function (d) {
                return nbviz.categoryFill(d.category);
            })
            .attr('cy', height)
            .attr('cx', xScale.bandwidth() / 2)
            .attr('r', xScale.bandwidth() / 2)
            .transition().duration(nbviz.TRANS_DURATION)
            .attr('cy', function (d, i) {
                return yScale(i);
            });

        winners.exit().remove();
    };

}(window.nbviz = window.nbviz || {}));