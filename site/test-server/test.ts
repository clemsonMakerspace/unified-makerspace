/*

 */

const fs = require('fs')
let f = fs.readFileSync('./responses/machines.yaml', 'utf8');
let d = JSON.parse(f)['machines'];


/* converts response to usable data */
function convertData(data, startTime: number, endTime: number) {

    let interval = endTime - startTime;
    let type = 'hours';
    let stepSize = 1000 * 60 * 60; // an hour
    let cutoff = 48; // max units

    // find the best step size for interval
    let hours = interval / stepSize;
    if (hours > cutoff) {
        stepSize *= 24; // one day
        type = 'days';
        if (hours > Math.pow(cutoff, 2)) {
            stepSize *= 7; // one week
            type = 'weeks';
        }
    }

    let steps = Math.floor(interval / stepSize);
    // this.intervalFormat = `${steps} ${type}`; // todo uncomment

    console.log(steps, interval);

    let ret = []; // return data
    let t = startTime;
    for (let i = 0; i < steps; i++) {
        let series = [];
        t += stepSize;
        for (const [key, value] of (<any> Object).entries(data)) {
            let state = 0;
            for (let v of (value as any)) {
                if (t >= v[0] && t <= v[1]) {
                    state = 1; // todo add optimization.
                    break;
                }
                if (t >= v[1]) {
                    break;
                }
            }
            series.push({'name': key, 'value': state});
        }
        ret.push({'name': i + 1, 'series': series});
    }

    return ret;
}


fs.writeFile('./out.json',
    JSON.stringify(
        convertData(d,new Date(2021, 2, 5).getTime(), Date.now())
    ), err => {
        console.log(err)
    })


