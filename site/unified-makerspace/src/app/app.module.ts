import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {RouterModule, Routes} from '@angular/router';
import {HomeComponent} from './home/home.component';
import {NgxChartsModule} from '@swimlane/ngx-charts';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';

import {AppComponent} from './app.component';
import {AuthComponent} from './auth/auth.component';
import {DashboardComponent} from './dashboard/dashboard.component';
import {TasksComponent} from './dashboard/tasks/tasks.component';
import {CreateTaskComponent} from './dashboard/tasks/create-modal/create-task.component';
import {ProfileComponent} from './profile/profile.component';
import {NotFoundComponent} from './not-found/not-found.component';
import {AccountsComponent} from './accounts/accounts.component';
import {RequestsComponent} from './dashboard/requests/requests.component';
import {VisitorsGraphComponent} from './dashboard/visitors/visitors-graph/visitors-graph.component';
import {MachinesComponent} from './dashboard/machines/machines.component';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import {VisitorComponent} from './auth/visitor/visitor.component';
import {RegisterComponent} from './auth/register/register.component';
import {LoginComponent} from './auth/login/login.component';
import {ChangePasswordComponent} from './profile/change-password/change-password.component';
import {InterceptorService} from './shared/interceptor.service';
import {ResetPasswordComponent} from './auth/reset-password/reset-password.component';
import { VisitorsComponent } from './dashboard/visitors/visitors.component';
import { VisitorsTableComponent } from './dashboard/visitors/visitors-table/visitors-table.component';
import { UsersComponent } from './dashboard/users/users.component';
import { TaskDetailsComponent } from './dashboard/tasks/details-modal/task-details.component';
import { ErrorComponent } from './dashboard/error/error.component';
import {AuthGuard} from './shared/auth-guard.service';

let routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'login', component: AuthComponent},
  {path: 'forgot', component: ResetPasswordComponent},
  {path: 'register', component: AuthComponent},
  {path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard]},
  {path: 'profile', component: ProfileComponent, canActivate: [AuthGuard]},
  {path: 'users', component: AccountsComponent},
  {path: '**', component: NotFoundComponent},
];

@NgModule({
  declarations: [
    AppComponent,
    AuthComponent,
    DashboardComponent,
    TasksComponent,
    CreateTaskComponent,
    HomeComponent,
    ProfileComponent,
    NotFoundComponent,
    AccountsComponent,
    RequestsComponent,
    VisitorsGraphComponent,
    MachinesComponent,
    VisitorComponent,
    RegisterComponent,
    LoginComponent,
    ChangePasswordComponent,
    ResetPasswordComponent,
    VisitorsComponent,
    VisitorsTableComponent,
    UsersComponent,
    TaskDetailsComponent,
    ErrorComponent,
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
