import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {AuthService} from '../shared/auth/auth.service';
import {Router} from '@angular/router';
import {Auth} from 'aws-amplify'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private auth: AuthService, private router: Router) { }

  loginForm: FormGroup;
  registerForm: FormGroup;
  verificationForm: FormGroup;
  toVerifyEmail = false;

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
    
    this.verificationForm = new FormGroup({
      'code': new FormControl('ABCDEF', Validators.required)
    })

  }


  // todo change url instead?
  switchMode() {
    this.router.navigate([this.formType == 'login' ? 'register' : 'login'])
      .then()

  }
  
  login() {
    // todo check for success
    this.auth.login();
    this.router.navigate(['dashboard']).then()

    //Todo: test sign in with an existing user
    const user = {
      username: this.loginForm.get('username').value,
      password: this.loginForm.get('password').value
   }

    Auth.signIn(user).then(user => {
      console.log(user);
    })
      .catch(err => console.log(err));

  }
  

  registerSuccess = false;
  register() {
    this.auth.register();
    this.registerSuccess = true;

    //Add first and last name entries
    const user = {
      username: this.registerForm.get('username').value,
      password: this.registerForm.get('password').value,
      attributes: {
           email: this.registerForm.get('username').value
           //phone_number
           // other custom attributes
         }
   }


    Auth.signUp(user)
    .then(data => {
      console.log(data);
      this.toVerifyEmail = true;
      this.formType = 'register';
    })
    .catch(err => console.log(err));
  
  }

  verify(){
    Auth.confirmSignUp(this.registerForm.get('username').value, this.verificationForm.get('code').value, 
      {forceAliasCreation: true}).then(data => {
            console.log(data)
            this.toVerifyEmail = false;
            this.formType = 'login'
            this.switchMode()
         })
           .catch(err => console.log(err));
  }
}
