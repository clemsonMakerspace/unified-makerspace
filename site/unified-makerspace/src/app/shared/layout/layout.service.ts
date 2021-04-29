import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LayoutService {

  constructor() { }

  // whether the users table is expanded
  usersTableIsExpanded = false;

}
