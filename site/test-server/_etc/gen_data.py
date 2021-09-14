"""
gen_data.py

"""

# todo refactor later

import random
import json


def gen_machine_data():
    machines = ["Screwdriver", "Hammer", "Chain Saw", "Rocket Fuel"]
    data = {}
    for machine in machines:
        data[machine] = []
        slots = random.randint(2, 8)
        for _ in range(slots):
            # todo times are random ints rn
            # todo fix later so sequential
            time = [random.getrandbits(30), random.getrandbits(30)]
            data[machine].append(time)

    with open("machines.yaml", "w") as f:
        # yaml is a superset of json
        # but json looks a bit cleaner
        # sometimes
        json.dump(data, f)


gen_machine_data()
