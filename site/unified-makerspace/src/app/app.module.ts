import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { TasksComponent } from './dashboard/tasks/tasks.component';
import {ModalComponent} from './shared/modal/modal.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {RouterModule, Routes} from '@angular/router';
import { RootComponent } from './root/root.component';
import {NgxChartsModule} from '@swimlane/ngx-charts';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { ProfileComponent } from './profile/profile.component';

let routes: Routes = [
  // {path: 'root', component: AppComponent, children: [
  //     {path: '', component: LoginComponent},
  //     {path: 'dashboard', component: DashboardComponent}
  //   ]},

  {path: '', component: RootComponent},
  {path: 'login', component: LoginComponent},
  {path: 'register', component: LoginComponent},
  {path: 'dashboard', component: DashboardComponent},
  {path: 'profile', component: ProfileComponent}

]


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    TasksComponent,
    ModalComponent,
    RootComponent,
    ProfileComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    NgxChartsModule,
    BrowserAnimationsModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
