import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {AuthService} from '../shared/auth/auth.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private auth: AuthService, private router: Router) { }

  loginForm: FormGroup;
  registerForm: FormGroup;



  // can either be login or register
  formType = 'login';


  ngOnInit(): void {

    // todo get params
    this.formType = this.router.url.split('/')[1];

    // todo only for testing
    this.loginForm = new FormGroup({
      'username': new FormControl('joe@makerspace.com', Validators.required),
      'password': new FormControl('password', Validators.required),
    })

    this.registerForm = new FormGroup({
      'username': new FormControl('joe@makerspace.com', Validators.required),
      'password': new FormControl('password', Validators.required),
      'confirmPassword': new FormControl('', Validators.required)
    })


  }


  // todo change url instead?
  switchMode() {
    this.router.navigate([this.formType == 'login' ? 'register' : 'login'])
      .then()

  }

  login() {
    // todo check for success
    this.auth.login(this.loginForm.get('username').value, this.loginForm.get('password').value);
    this.router.navigate(['dashboard']).then()
  }

  // todo make sure forms are valid prior
  registerSuccess = false;
  register() {
    this.auth.register();
    this.registerSuccess = true;
    // todo send confirmation email
  }


}
