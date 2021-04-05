import {Injectable} from '@angular/core';
import {ApiService} from '../api.service';
import {BehaviorSubject, Observable} from 'rxjs';
import {User} from '../models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  userLoggedIn = false;
  user: BehaviorSubject<User>;

  constructor(private api: ApiService) {
  }




  // todo implement this method
  login(username: string, password: string): Observable<any> {
    this.userLoggedIn = true;
    return this.api.login(username, password);
  }


  // todo implement this method
  register() {
    this.userLoggedIn = true;
  }



  // todo implement
  logout() {}
}
