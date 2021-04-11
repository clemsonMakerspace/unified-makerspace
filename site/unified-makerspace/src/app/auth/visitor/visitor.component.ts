import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, ValidatorFn, Validators} from '@angular/forms';
import * as majors from './majors.json';
import {AuthService} from '../../shared/auth/auth.service';
import {ApiService} from '../../shared/api/api.service';
import {showError} from '../../shared/funcs';

/* validates that item is in list */
export function ListValidator(list: string[]): ValidatorFn {
  return (control: FormControl) => list.includes(control.value) ? null : {'error': true}
}

@Component({
  selector: 'app-visitor',
  templateUrl: './visitor.component.html',
  styleUrls: ['./visitor.component.scss']
})
export class VisitorComponent implements OnInit {


  // todo update card text
  // todo do you want to leave this page
  // todo hardware id validation?


  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    public auth: AuthService) {
  }

  visitorForm: FormGroup;
  showError: any;
  majors = majors['default'];
  degrees = ['Phd', 'Masters', 'B.A', 'B.S'];

  ngOnInit(): void {

    this.visitorForm = this.fb.group({
      major: ['', [Validators.required, ListValidator(this.majors)]],
      degree: ['', [Validators.required, ListValidator(this.degrees)]],
      hardwareId: ['', Validators.required],
    });

    this.showError = showError(this.visitorForm);

    // todo for testing
    this.visitorForm.setValue({
      'major': 'Computer Science',
      'degree': 'Phd',
      'hardwareId': 'XX89712'
    })

  }


  onSubmit() {

    this.visitorForm['submitted']  = true;

    if (this.visitorForm.valid) {
      this.api.createVisitor({
        ...this.auth.newUserInfo,
        ...this.visitorForm.value
      }).subscribe((res) => {
        // clear sensitive data
        this.auth.newUserInfo = null;
        // todo show loading
        this.auth.regState = 'success'
      }, (err) => {
        // todo better error handling ?
        this.visitorForm['error'] = "Sorry, we're having issues with the server.";
      })
    }



  }

}
