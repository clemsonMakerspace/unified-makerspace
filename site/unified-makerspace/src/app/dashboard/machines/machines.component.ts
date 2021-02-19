import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-machines',
  templateUrl: './machines.component.html',
  styleUrls: ['./machines.component.scss']
})
export class MachinesComponent implements OnInit {

  constructor() { }

  machines = []

  stateMap = {
    '1': 'Working',
    '.5': 'Being Used',
    '.25': 'Being Repaired',
    '0': 'Not Working'
  }

  ngOnInit(): void {
    this.createFakeData();
    console.log(this.stateMap)
  }

  createFakeData() {
    let types = ['3D Printer', 'Chainsaw', 'Wire Cutter', 'Screwdriver', 'Hammer', 'Rocket Fuel']
    let values = [1, 1, 1, 1, 1, 1, 1, .5, 0, .25]

    for(let i =0; i < 24; i++) {
      this.machines.push({
        'name': i.toString(),
        'series': types.map(t => ({
          'name':t,
          'value': values[Math.floor(Math.random()*values.length)]
        }))
      })
    }
  }





  tooltip(data) {
    if (!this.stateMap) {
      return ""
    }
    console.log(data)
    return data.label + ' ' + this.stateMap[data.data.toString()] + ' at hour ' + data.series;
  }


}
