import { Injectable } from '@angular/core';
import {BehaviorSubject} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {


  visits = new BehaviorSubject<any>(null);

  constructor() { }

}
