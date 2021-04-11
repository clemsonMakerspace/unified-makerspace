import {Component} from '@angular/core';
import {AuthService} from '../shared/auth/auth.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.scss'],
})
export class AuthComponent {


  constructor(private auth: AuthService,
              private router: Router) {
  }

  get state() {
    return this.router.url.split('/')[1];
  }


}
