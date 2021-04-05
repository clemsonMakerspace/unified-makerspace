import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from "rxjs";
import {environment} from '../../environments/environment';
import {User} from "./models";

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  server = environment.server;
  constructor(private http: HttpClient) {}

  endpoints = {
    // authentication
    'createUser': ['/api/users', 'POST'],
    'deleteUser': ['/api/users', 'DELETE'],
    'getUsers': ['/api/users', 'GET'],
    'updatePermissions': ['/api/users', 'PATCH'],
    // tasks
    'createTask': ['/api/tasks', 'POST'],
    'resolveTask': ['/api/tasks', 'DELETE'],
    'updateTask': ['/api/tasks', 'PATCH'],
    // machines
    'getMachinesStatus': ['/api/machines', 'GET'],
    // visitors
    'getVisitors': ['/api/visitors', 'GET']

    // todo add the rest...
    // todo add "requests" in the future
  }


  apiEndpoint() {

  }


  /*
    Authentication
   */

  @this.apiEndpoint()
  createUser(email: string, password: string) {
    let [url, method] = this.endpoints['createUser'];
    return this.http.request<User>(method, url, {
      body: {
        'email': email,
        'password': password
      }
    });
  }


  deleteUser(user_id: string) {
    let [url, method] = this.endpoints['deleteUser'];
    return this.http.request(method, url, {
      body: {
        'user_id': user_id,
      }
    });
  }


  getUsers() {
    let [url, method] = this.endpoints['getUsers'];
    return this.http.request(method, url);
  }


  updatePermissions(user_id: string, user) {

  }


  /*
  Tasks
   */

  createTask(task) {


    return this.http.get('endpoint')

  }


  getTasks() {

  }

  resolveTask(task_id: string) {

  }

  updateTask(task) {

  }


  // todo not implemented
  login(username: string, password: string) {
    let [url, method] = this.endpoints['createUser'];
    return this.http.request<User>(method, url, {
      body: {
        'email': username,
        'password': password
      }
    });
  }


}
