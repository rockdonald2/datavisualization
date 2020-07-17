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

let buildCrudeBarChart = function() {
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

    nobelData.forEach(function(d, i) {
        svg.append('rect').classed('bar', true)
            .attr('height', d.value)
            .attr('width', barWidth)
            .attr('y', height - d.value)
            .attr('x', i*(barWidth));
    });
}