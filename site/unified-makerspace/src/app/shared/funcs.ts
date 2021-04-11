import {FormGroup} from '@angular/forms';
import * as lodash from 'lodash';


export function showError(form: FormGroup) {
  return function err(field: string) {
    let f = form.get(field);
    // camel case to title case
    field = lodash.startCase(field);
    let error = "";
    if (f.touched || form['submitted']) {
      if (f.invalid) {
        error = field + " is not valid."
        if (f.value == '') {
          error = field + " is required."
        }
      }
    }
    return error;
  }

}
