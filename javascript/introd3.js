let exCircles = function(data) {
    let ex = d3.select('#ex3');

    // beállítjuk az SVG kontextus magasságát és szélességét a paraméterből
    ex.attr('height', data.height).attr('width', data.width);

    // létrehozunk néhány kört a paramétert felhasználva
    ex.selectAll('circle').data(data.circles)
        .enter()
        .append('circle')
        .attr('cx', function(d) { return d.x })
        .attr('cy', function(d) { return d.y })
        .attr('r', function(d) { return d.r })
};

let data = {
    width: 300, height: 225,
    circles: [
        {'x': 50, 'y': 30, 'r': 20},
        {'x': 70, 'y': 80, 'r': 10},
        {'x': 160, 'y': 60, 'r': 10},
        {'x': 200, 'y': 100, 'r': 5},
    ]
};

exCircles(data);