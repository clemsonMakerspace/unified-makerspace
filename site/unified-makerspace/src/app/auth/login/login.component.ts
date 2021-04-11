import {Component, OnInit} from '@angular/core';
import {AuthService} from '../../shared/auth/auth.service';
import {Router} from '@angular/router';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {showError} from 'src/app/shared/funcs';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private auth: AuthService,
              public router: Router,
              private fb: FormBuilder) {
  }

  loginForm: FormGroup;
  showError: any;

  ngOnInit(): void {

    this.loginForm = this.fb.group({
      email: ['', Validators.required],
      password: ['', Validators.required]
    });

    this.showError = showError(this.loginForm);

    // todo testing - outsource this later
    this.loginForm.setValue({
      'email': 'joe@makerspace.com',
      'password': 'password'
    });

  }

  // todo show loading indicators....

  login() {

    // todo move stuff to api service

    this.loginForm['submitted'] = true;
    this.loginForm['error'] = '';

    if (this.loginForm.valid) {
      this.auth.login(this.loginForm.value).subscribe(
        (res) => {
          try {


            let user = res['user'];
            this.auth.user.next(user); // todo body?
            localStorage.setItem('User', JSON.stringify(user));


            this.router.navigate(['dashboard']).then();
          } catch (e) {
            this.loginForm['error'] = 'Sorry, we\'re having issue with the server.';
          }
        },
        (err) => {
          // todo handle incorrect password
          // todo handle email in use
          this.loginForm['error'] = 'Sorry, we\'re having trouble logging you in.';
        }
      );
    }
  }


}
