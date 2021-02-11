import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() {
  }

  userLoggedIn = false;


  login(): void {
    this.userLoggedIn = true;
  }


}
