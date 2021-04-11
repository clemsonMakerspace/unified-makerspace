/*
 * Coverts visitors response into a format
 * usable by graphs.
 */

const fs = require('fs')
let f = fs.readFileSync('../data/visits.yaml', 'utf8');
let d = JSON.parse(f)['visits'];


/* converts response to usable data */
function convertData(data: [], startTime: number, endTime: number) {

    let interval = endTime - startTime;
    let type = 'days';
    let stepSize = 1000 * 60 * 60 * 24; // a day
    let steps = Math.floor(interval / stepSize);

    let ret = [{
        name: 'All Users',
        series: []
    }, {
        name: 'New Users',
        series: []
    }
    ]; // return data
    let t = startTime;
    for (let i = 0; i < steps; i++) {
        let series = [];
        t += stepSize;
        let count = {
            'new': 0,
            'all': 0,
        }
        for (const visit of (data as any)) {
            let d = visit.date_visited;
            if (t[0] >= d && d <= t[1]) {
                count[d.is_new ? 'new' : 'all']++;
            }
        }
        ret[0].series.push({'name': i, 'value': count['all']});
        ret[1].series.push({'name': i, 'value': count['new']});
    }

    return ret;
}


fs.writeFile('./out.json',
    JSON.stringify(
        convertData(d, new Date(2021, 2, 5).getTime(), Date.now())
    ), err => {
        console.log(err)
    })


