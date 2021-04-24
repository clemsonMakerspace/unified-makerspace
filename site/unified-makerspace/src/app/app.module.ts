import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {RouterModule, Routes} from '@angular/router';
import {RootComponent} from './root/root.component';
import {NgxChartsModule} from '@swimlane/ngx-charts';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';

import {AppComponent} from './app.component';
import {AuthComponent} from './auth/auth.component';
import {DashboardComponent} from './dashboard/dashboard.component';
import {TasksComponent} from './dashboard/tasks/tasks.component';
import {ModalComponent} from './dashboard/tasks/modal/modal.component';
import {ProfileComponent} from './profile/profile.component';
import {NotFoundComponent} from './not-found/not-found.component';
import {UsersComponent} from './users/users.component';
import {RequestsComponent} from './dashboard/requests/requests.component';
import {UserGraphComponent} from './dashboard/user-graph/user-graph.component';
import {MachinesComponent} from './dashboard/machines/machines.component';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import {VisitorComponent} from './auth/visitor/visitor.component';
import {RegisterComponent} from './auth/register/register.component';
import {LoginComponent} from './auth/login/login.component';
import {ChangePasswordComponent} from './profile/change-password/change-password.component';
import {InterceptorService} from './shared/api/interceptor.service';
import {ResetPasswordComponent} from './auth/reset-password/reset-password.component';

let routes: Routes = [
  {path: '', component: RootComponent},
  {path: 'login', component: AuthComponent},
  {path: 'forgot', component: ResetPasswordComponent},
  {path: 'register', component: AuthComponent},
  {path: 'dashboard', component: DashboardComponent},
  {path: 'profile', component: ProfileComponent},
  {path: 'users', component: UsersComponent},
  {path: '**', component: NotFoundComponent},
];

@NgModule({
  declarations: [
    AppComponent,
    AuthComponent,
    DashboardComponent,
    TasksComponent,
    ModalComponent,
    RootComponent,
    ProfileComponent,
    NotFoundComponent,
    UsersComponent,
    RequestsComponent,
    UserGraphComponent,
    MachinesComponent,
    VisitorComponent,
    RegisterComponent,
    LoginComponent,
    ChangePasswordComponent,
    ResetPasswordComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    NgxChartsModule,
    BrowserAnimationsModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    NgbModule,
  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: InterceptorService,
    multi: true
  }],
  bootstrap: [AppComponent],
})
export class AppModule {
}
