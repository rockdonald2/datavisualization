"use strict"

let studentData = [{
        'name': 'Bob',
        'id': 0,
        'scores': [68, 75, 56, 81]
    },
    {
        'name': 'Alice',
        'id': 1,
        'scores': [75, 90, 64, 88]
    },
    {
        'name': 'Carol',
        'id': 2,
        'scores': [59, 74, 71, 68]
    },
    {
        'name': 'Dan',
        'id': 3,
        'scores': [64, 58, 53, 62]
    },
]

function processStudentData(data, passThreshold, meritThreshold) {
    passThreshold = typeof passThreshold !== 'undefined' ? passThreshold : 60;
    meritThreshold = typeof meritThreshold !== 'undefined' ? meritThreshold : 75;
    /* A fenti kód esetében inicializálja a paramétereket, 
    amennyiben azok nem kaptak kezdeti értéket a függvény hívásakor */

    data.forEach((sdata) => {
        let av = sdata.scores.reduce((prev, current) => prev + current, 0) / sdata.scores.length;
        sdata.average = av;

        if (av > meritThreshold) {
            sdata.assessment = 'passed with merit';
        } else if (av > passThreshold) {
            sdata.assessment = 'passed';
        } else {
            sdata.assessment = 'failed';
        }

        console.log(sdata.name + "'s (id: " + sdata.id + ") final assessment is: " + sdata.assessment.toUpperCase());
    });
}

processStudentData(studentData);

///////////////////////////////

let foo = {
    'firstKey': 1,
    'secondKey': 2
};

for (let item in foo) {
    if (foo.hasOwnProperty(item)) {
        console.log(item + " " + foo[item]);
    }
}

///////////////////////////////

let Citizen = function(name, country) {
    this.name = name;
    this.country = country;
}

Citizen.prototype = {
    printDetails: function() {
        console.log('Citizen ' + this.name + ' from ' + this.country);
    }
}

let c = new Citizen('Lukács Zs.', 'Hungary');

c.printDetails();

///////////////////////////////

let Citizen = {
    setCitizen: function(name, country) {
        this.name = name;
        this.country = country;
        return this;
    },
    printDetails: function() {
        console.log('Citizen ' + this.name + ' from ' + this.country);
    }
}

let Winner = Object.create(Citizen);

Winner.setWinner = function(name, country, category, year) {
    this.setCitizen(name, country);
    this.category = category;
    this.year = year;
    return this;
}

Winner.printDetails = function() {
    console.log('Nobel winner ' + this.name + ' from ' + this.country + ', category ' + this.category + ', year ' + this.year);
}

let a = Object.create(Winner).setWinner('Einstein A.', 'Switzerland', 'Physics', '1921');

a.printDetails();

///////////////////////////////

let names = ['Alice', 'Bob', 'Carol']

names.forEach(function(i, n) {
    console.log(i + ': ' + n);
})

///////////////////////////////

let items = ['F', 'B', 'B', 'F', 'A', 'C', 'D', 'D'];

_.countBy(items);

///////////////////////////////

function Counter(inc) {
    let count = 0;
    let add = function() {
        count += inc;
        console.log('Current count: ' + count);
    }
    return add;
}

let cntr = Counter(2);

cntr();

cntr();

///////////////////////////////

function outer(bar) {
    this.bar = bar;
    var that = this;
    function inner(baz) {
        this.baz = baz * that.bar;
        // ...
        // ebben az esetben a that a külső függvény this-jére vonatkozik.
    }
}