/*
 * Coverts machines response into a format
 * usable by graphs.
 */
var fs = require('fs');
var f = fs.readFileSync('../data/visits.yaml', 'utf8');
var d = JSON.parse(f)['visitors'];
/* converts response to usable data */
function convertData(data, startTime, endTime) {
    var interval = endTime - startTime;
    var type = 'days';
    var stepSize = 1000 * 60 * 60 * 24; // a day
    var steps = Math.floor(interval / stepSize);
    var ret = [{
            name: 'All Users',
            series: []
        }, {
            name: 'New Users',
            series: []
        }
    ]; // return data
    var t = startTime;
    for (var i = 0; i < steps; i++) {
        var series = [];
        t += stepSize;
        var count = {
            'new': 0,
            'all': 0,
        };
        for (var _i = 0, _a = data; _i < _a.length; _i++) {
            var visit = _a[_i];
            var d_1 = visit.date_visited;
            if (t[0] >= d_1 && d_1 <= t[1]) {
                count[d_1.is_new ? 'new' : 'all']++;
            }
        }
        ret[0].series.push({ 'name': i, 'value': count['all'] });
        ret[1].series.push({ 'name': i, 'value': count['new'] });
    }
    return ret;
}
fs.writeFile('./out.json', JSON.stringify(convertData(d, new Date(2021, 2, 5).getTime(), Date.now())), function (err) {
    console.log(err);
});
