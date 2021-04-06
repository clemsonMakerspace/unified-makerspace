import {Injectable} from '@angular/core';
import {ApiService} from '../api.service';
import {BehaviorSubject, Observable} from 'rxjs';
import {User} from '../models';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  // todo change to function in the future.
  user = new BehaviorSubject<User>(null);

  constructor(private api: ApiService, private router: Router) {
    // todo load user from lacal storage
    if (this.user.getValue() == null) {
      let user = localStorage.getItem('User');
      if (user != null) {
        this.user.next(JSON.parse(user));
      }
    }
  }

  isUserLoggedIn() {
    return this.user.getValue() != null;
  }

  // todo create user object and then pass that in

  // todo implement this method
  // todo intercept subscription
  // todo and add to localstorage
  login(username: string, password: string): Observable<Response> {
    return this.api.login({
      email: username,
      password: password,
    });
  }

  register(email: string, password: string,
           hardwareId: string, firstName: string,
           lastName: string): Observable<Response> {
    return this.api.createUser({
      email: email,
      password: password,
      hardware_id: hardwareId,
      first_name: firstName,
      last_name: lastName,
    });
  }

  // todo add token expiry...
  logout() {
    this.user.next(null);
    localStorage.removeItem('User');
    this.router.navigate(['/']).then();


  }
}
