/*

 */
var fs = require('fs');
var f = fs.readFileSync('./responses/machines.yaml', 'utf8');
var d = JSON.parse(f)['machines'];
/* converts response to usable data */
function convertData(data, startTime, endTime) {
    var interval = endTime - startTime;
    var type = 'hours';
    var stepSize = 1000 * 60 * 60; // an hour
    var cutoff = 48; // max units
    // find the best step size for interval
    var hours = interval / stepSize;
    if (hours > cutoff) {
        stepSize *= 24; // one day
        type = 'days';
        if (hours > Math.pow(cutoff, 2)) {
            stepSize *= 7; // one week
            type = 'weeks';
        }
    }
    var steps = Math.floor(interval / stepSize);
    // this.intervalFormat = `${steps} ${type}`; // todo uncomment
    console.log(steps, interval);
    var ret = []; // return data
    var t = startTime;
    for (var i = 0; i < steps; i++) {
        var series = [];
        t += stepSize;
        for (var _i = 0, _a = Object.entries(data); _i < _a.length; _i++) {
            var _b = _a[_i], key = _b[0], value = _b[1];
            var state = 0;
            for (var _c = 0, _d = value; _c < _d.length; _c++) {
                var v = _d[_c];
                if (t >= v[0] && t <= v[1]) {
                    state = 1; // todo add optimization.
                    break;
                }
                if (t >= v[1]) {
                    break;
                }
            }
            series.push({ 'name': key, 'value': state });
        }
        ret.push({ 'name': i + 1, 'series': series });
    }
    return ret;
}
fs.writeFile('./out.json', JSON.stringify(convertData(d, new Date(2021, 2, 5).getTime(), Date.now())), function (err) {
    console.log(err);
});
