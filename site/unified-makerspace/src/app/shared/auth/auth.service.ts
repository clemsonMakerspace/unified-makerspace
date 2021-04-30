import {Injectable} from '@angular/core';
import {ApiService} from '../api/api.service';
import {BehaviorSubject, Observable} from 'rxjs';
import {User} from '../models';
import {Router} from '@angular/router';

export function inStorage(prop: string) {
  return {
    get: () => JSON.parse(sessionStorage.getItem(prop)),
    set: (s) => {
      sessionStorage.setItem(prop, JSON.stringify(s));
    }
  };
}


@Injectable({
  providedIn: 'root',
})
export class AuthService {

  user = new BehaviorSubject<User>(null);

  public newUserInfo; // overridden
  public regState; // overridden

  // todo create localObject...

  constructor(private api: ApiService,
              private router: Router) {

    Object.defineProperty(this, 'newUserInfo', inStorage('newUserInfo'));
    Object.defineProperty(this, 'regState', inStorage('regState'));


    /* default state is 'register' */
    if (!this.regState) {
      this.regState = 'register';
    }

    /* get user from localStorage (if any) */
    if (this.user.getValue() == null) {
      let user = localStorage.getItem('User');
      if (user != null) {
        this.user.next(JSON.parse(user));
      }
    }
  }


  /* checks whether user is logged in */
  isUserLoggedIn() {
    return this.user.getValue() != null;
  }


  // todo implement this method
  // todo intercept subscription
  // todo add auth token

  login(args): Observable<Response> {
    return this.api.login(args);
  }

  // todo add token expiry...
  logout() {
    this.user.next(null);
    localStorage.removeItem('User');
    this.router.navigate(['/']).then();
  }

  // todo intercept responses

  createUser(args: any): Observable<Response> {
    // todo modify response ?
    // args['first_name'] = args['first_name']
    return this.api.createUser(args);
  }

}
