import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { RootComponent } from './root/root.component';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { TasksComponent } from './dashboard/tasks/tasks.component';
import { ModalComponent } from './dashboard/tasks/modal/modal.component';
import { ProfileComponent } from './profile/profile.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { UsersComponent } from './users/users.component';
import { RequestsComponent } from './dashboard/requests/requests.component';
import { UserGraphComponent } from './dashboard/user-graph/user-graph.component';
import { MachinesComponent } from './dashboard/machines/machines.component';

let routes: Routes = [
  // {path: 'root', component: AppComponent, children: [
  //     {path: '', component: LoginComponent},
  //     {path: 'dashboard', component: DashboardComponent}
  //   ]}, // todo remove

  { path: '', component: RootComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'users', component: UsersComponent },
  { path: '**', component: NotFoundComponent },
];

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
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
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    NgxChartsModule,
    BrowserAnimationsModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
