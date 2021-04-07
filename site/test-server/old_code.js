
machines = []

function createFakeData() {
    let types = [
        '3D Printer',
        'Chainsaw',
        'Wire Cutter',
        'Screwdriver',
        'Hammer',
        'Rocket Fuel',
    ];

    // todo get rid of this later
    let values = [1, 1, 1, 1, 1, 1, 1, 0.5, 0, 0.25];

    for (let i = 1; i <= 24; i++) {
        machines.push({
            name: i.toString(),
            series: types.map((t) => ({
                name: t,
                value: values[Math.floor(Math.random() * values.length)],
            })),
        });
    }

    console.log(JSON.stringify(machines))
}
