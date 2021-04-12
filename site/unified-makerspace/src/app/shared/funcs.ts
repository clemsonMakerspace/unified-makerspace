import {FormGroup} from '@angular/forms';
import * as lodash from 'lodash';
import {environment} from '../../environments/environment';


export function showError(form: FormGroup) {
  return function err(field: string) {

    let errorMap = {
      'length': '$ must be six digits.',
      'list': '$ is not in the list.',
      'required': '$ is required.',
      'minlength': '$ must be at least {requiredLength} characters.',
      'email': '@ is not a valid email.'
    };

    let f = form.get(field);
    field = lodash.startCase(field);     // camel case to title case
    let error = '';
    if (f.invalid &&
      (f.touched || form['submitted'])) {
      let errName = Object.keys(f.errors)[0];
      error = errorMap[errName];
      if (!error) {

        error = field + ' is not valid.';
      }

      error = error.replace('@', f.value);
      error = error.replace('$', field);
      error = error.replace(/{([A-aZ-z]*)}/,
        (v, p1) => {
        return f.errors[errName][p1]
        });
    }
    return error;
  };
}


export function useTestData(control: FormGroup) {
  if (!environment.production) {
    for (let [c, v] of Object.entries(control.controls)) {
      v.setValue(environment.user[c]);
    }
  }
}
