import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '../../environments/environment';
import {Task, User} from './models';


/* relative endpoints */
let endpoints = {
  /* auth */
  generateUserToken: ['/api/auth', 'POST'],
  /* users */
  createUser: ['/api/users', 'PUT'],
  login: ['/api/users', 'POST'],
  changePassword: ['/api/users', 'POST'],
  deleteUser: ['/api/users', 'DELETE'],
  getUsers: ['/api/users', 'GET'],
  updateUser: ['/api/users', 'PATCH'],
  /* tasks */
  getTasks: ['/api/tasks', 'GET'],
  createTask: ['/api/tasks', 'POST'],
  resolveTask: ['/api/tasks', 'DELETE'],
  updateTask: ['/api/tasks', 'PATCH'],
  /* machines */
  getMachinesStatus: ['/api/machines', 'POST'],
  /* visitors */
  createVisitor: ['/api/visitors', 'PUT'],
  getVisitors: ['/api/visitors', 'POST'],
};

function endpoint(
  target: Object,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  let [url, method] = endpoints[propertyKey];
  let func = descriptor.value;
  descriptor.value = function(args): any {
    let body = func(args);
    return this.http.request(method, environment.server + url, body);
  };
}


@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(private http: HttpClient) {
  }

  /*
   Below are the endpoints
   # todo explain

   */

  /** Authentication **/

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
    return args;
  }



  // todo users in user fields.
  @endpoint
  getUsers(args: any): any | Observable<{users: [User]}> {
    return args;
  }


  /** Tasks **/

  @endpoint
  createTask(args: any): any | Observable<Response> {
    args['task_id'] = 'null';
    args['status'] = 'null';
    return args;
  }

  @endpoint
  getTasks(args: any): any | Observable<{tasks: [Task]}> {
    return args;
  }

  @endpoint
  resolveTask(args: { 'task_id': string }): any | Observable<Response> {
    return args;
  }


  // todo what's the point of this
  @endpoint
  updateTask(args: any): any | Observable<Response> {
    return args;
  }


  /** machines **/
  @endpoint
  getMachinesStatus(args: any): any | Observable<Response> {
    return args;
  }


  @endpoint
  createVisitor(args: any): any | Observable<Response> {
    return args;
  }



  // todo figure out a way to synchronize documentation with models here
}
