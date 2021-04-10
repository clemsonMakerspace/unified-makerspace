import {Component, OnInit, TemplateRef} from '@angular/core';
import {AuthService} from '../shared/auth/auth.service';
import {ApiService} from '../shared/api.service';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';



@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  constructor(public auth: AuthService,
              private api: ApiService,
              private modal: NgbModal) {}

  userToken: string;


  ngOnInit(): void {

  }

  generateUserToken() {
    this.userToken = "RST234NS"
  }

  changePassword() {
    // todo implement
  }


  deleteUser() {
    this.api.deleteUser({"user_id": this.auth.user.getValue().user_id});
  }

  // todo add change password
  // todo remove account management page?

}
