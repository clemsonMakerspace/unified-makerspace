/*

 */

const fs = require('fs')
let f = fs.readFileSync('./responses/machines.yaml', 'utf8');
let d = JSON.parse(f);

/* converts response to usable data */
function convertData(data) {
    let startTime = new Date(2021, 2, 20);
    let interval = Date.now() - startTime.getTime();

    let stepSize = 1000 * 60 * 60; // an hour

    // jumps to next step size based on cutoff
    let cutoff = 48;

    // find the best step size for interval
    let hours = interval / stepSize;
    if (hours > cutoff) {
        stepSize *= 24; // one day
        if (hours > Math.pow(cutoff, 2)) {
            stepSize *= 7; // one week
        }
    }

    let steps = Math.floor(interval / stepSize);

    let ret = []

    let t = startTime.getTime();
    for (let i = 0; i < steps; i++) {
        let series = []
        t += stepSize;
        for (const [key, value] of (<any>Object).entries(data)) {
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
            series.push({"name": key, "value": state})
        }
        ret.push({"name": i + 1, 'series': series})
    }

    return ret;
}


fs.writeFile('./out.json',
    JSON.stringify(convertData(d)), err => {
        console.log(err)
    })


