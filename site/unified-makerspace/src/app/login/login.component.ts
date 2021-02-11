import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor() { }

  loginForm: FormGroup;


  ngOnInit(): void {

    this.loginForm = new FormGroup({
      'username': new FormControl('joe@makerspace.com', Validators.required),
      'password': new FormControl('password', Validators.required)
    })
  }

}
