import {Component, OnInit} from '@angular/core';
import {ModalService} from '../../shared/modal.service';

@Component({
  selector: 'app-tasks',
  templateUrl: './tasks.component.html',
  styleUrls: ['./tasks.component.scss']
})
export class TasksComponent implements OnInit {

  constructor(public modal: ModalService) {
  }

  tasks = [{
    task: 'Replace 3D-Printer Cartridge',
    person: 'Ellie',
    status: 'Completed',
  },
    {
      task: 'Install new CNC-Router',
      person: 'Beck',
      status: 'In-Progress'
    },
    {
      task: 'Update the Sign-in System',
      person: 'Peach',
      status: 'Not Started'
    }
  ];


  ngOnInit(): void {
  }

  clearTasks(): void {
    this.tasks = this.tasks.filter((task) =>
      task.status !== 'Completed'
    );

  }

  exportTaskData(){
    let rowDelimiter = '\n'
    let columnDelimiter = ','
    let formattedData = 'data:text/csv;charset=utf-8,'

    //setup header of csv as Task, Person, Status
    formattedData += "Task" + columnDelimiter + "Person" + columnDelimiter + "Status" + rowDelimiter

    //loop through tasks and add data to csv
    this.tasks.forEach(function (item, index) {
      formattedData += item.task + columnDelimiter + item.person + columnDelimiter + item.status + rowDelimiter
    });

    //Download data as a csv
    let encodedUri = encodeURI(formattedData);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "Tasks.csv")
    document.body.appendChild(link)
    link.click()
  }
}
