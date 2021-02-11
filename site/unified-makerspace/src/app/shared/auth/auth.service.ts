import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() {
  }

  userLoggedIn = false;


  // todo implement this method
  login(): void {
    this.userLoggedIn = true;
  }


  // todo implement this method
  register() {
    this.userLoggedIn = true;
  }
}
