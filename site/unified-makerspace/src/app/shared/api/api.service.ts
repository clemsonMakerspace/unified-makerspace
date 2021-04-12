import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '../../../environments/environment';
import {Task, User} from '../models';


// todo figure out a way to synchronize
//  documentation with models here ?

/* relative endpoints */

let endpoints = {
  /* admin */
  generateUserToken: ['/api/admin', 'POST'],
  resetPassword: ['/api/admin', 'PATCH'],
  /* users */
  changePassword: ['/api/users', 'POST'],
  createUser: ['/api/users', 'PUT'],
  deleteUser: ['/api/users', 'DELETE'],
  getUsers: ['/api/users', 'GET'],
  login: ['/api/users', 'POST'],
  updateUser: ['/api/users', 'PATCH'],
  /* tasks */
  createTask: ['/api/tasks', 'POST'],
  getTasks: ['/api/tasks', 'GET'],
  resolveTask: ['/api/tasks', 'DELETE'],
  updateTask: ['/api/tasks', 'PATCH'],
  /* machines */
  deleteMachine: ['/api/machines', 'DELETE'],
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
    console.log(body); // todo for testing
    return this.http.request(method,
      environment.server + url, body);
  };
}


@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(private http: HttpClient) {
  }


  /** Admin **/

  @endpoint
  generateUserToken(): any | Observable<Response> {
    return // no parameters
  }

  @endpoint
  resetPassword(args: any): any | Observable<Response> {
    return {email: args.email};
  }


  /** Users **/

  @endpoint
  login(args: any): any | Observable<User> {
    return args;
  }

  @endpoint
  createUser(args: any): any | Observable<User> {
    return {
      email: args['email'],
      password: args['password'],
      first_name: args['firstName'],
      last_name: args['lastName'],
      user_token: args['userToken']
    };
  }

  @endpoint
  deleteUser(args: any) {
    return args;
  }


  // todo users in user fields.
  @endpoint
  getUsers(args: any): any | Observable<{ users: [User] }> {
    return args;
  }

  @endpoint
  changePassword(args: any): any | Observable<Response> {
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
  getTasks(args: any): any | Observable<{ tasks: [Task] }> {
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


  /** visitors **/
  @endpoint
  createVisitor(args: any): any | Observable<Response> {
    return {
      visitor: {
        email: args['email'],
        password: args['password'],
        first_name: args['firstName'],
        last_name: args['lastName'],
        major: args['major'],
        degree: args['degree'],
      },
      hardware_id: args['hardwareId']
    };
  }


  @endpoint
  getVisitors(args: any): any | Observable<Response> {
    return args;
  }


}
