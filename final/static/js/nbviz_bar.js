(function (nbviz) {
    'use strict';

    const chartHolder = d3.select('#nobel-bar');
    const margin = {
        top: 20,
        right: 20,
        bottom: 45,
        left: 60
    };
    const boundingRect = chartHolder.node().getBoundingClientRect();

    const width = boundingRect.width - margin.left - margin.right;
    const height = boundingRect.height - margin.top - margin.bottom;

    const xPaddingLeft = 20;

    const xScale = d3.scaleBand().rangeRound([xPaddingLeft, width]).padding(0.1);
    const yScale = d3.scaleLinear().range([height, 0]);

    const xAxis = d3.axisBottom().scale(xScale);
    const yAxis = d3.axisLeft().scale(yScale).ticks(10).tickFormat(function (d) {
        if (nbviz.valuePerCapita) {
            return d.toExponential();
        } else {
            return d;
        }
    });

    const svg = chartHolder.append('svg').attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    svg.append('g').attr('class', 'xaxis').attr('transform', 'translate(0,' + height + ')');
    svg.append('g').attr('class', 'yaxis').append('text').attr('id', 'y-axis-label').attr('transform', 'rotate(-90)')
        .attr('y', 6).attr('dy', '1em').attr('dx', '-.5em').style('text-anchor', 'end');


    nbviz.updateBarChart = function (data) {
        // megelőzi azt, hogy a 0-ás országok bentmaradjanak a tömbben
        data = data.filter(function (d) {
            return d.value > 0;
        })

        xScale.domain(data.map(function (d) {
            return d.code;
        }));
        yScale.domain([0, d3.max(data, function (d) {
            return +d.value
        })]);

        svg.select('.xaxis')
            .call(xAxis).selectAll('text').style('font-size', '1.2rem')/* .transition().duration(nbviz.TRANS_DURATION) */.style('text-anchor', 'end').attr('dx', '-.8em')
            .attr('dy', '.15em').attr('transform', 'rotate(-65)');
        svg.select('.yaxis')
            .call(yAxis).selectAll('text').style('font-size', '1.2rem')/* .transition().duration(nbviz.TRANS_DURATION) */;

        const bars = svg.selectAll('.bar').data(data, function (d) {
            return d.code;
        });

        const colColor = (nbviz.activeCategory === nbviz.ALL_CATS) ? 'goldenrod' : nbviz.categoryFill(nbviz.activeCategory);

        bars.enter().append('rect').classed('bar', true)
            .attr('x', 2 * xPaddingLeft)
            .attr('height', height)
            .merge(bars).classed('active', function (d) {
                return d.key === nbviz.activeCountry;
            })
            .transition().duration(nbviz.TRANS_DURATION)
            .attr('x', function (d) {
                return xScale(d.code);
            }).attr('y', function (d) {
                return yScale(d.value);
            }).attr('width', xScale.bandwidth())
            .attr('height', function (d) {
                return height - yScale(d.value);
            }).style('fill', colColor);

        bars.exit().remove();

        setTimeout(function () {
            const yLabel = svg.select('#y-axis-label').text('Number of Winners').style('fill', '#000').style('font-size', '1.2rem');
        }, nbviz.TRANS_DURATION);
    };

}(window.nbviz = window.nbviz || {}));