import { Component, OnInit } from '@angular/core';
import {ModalService} from '../shared/modal.service';
import {NgxChartsModule} from '@swimlane/ngx-charts';
import {BrowserModule} from '@angular/platform-browser'
import * as d3 from 'd3';



@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  constructor(public modal: ModalService) { }

  ngOnInit(): void {
    // this.
  }


  requests = [
    {
      "name": "Will",
      "request": "3D printer ink is out.",
      "date": "Today"
    },
    {
      "name": "Blythe",
      "request": "The wrenches are difficult to find.",
      "date": "Two weeks ago"
    },

  ]


  data = [{
    "name": "All Users",
    "series": [
      {
        "name": "Today",
        "value": 2
      },
      {
        "name": "Yesterday",
        "value": 7
      },
      {
        "name": "Wednesday",
        "value": 4
      },
      {
        "name": "Tuesday",
        "value": 9
      }
    ]
  },
    {
      "name": "New Users",
      "series": [
        {
          "name": "Today",
          "value": 1
        },
        {
          "name": "Yesterday",
          "value": 3
        },
        {
          "name": "Wednesday",
          "value": 2
        },
        {
          "name": "Tuesday",
          "value": 4
        }
      ]
    }]



  // todo remove d3.js?

  draw() {

    let csv_file = '/assets/data.csv'
    let canvas = d3.select('svg')
    let x = (d) => +d['day'];
    let y = (d) => +d['frequency'];
    let [px, py] = [500, 300] // canvas size

    d3.csv(csv_file)
      .then(data => graph(data))

    function graph(data) {


      // create ranges
      let scX = d3.scaleLinear()

        .domain(d3.extent(data, d => x(d)))
        .range([0, px])

      let scY = d3.scaleLinear()
        .domain(d3.extent(data, d => y(d)))
        .range([0, py]);


      // draw axes
      canvas.append('g')
        .call(d3.axisRight(scY));

      canvas.append('g')
        .attr('transform', 'translate(0,' + py + ')')
        .call(d3.axisTop(scX));


      // draw graph
      canvas.selectAll('circle')
        .data(data)
        .enter()
        .append('circle')
        .attr('r', 7)
        .attr('cx', (d) => scX(x(d)))
        .attr('cy', (d) => scY(y(d)))
        .attr('class', 'fill-primary')
        .on('mouseover', (e) => {
          console.log(e);
          let t = d3.select(e.target).attr('r', e.clientY / 10);
          if (e.shiftKey) {
            t.attr('fill', 'yellow');
          }
        })


      let line = d3.line()
        .x((d) => scX(x(d)))
        .y((d) => scY(y(d)))


      canvas.append('path')
        .attr('fill', 'none')
        .attr('class', 'stroke-primary')
        .attr('stroke-width', '5px')
        .attr('d', line(data))
    }
  }


}
