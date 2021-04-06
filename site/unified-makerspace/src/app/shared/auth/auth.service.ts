import {Injectable} from '@angular/core';
import {ApiService} from '../api.service';
import {BehaviorSubject, Observable} from 'rxjs';
import {User} from '../models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {


  // todo change to function in the future.
  userLoggedIn = false;
  user = new BehaviorSubject<User>(null);

  constructor(private api: ApiService) {
  }


  // todo create user object and then pass that in


  // todo implement this method
  login(username: string, password: string): Observable<Response> {
    // this.userLoggedIn = true; // todo necessary?
    return this.api.login({
      'email': username,
      'password': password
    });
  }


  // todo implement this method
  register(
    email: string,
    password: string, hardwareId: string,
    firstName: string, lastName: string,
  ): Observable<Response> {
    // this.userLoggedIn = true; // todo necessary?
    return this.api.createUser({
      'email': email,
      'password': password,
      'hardware_id': hardwareId,
      'first_name': firstName,
      'last_name': lastName
    });
  }


  // todo get cookie information automatically

  // todo implement
  logout() {
    this.user.next(null);
    // todo remove cookie information
  }
}
