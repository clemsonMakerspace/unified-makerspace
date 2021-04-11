import { Component, OnInit } from '@angular/core';
import {AuthService} from '../shared/auth/auth.service';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.scss'],
})
export class AuthComponent implements OnInit {


  constructor(private auth: AuthService,
              private router: Router,
              private route: ActivatedRoute) { }





  ngOnInit() {
    // todo query params
    // this.route.

    // todo urls
    // todo subject?
    // this.auth.formState = 'login';
    // todo change
  }


  // todo add success on the bottom


  get state() {
    return this.router.url.split('/')[1];
  }


}
