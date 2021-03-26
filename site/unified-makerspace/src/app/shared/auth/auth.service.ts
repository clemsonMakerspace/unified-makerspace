import {Injectable} from '@angular/core';
import {ApiService} from "../api.service";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private api: ApiService) {
  }

  userLoggedIn = false;


  // todo implement this method
  login(username: string, password: string): Observable<any> {
    this.userLoggedIn = true;
    return this.api.login(username, password);
  }


  // todo implement this method
  register() {
    this.userLoggedIn = true;
  }
}
