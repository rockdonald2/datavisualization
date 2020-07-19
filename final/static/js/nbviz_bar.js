(function (nbviz) {
    'use strict';

    const chartHolder = d3.select('#nobel-bar');
    const margin = {
        top: 20,
        right: 20,
        bottom: 35,
        left: 40
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
        .attr('y', 6).attr('dy', '.71em').style('text-anchor', 'end');


    nbviz.updateBarChart = function (data) {
        xScale.domain(data.map(function (d) {
            return d.code;
        }));
        yScale.domain([0, d3.max(data, function (d) {
            return +d.value
        })]);

        svg.select('.xaxis').transition().duration(nbviz.TRANS_DURATION)
            .call(xAxis).selectAll('text').style('text-anchor', 'end').attr('dx', '-.8em')
            .attr('dy', '.15em').attr('transform', 'rotate(-65)');
        svg.select('.yaxis').transition().duration(nbviz.TRANS_DURATION)
            .call(yAxis);

        const bars = svg.selectAll('.bar').data(data, function (d) {
            return d.code;
        });

        bars.enter().append('rect').classed('bar', true)
            .merge(bars).classed('active', function (d) {
                return d.key === nbviz.activeCountry;
            })
            .attr('height', height)
            .attr('x', 2 * xPaddingLeft)
            .transition().duration(nbviz.TRANS_DURATION)
            .attr('x', function (d) {
                return xScale(d.code);
            }).attr('y', function (d) {
                return yScale(d.value);
            }).attr('width', xScale.bandwidth())
            .attr('height', function (d) {
                return height - yScale(d.value);
            }).style('fill', '#0048ab');

        bars.exit().remove();

        setTimeout(function() {
            const yLabel = svg.select('#y-axis-label').text('Number of Winners').style('fill', '#000');
        }, nbviz.TRANS_DURATION);
    };

}(window.nbviz = window.nbviz || {}));