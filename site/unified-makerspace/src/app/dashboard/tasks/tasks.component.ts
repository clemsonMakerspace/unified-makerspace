import {Component, OnInit, Output, EventEmitter, ElementRef} from '@angular/core';
import {ApiService} from '../../shared/api/api.service';
import {Task, User} from 'src/app/shared/models';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';
import {AuthService} from '../../shared/auth/auth.service';

@Component({
  selector: 'app-tasks',
  templateUrl: './tasks.component.html',
  styleUrls: ['./tasks.component.scss'],
})
export class TasksComponent implements OnInit {

  constructor(private modal: NgbModal,
              private api: ApiService,
              public auth: AuthService) {
  }


  tasks: Task[];
  users: User[];
  errorMessage: string;

  selTask;

  // for pagination
  page = 1;
  pageSize = 5;

  tableFields = {
    task_name: 'Task Name',
    assigned_to: 'Assigned To',
    date_created_str: 'Date Created',
    state: 'State',
  };

  keys: string[];


  /* status integer to description */
  status_map = {
    0: 'Not Completed',
    1: 'In-Progress',
    2: 'Completed'
  };

  /* get users on launch */
  ngOnInit(): void {
    this.tasks = []
    this.getUsers();
    this.keys = Object.keys(this.tableFields);
  }


  /* wrapper to open modal */
  open(content: ElementRef, refresh=true) {
    let taskModal = this.modal.open(content, {
      size: 'lg'
    });

    // refresh tasks whenever modal is closed
    if (refresh) {
      if (content.nativeElement.id === 'create-task-modal') {
        taskModal.dismissed.subscribe(() => this.getTasks());
      }
    }
  }


  /* gets users and then tasks */
  getUsers() {
    this.api.getUsers([]).subscribe((res) => {
      this.users = res['users'];
      this.getTasks();
    }, (err) => this.handleError(err));
  }

  /* updates `tasks` array with new tasks */
  getTasks() {
    this.api.getTasks([]).subscribe((res) => {
      this.tasks = res['tasks'];
      this.tasks.forEach(((task, i) => {
          for (let user of this.users) {
            if (user.user_id == task.assigned_to) {
              this.tasks[i]['user_id'] = this.tasks[i].assigned_to;
              this.tasks[i].assigned_to = user.first_name;
            }

          }
          for (let task of this.tasks) {
            task.state = this.status_map[task.status];
            let date = new Date(task['date_created'] * 1000);
            task['date_created_str'] = date.toLocaleString();
          }
        }));
      console.warn(this.tasks);

    }, (err) => this.handleError(err));
  }

  /* changes a task's state */
  changeTaskState(taskId: string, newState: number) {
    this.api.updateTask(
      {'task_id': taskId, 'state': newState}
    ).subscribe((res) => {
      this.getTasks(); // refresh after task state changed
    }, (err) => {
      // todo implement this..
    });
  }

  /* calls `resolveTask` for all completed tasks */
  clearTasks(): void {
    for (let task of this.tasks.filter((task) => task.state == 'Completed')) {
      this.resolveTask(task.task_id);
    }
  }

  /* resolves a single task */
  resolveTask(taskId: string) {
    this.api.resolveTask({
      'task_id': taskId
    }).subscribe((res) => {
      this.getTasks();
    }, (err) => this.handleError(err));
  }


  handleError(err: Error) {
    this.errorMessage = err.message;
  }

  /* export task data to csv */
  exportTaskData() {
    let rowDelimiter = '\n';
    let columnDelimiter = ',';
    let formattedData = 'data:text/csv;charset=utf-8,';

    //setup header of csv as Task, Person, Status
    formattedData +=
      'Task ID' +
      columnDelimiter +
      'Task Name' +
      columnDelimiter +
      'Description' +
      columnDelimiter +
      'Assigned to' +
      columnDelimiter +
      'Date Created' +
      columnDelimiter +
      'Date Resolved' +
      columnDelimiter +
      'Status' +
      rowDelimiter;

    //loop through tasks and add data to csv
    this.tasks.forEach(function(item, index) {
      formattedData +=
        item.task_id +
        columnDelimiter +
        item.task_name +
        columnDelimiter +
        item.description +
        columnDelimiter +
        item.assigned_to +
        columnDelimiter +
        item.date_created +
        columnDelimiter +
        item.date_resolved +
        columnDelimiter +
        item.status +
        rowDelimiter;
    });

    //Download data as a csv
    let encodedUri = encodeURI(formattedData);
    var link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'Tasks.csv');
    document.body.appendChild(link);
    link.click();
  }

}
