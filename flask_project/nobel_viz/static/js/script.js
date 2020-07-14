// static/js/script.js

let API_URL = 'http://127.0.0.1:5000/api';

let displayJSON = function(query) {
    d3.json(API_URL + query).then(function(data) {
        d3.select('#query pre').html(query);
        d3.select('#data pre').html(JSON.stringify(data, null, 4));

        console.log(data);
    });
};

/* let query = '/winners?projection=' + JSON.stringify({
    "mini_bio": 0
}); */

// egyik elérési mód

/* let query = '/winners?where=' + JSON.stringify({
    "name": "Albert Einstein"
}); */

// másik elérési mód
// Einstein ID-ja a = 5f0dcfe5b7fb6ee9b727573f
// /api/winners/5f0dcfe5b7fb6ee9b727573f
/* const albert_id = '5f0dcfe5b7fb6ee9b727573f'
let query = '/winners/' + albert_id

displayJSON(query); */

let filters = [ {"name": "year", "op": "gte", "val": 2000},
                {"name": "gender", "op": "==", "val": "female"}
];

let order_by = [ {"field": "year", "direction": "asc"}];

let query = '/winners?' + 'q=' + JSON.stringify({'filters': filters, 'order_by': order_by});

displayJSON(query);