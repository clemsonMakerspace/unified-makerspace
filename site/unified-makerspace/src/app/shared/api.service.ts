import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { User, Task } from './models';

let endpoints = {
  // authentication
  createUser: ['/api/users', 'POST'],
  deleteUser: ['/api/users', 'DELETE'],
  getUsers: ['/api/users', 'GET'],
  updateUser: ['/api/users', 'PATCH'],
  login: ['/api/users', 'POST'],
  // tasks
  getTasks: ['/api/tasks', 'GET'],
  createTask: ['/api/tasks', 'POST'],
  resolveTask: ['/api/tasks', 'DELETE'],
  updateTask: ['/api/tasks', 'PATCH'],
  // machines
  getMachinesStatus: ['/api/machines', 'GET'],
  // visitors
  getVisitors: ['/api/visitors', 'GET'],

  // todo add the rest...
  // todo add "requests" in the future
};

function endpoint(
  target: Object,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  let [url, method] = endpoints[propertyKey];
  console.log(environment.server + url); // todo remove
  let func = descriptor.value;
  descriptor.value = function (args): any {
    let body = func(args);
    console.log(body); // todo remove
    return this.http.request(method, environment.server + url, body);
  };
}

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(private http: HttpClient) {}

  /*
    Authentication
   */

  @endpoint
  login(args: any): any | Observable<User> {
    return args;
  }

  @endpoint
  createUser(args: any): any | Observable<User> {
    // todo modify response?
    return args;
  }

  @endpoint
  deleteUser(args: any) {
    // let [url, method] = this.endpoints['deleteUser'];
    // return this.http.request(method, url, {
    //   body: {
    //     'user_id': user_id,
    //   }
    // });
  }

  //
  // getUsers() {
  //   let [url, method] = this.endpoints['getUsers'];
  //   return this.http.request(method, url);
  // }
  //

  updatePermissions(user_id: string, user) {}

  /*
  Tasks
   */

  createTask(task) {
    return this.http.get('endpoint');
  }

  @endpoint
  getTasks(args: any): Observable<[Task]> {
    return args;
  }

  resolveTask(task_id: string) {}

  updateTask(task) {}
}
