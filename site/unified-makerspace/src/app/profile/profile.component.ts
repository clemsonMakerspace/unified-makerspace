import {Component, OnInit} from '@angular/core';
import {AuthService} from '../shared/auth/auth.service';
import {ApiService} from '../shared/api/api.service';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  constructor(public auth: AuthService,
              private api: ApiService,
              private modal: NgbModal) {
  }

  // todo add change password
  // todo remove account management page?
  // todo delete / edit machines
  // todo create modals for all of these

  userToken: string;

  ngOnInit(): void {
  }

  generateUserToken() {
    this.api.generateUserToken({})
      .subscribe((res) => this.userToken = res.user_token, () => {
        // todo handle error
      });

  }

  changePassword() {
    this.api.changePassword(null).subscribe();
    // todo implement
  }


  deleteUser() {
    this.api.deleteUser({'user_id': this.auth.user.getValue().user_id});
  }


}
