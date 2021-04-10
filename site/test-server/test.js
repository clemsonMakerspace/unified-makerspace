var fs = require('fs');
var f = fs.readFileSync('./responses/machines.yaml', 'utf8');
var d = JSON.parse(f);
// todo create string
/* converts response to usable data */
function convertData(data) {
    var startTime = new Date(2021, 2, 20);
    var interval = Date.now() - startTime.getTime();
    var stepSize = 1000 * 60 * 60; // an hour
    // jumps to next step size based on cutoff
    var cutoff = 48;
    // find the best step size for interval
    var hours = interval / stepSize;
    if (hours > cutoff) {
        stepSize *= 24; // one day
        if (hours > Math.pow(cutoff, 2)) {
            stepSize *= 7; // one week
        }
    }
    var steps = Math.floor(interval / stepSize);
    var ret = [];
    var t = startTime.getTime();
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
            series.push({ "name": key, "value": state });
        }
        ret.push({ "name": i + 1, 'series': series });
    }
    return ret;
}
// console.log(convertData(d));
fs.writeFile('./out.json', JSON.stringify(convertData(d)), function (err) {
    console.log(err);
});
