import {Component, OnInit, ViewChild} from '@angular/core';
import {AuthService} from '../shared/auth/auth.service';
import {ApiService} from '../shared/api/api.service';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';
import {Router} from '@angular/router';


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  constructor(public auth: AuthService,
              private api: ApiService,
              private modal: NgbModal,
              private router: Router) {
  }

  @ViewChild('userTokenModal')
  userTokenModal

    // todo delete / edit machines

  userToken: string;

  ngOnInit(): void {
  }

  open(content) {
    this.modal.open(content);
  }

  generateUserToken() {
    this.modal.open(this.userTokenModal)
    this.api.generateUserToken()
      .subscribe((res) => this.userToken = res.user_token,
        () => {
        // todo handle error
      });
  }


  name = '';
  deleteUser() {
    this.api.deleteUser(
      {'user_id': this.auth.user.getValue().user_id}
      ).subscribe(() => {
        this.modal.dismissAll();
        this.router.navigate(['/']).then(()=> {
          this.auth.logout();
        })
    }, (err) => {
        // todo implement
    })
  }


}
